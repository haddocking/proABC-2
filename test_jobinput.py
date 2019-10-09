#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Francesco Ambrosetti

import unittest
import jobinput as ji
import os as os
import numbering as nu

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
        # Sequences aligned (normal H3)
        self.golden_h = 'EVQLVESGGGLVQPGGSLRLSCAASGYTFTN-------YGMNWVRQAPGKGLEWVGWINT-------YTGEPTYAADFKRRFTFSLDTSKSTAYLQMNSLRAEDTAVYYCAKYPHYYGSSHWYF----------------DVWGQGTLVTVSS'  # Sequence H 1bj1
        self.golden_l = 'DIQMTQSPSSLSASVGDRVTITCSASQDIS----------NYLNWYQQKPGKAPKVLIYF--------TSSLHSGVPSRFSGSGSG--------TDFTLTISSLQPEDFATYYCQQYSTVP--------WTFGQGTKVEIKRTV'  # Sequence L (K) 1bj1
        self.golden_l_l = '---ALTQPASVSGSPGQSITISCTGTSSDVGGY-------NYVSWYQQHPGKAPKLMIYG--------VTNRPSGVSNRFSGSKSG--------NTASLTISGLQAGDEADYYCSSYTSTRTP------YVFGTGTKV------'  # Sequence L (L) 3kdm

        # Isotypes
        self.isotype_h = 'H'  # Isotype H
        self.isotype_l = 'K'  # Isotype L

        # Lenghts
        self.gold_len_h = [7, 4, 12]  # H 1bj1
        self.gold_len_l_k = [7, 3, 6]  # L (Kappa) 1bj1
        self.gold_len_l_l = [11, 3, 8]  # L (Lambda) 2kdm

        # Canonical structures
        self.golden_cs_h = [1, 2, 'bulged']  # Canonical H 1bj1
        self.golden_cs_k = [2, 1, 1]  # Canonical (Kappa) 1bj1
        self.golden_cs_l = [6, 1, 1]  # Canonical (Lamba) 3kdm

    def test_readInput(self):

        """Test oneLiner fasta and read input functions"""

        if not os.path.exists(os.path.join(TestJi.jobid, 'tmp')):
            os.makedirs(os.path.join(TestJi.jobid, 'tmp'))

        ji.oneLiner_fasta(TestJi.jobid, self.file_h, self.out_h)
        ji.oneLiner_fasta(TestJi.jobid, self.file_l, self.out_l)

        # Read input
        target_name = TestJi.jobid.replace('/', '')
        seq_h, isotype_h = ji.read_input_single(self.out_h, TestJi.jobid, TestJi.hmmpath, target_name)
        seq_l, isotype_l = ji.read_input_single(self.out_l, TestJi.jobid, TestJi.hmmpath, target_name)

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

    def test_loopLen(self):

        '''Test length calculation of the HV loops'''

        # Heavy chain
        len_h = list(nu.H(self.golden_h).loopLen().values())
        self.assertListEqual(self.gold_len_h , len_h, "Heavy chain loop lengths are different \n")

        # Light chain (K)
        len_k = list(nu.K(self.golden_l).loopLen().values())
        self.assertListEqual(self.gold_len_l_k, len_k, "Light chain (K) loop lengths are different \n")

        # Light chain (L)
        len_l = list(nu.L(self.golden_l_l).loopLen().values())
        self.assertListEqual(self.gold_len_l_l, len_l, "Light chain (L) loop lengths are different \n")

    def test_getCs(self):
        '''Test canonical structures
        calculation'''

        # Heavy chain
        cs_h = nu.H(self.golden_h).getCs()
        self.assertListEqual(self.golden_cs_h, cs_h, "Heavy chain canonical structures are different \n")

        # Light chain (K)
        cs_k = nu.K(self.golden_l).getCs()
        self.assertListEqual(self.golden_cs_k, cs_k, "Light chain (K) canonical structures are different \n")

        # Light chain (L)
        cs_l = nu.L(self.golden_l_l).getCs()
        self.assertListEqual(self.golden_cs_l, cs_l, "Light chain (L) canonical structures are different \n")



if __name__ == '__main__':
    unittest.main()