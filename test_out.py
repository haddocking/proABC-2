#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Francesco Ambrosetti

import unittest
import filecmp
import proABC as pr
import os as os

class TestOut(unittest.TestCase):

    """Create testing class"""

    def setUp(self):

        # Input
        # igblastp database for heavy Kappa and Light chain
        base_dir = os.path.dirname(__file__)
        ig_database_H = os.path.join(base_dir, 'database', 'IGHVp.fasta')
        ig_database_K = os.path.join(base_dir, 'database', 'IGKVp.fasta')
        ig_database_L = os.path.join(base_dir, 'database', 'IGLVp.fasta')

        # only needed if you want to specify the path for HMMER
        hmmpath = ''
        jobid = 'Test_data/'
        light = 'light.fasta'
        heavy = 'heavy.fasta'

        # Open file log
        open(os.path.join(jobid, 'test.log'), 'w').close()  # create empty file
        log = open(os.path.join(jobid, 'test.log'), 'a')

        # Run script to create output
        pr.get_features(jobid, hmmpath, light, heavy, ig_database_H, ig_database_K, ig_database_L, log)
        self.golden_feat = 'Test_data/Test-features.csv'
        log.close()


    def test_features(self):
        """Test features files"""

        # Ini
        feat = 'Example/Example-features.csv'

        # Testing
        self.assertTrue(filecmp.cmp(self.golden_feat, feat), "Features files are different \n")

if __name__ == '__main__':
    unittest.main()