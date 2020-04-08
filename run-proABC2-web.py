#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020:
#   Francesco Ambrosetti
#

"""
This script is used to launch and download the proABC-2 webserver predictions.
It requires only the heavy and light chain fasta files.

Usage:
    python run_proABC2_web.py <heavy chain fasta file> <light chain fasta file>

Example:
    python run_proABC2_web.py ./heavy.fasta ./light.fasta

Author: {0}
Email: {1}

"""

import os
import re
import requests
import sys
from time import sleep
import urllib3


__author__ = "Francesco Ambrosetti"
__email__ = "ambrosetti.francesco@gmail.com"
USAGE = __doc__.format(__author__, __email__)


def write_error(msg, use=True):
    """
    Writes error message and exit
    Args:
        msg (str): message to be written
        use (bool): True prints also the USAGE, False does not

    Returns:
        0
    """

    if use:
        sys.stderr.write(msg)
        sys.stderr.write(USAGE)
        sys.exit(1)
    elif not use:
        sys.stderr.write(msg)
        sys.exit(1)

    return 0


def check_input(args):
    """
    Validates user inputs
    Args:
        args (list): list of user inputs

    Returns:
        heavy (str): path to the input heavy.fasta file
        light (str): path to the light.fasta file
    """

    if not len(args):
        emsg = f'\nERROR!! No files provided\n'
        write_error(msg=emsg, use=True)

    elif len(args) < 2:
        if args[0] == '-h':
            sys.stderr.write(USAGE)
            sys.exit(1)
        else:
            emsg = f'\nERROR!! No files provided\n'
            write_error(msg=emsg, use=True)

    else:
        if not os.path.isfile(args[0]):
            emsg = f'\nERROR!! File {args[0]} not found or not readable\n'
            write_error(msg=emsg, use=True)
        if not os.path.isfile(args[1]):
            emsg = f'\nERROR!! File {args[1]} not found or not readable\n'
            write_error(msg=emsg, use=True)

        heavy = args[0]
        light = args[1]

        return heavy, light


class RunProABC2:
    """ Class to run and collect the proABC-2 webserver predictions"""

    def __init__(self, heavy, light, proabc_url='https://bianca.science.uu.nl/proabc2/'):
        """
        Constructor for the RunProABC2 class
        Args:
            heavy (str): fasta file of the heavy chain
            light (str): fasta file of the light chain
            proabc_url (str): url to the proABC-2 webserver
        """
        self.heavy = heavy
        self.light = light
        self.proabc_url = proabc_url

    def get_csrf(self):
        """
        Retrieves the csrf token
        Returns:
            client (requests.session object): request.session object
            csrftoken (str): csrf token of the session
        """

        # Check connection
        client = requests.session()
        r = ''
        try:
            r = client.get(self.proabc_url, verify=False)
        except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema):
            emsg = f'\nERROR!! {self.proabc_url} does not exist or not reachable\n\n'
            write_error(msg=emsg, use=False)

        # Get token
        csrftoken = ''
        try:
            line = re.search(r'<input id="csrf_token" name="csrf_token" type="hidden" value=(\S+)', r.text).group(1)
            csrftoken = re.findall(r'"([^"]*)"', line)[0]
        except AttributeError as e:
            emsg = f'\nProblems retrieving csrf_token: {e}\n\n'
            write_error(msg=emsg, use=False)

        return client, csrftoken

    def launch(self):
        """
        Run a proABC-2 job
        Returns:
            out_url (str): url of the output
            job_id (str): job id
        """

        # Retrieve csrf token first
        client, csrf_token = self.get_csrf()

        # Parameters to run proABC-2
        params = {'csrf_token': csrf_token,
                  'sequence_heavy': open(self.heavy).read(),
                  'sequence_light': open(self.light).read()}

        # Run job
        job = client.post(url=self.proabc_url, data=params, verify=False)

        # Get results url
        result = job.text
        job_id = re.search(r'Run (\S+)', result).group(1)
        out_url = f'{self.proabc_url}run/{job_id}'

        return out_url, job_id

    @staticmethod
    def check_status(proabc_job):
        """
        Check status of the proABC-2 job and return a error if
        the run has failed
        Args:
            proabc_job (str): url of the proABC-2 job

        Returns:
            0
        """

        client = requests.session()
        r = ''

        # Check connection
        try:
            r = client.get(proabc_job, verify=False)
        except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema):
            emsg = f'\nERROR!! {proabc_job} does not exist or not reachable\n\n'
            write_error(msg=emsg, use=False)

        # Retrieve run status
        status = ''
        try:
            status = re.search(r'Status: (\S+)', r.text).group(1)
        except AttributeError:
            pass

        if status == 'Failed':
            emsg = f'Your run: {proabc_job} has failed\n'
            write_error(msg=emsg, use=False)

        return 0

    @staticmethod
    def download_results(job_name, result_url='https://bianca.science.uu.nl/proabc2/res/'):
        """
        Downloads proABC-2 predictions and writes them
        into two files: <job_name>_heavy.csv and <job_name>_light.csv
        Args:
            job_name (str): name of the proABC-2 job
            result_url (str): url of the result page

        Returns:
            0
        """

        # Create result urls
        client = requests.session()
        job_results_heavy = f'{result_url}{job_name}/heavy-pred.csv'
        job_results_light = f'{result_url}{job_name}/light-pred.csv'
        r_heavy = ''
        r_light = ''

        # Download results
        try:
            r_heavy = client.get(job_results_heavy, verify=False)
            r_light = client.get(job_results_light, verify=False)
        except requests.exceptions.ConnectionError:
            emsg = f'\nERROR!! {job_results_heavy} or {job_results_light} does not exist or not reachable\n\n'
            write_error(msg=emsg, use=False)

        # Write results into separated files
        with open(f'{job_name}_heavy.csv', 'w') as he:
            he.write(r_heavy.text)
        with open(f'{job_name}_light.csv', 'w') as li:
            li.write(r_light.text)

        return 0


if __name__ == "__main__":

    # Disable annoying warnings
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Validates inputs
    file_heavy, file_light = check_input(sys.argv[1:])

    # Define class
    proabc_web = RunProABC2(file_heavy, file_light)

    # Run proABC-2 web-server
    job_url, id_job = proabc_web.launch()

    # Check if run has failed
    proabc_web.check_status(job_url)

    # Sleep to not overload the webserver
    # when multiple jobs are run sequentially
    # and to be able to download the results
    sleep(10)

    # Download the results
    proabc_web.download_results(job_name=id_job)

    print(f'{job_url} --- Success')
