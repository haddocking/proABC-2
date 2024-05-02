import os

HMMER_PATH = os.environ["HMMER_PATH"]
IGBLAST_PATH = os.environ["IGBLAST_PATH"]
IGDATA = os.environ["IGDATA"]

HELP_MSG = "Please check the installation instructions at <https://github.com/haddocking/proabc-2>"

if HMMER_PATH is None:
    _msg = "Please set the HMMER_PATH environment variable" + os.newline + HELP_MSG
    print(_msg)
    exit(1)

if IGBLAST_PATH is None:
    _msg = "Please set the IGBLAST_PATH environment variable" + os.newline + HELP_MSG
    print(_msg)
    exit(1)

if IGDATA is None:
    _msg = "Please set the IGDATA environment variable" + os.newline + HELP_MSG
    print(_msg)
    exit(1)
