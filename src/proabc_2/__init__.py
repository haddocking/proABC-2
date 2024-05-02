import os

HMMER_PATH = os.environ.get("HMMER_PATH")
IGBLAST_PATH = os.environ.get("IGBLAST_PATH")
IGDATA = os.environ.get("IGDATA")

HELP_MSG = "Check the installation instructions of THIRD-PARTY dependencies at `https://github.com/haddocking/proabc-2`"

if HMMER_PATH is None:
    _msg = "Please set the HMMER_PATH environment variable" + os.linesep + HELP_MSG
    print(_msg)
    exit(1)

if IGBLAST_PATH is None:
    _msg = "Please set the IGBLAST_PATH environment variable" + os.linesep + HELP_MSG
    print(_msg)
    exit(1)

if IGDATA is None:
    _msg = "Please set the IGDATA environment variable" + os.linesep + HELP_MSG
    print(_msg)
    exit(1)
