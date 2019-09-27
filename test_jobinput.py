#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Francesco Ambrosetti

import unittest
import jobinput as ji
import os as os

class TestJi(unittest.TestCase):

    """Create testing class"""

    jobid = 'Test_data/'
    hmmpath = ''

    def setUp(self):

        # input files
        self.file_h = 'heavy.fasta'
        self.file_l = 'light.fasta'

        # output files
        self.out_h = 'heavy_test.fasta'
        self.out_l = 'light_test.fasta'

        # golden files
        self.golden_h = 'EVQLVESGGGLVQPGGSLRLSCAASGYTFTN-------YGMNWVRQAPGKGLEWVGWINT-------YTGEPTYAADFKRRFTFSLDTSKSTAYLQMNSLRAEDTAVYYCAKYPHYYGSSHWYF----------------DVWGQGTLVTVSS'  # Sequence H
        self.golden_l = 'DIQMTQSPSSLSASVGDRVTITCSASQDIS----------NYLNWYQQKPGKAPKVLIYF--------TSSLHSGVPSRFSGSGSG--------TDFTLTISSLQPEDFATYYCQQYSTVP--------WTFGQGTKVEIKRTV'  # Sequence L
        self.isotype_h = 'H'  # Isotype H
        self.isotype_l = 'K'  # Isotype L

    def test_readInput(self):

        """Test oneLiner fasta and read input functions"""

        if not os.path.exists(os.path.join(TestJi.jobid, 'tmp')):
            os.makedirs(os.path.join(TestJi.jobid, 'tmp'))

        ji.oneLiner_fasta(TestJi.jobid, self.file_h, self.out_h)
        ji.oneLiner_fasta(TestJi.jobid, self.file_l, self.out_l)

        # Read input
        target_name = TestJi.jobid.replace('/', '')
        seq_h, isotype_h, message_h = ji.read_input_single(self.out_h, TestJi.jobid, TestJi.hmmpath, target_name)
        seq_l, isotype_l, message_l = ji.read_input_single(self.out_l, TestJi.jobid, TestJi.hmmpath, target_name)

        # Testing chain H
        self.assertEqual(self.golden_h, seq_h, "Heavy chain is different \n")  # Alignment
        self.assertEqual(self.isotype_h, isotype_h, "Heavy chain isotype is different \n")  # Isotype

        # Testing chain L
        self.assertEqual(self.golden_l, seq_l, "Light chain is different \n")  # Alignment
        self.assertEqual(self.isotype_l, isotype_l, "Light chain isotype is different \n")  # Isotype

        # Empty tmp dir
        for f in os.listdir(TestJi.jobid + 'tmp/'):
            os.remove(TestJi.jobid + 'tmp/' + f)

        # Remove tmp dir
        os.rmdir(TestJi.jobid + 'tmp/')

if __name__ == '__main__':
    unittest.main()