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
    :param msg: <string> message to be written
    :param use: <boolean> True prints also the USAGE
    False does not
    :return: 0
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
    :param args: <list> list of user inputs
    :return: <string> heavy: path to the input heavy.fasta file
    <string> light: path to the light.fasta file
    """""

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


def get_csrf(url):
    """
    Retrieves the csrf token of a url.
    :param url: <string> url of the website
    :return: <string> csrf token
    <requests.session object> client
    """

    # Check connection
    client = requests.session()
    r = ''
    try:
        r = client.get(url, verify=False)
    except requests.exceptions.ConnectionError:
        emsg = f'\nERROR!! {url} does not exist or not reachable\n\n'
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


def launch(heavy, light, proabc_url='https://bianca.science.uu.nl/proabc2/'):
    """
    Run the job on the proABC2 webserver
    :param heavy: <string> fasta file of the heavy chain
    :param light: <string> fasta file of the light chain
    :param proabc_url: <string> url to the proABC-2 webserver
    :return: <string> url of the output
    <string> job id
    """

    # Retrieve csrf token first
    client, csrf_token = get_csrf(proabc_url)

    # Parameters to run proABC-2
    params = {'csrf_token': csrf_token,
              'sequence_heavy': open(heavy).read(),
              'sequence_light': open(light).read()}

    # Run job
    job = client.post(url=proabc_url, data=params, verify=False)

    # Get results url
    result = job.text
    job_id = re.search(r'Run (\S+)', result).group(1)
    out_url = f'{proabc_url}run/{job_id}'

    return out_url, job_id


def check_status(proabc_job):
    """
    Check status of the proABC-2 job and return a error if
    the run has failed
    :param proabc_job: <string> url to the job
    :return: 0
    """
    client = requests.session()
    r = ''

    # Check connection
    try:
        r = client.get(proabc_job, verify=False)
    except requests.exceptions.ConnectionError:
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


def download_results(job_name, result_url='https://bianca.science.uu.nl/proabc2/res/'):
    """
    Downloads proABC-2 predictions and writes them
    into two files: {jobname}_heavy.csv and {jobname}_light.csv
    :param job_name: <string> name of the job
    :param result_url: <string> url of the result page
    :return: 0
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

    # Run proABC-2 web-server
    job_url, id_job = launch(heavy=file_heavy, light=file_light)

    # Check if run has failed
    check_status(job_url)

    # Sleep to not overload the webserver
    # when multiple jobs are run sequentially
    # and to be able to download the results
    sleep(10)

    # Download the results
    download_results(job_name=id_job)

    print(f'{job_url} --- Success')
