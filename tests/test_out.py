#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Francesco Ambrosetti

import filecmp
import os
import shutil
from pathlib import Path

import pytest

import proabc_2.proABC as pr


# Use pytest fixtures for setup
@pytest.fixture
def setup_environment(tmp_path):
    database_dir = Path(Path(__file__).parent.parent, "src", "proabc_2", "database")
    ig_database_H = os.path.join(database_dir, "IGHVp.fasta")
    ig_database_K = os.path.join(database_dir, "IGKVp.fasta")
    ig_database_L = os.path.join(database_dir, "IGLVp.fasta")

    hmmpath = ""
    jobid = str(tmp_path / "Test_data")
    os.makedirs(jobid, exist_ok=True)
    light = "light.fasta"
    heavy = "heavy.fasta"

    # Make a temporary folder to run the tests in
    test_dir = Path("tmp")
    test_dir.mkdir(exist_ok=True)
    # test_dir = str(test_dir) + "/"

    # Put the input in the temporary folder
    src = Path(Path(__file__).parent, "golden_data", "light.fasta")
    dst = Path(test_dir, "light.fasta")
    shutil.copy(src, dst)

    src = Path(Path(__file__).parent, "golden_data", "heavy.fasta")
    dst = Path(test_dir, "heavy.fasta")
    shutil.copy(src, dst)

    log_path = os.path.join(jobid, "test.log")
    with open(log_path, "w") as log:  # create empty file and use as log
        pr.get_features(
            str(test_dir) + "/",
            hmmpath,
            light,
            heavy,
            ig_database_H,
            ig_database_K,
            ig_database_L,
            log,
        )

    # golden_feat = os.path.join(jobid, 'Test-features.csv')
    golden_features = Path(Path(__file__).parent, "golden_data", "Test-features.csv")
    yield golden_features, os.path.join("Example", "Example-features.csv")

    # Clean up the temporary folder
    shutil.rmtree(test_dir)


def test_features(setup_environment):
    golden_feat, feat = setup_environment
    assert filecmp.cmp(golden_feat, feat), "Features files are different"
