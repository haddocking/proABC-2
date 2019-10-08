#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Francesco Ambrosetti

import unittest
import filecmp
import proABC as pr

class TestOut(unittest.TestCase):

    """Create testing class"""

    def setUp(self):

        # Run script to create output
        pr.prediction('Example', 'heavy.fasta', 'light.fasta')
        self.golden_feat = 'Test_data/Example-features.csv'
        self.golden_pred_h = 'Test_data/heavy-pred.csv'
        self.golden_pred_l = 'Test_data/light-pred.csv'

    def test_features(self):
        """Test features files"""

        # Ini
        feat = 'Example/Example-features.csv'

        # Testing
        self.assertTrue(filecmp.cmp(self.golden_feat, feat), "Features files are different \n")

    # def test_pred_h(self):
    #     """Test heavy chain predictions"""
    #
    #     # Ini
    #     pred_h = 'Example/heavy-pred.csv'
    #
    #     # Testing
    #     self.assertTrue(filecmp.cmp(self.golden_pred_h, pred_h), "Heavy chain predictions are different \n")
    #
    # def test_pred_l(self):
    #     """Test light chain predictions"""
    #
    #     # Ini
    #     pred_l = 'Example/light-pred.csv'
    #
    #     # Testing
    #     self.assertTrue(filecmp.cmp(self.golden_pred_l, pred_l), "Light chain predictions are different \n")


if __name__ == '__main__':
    unittest.main()