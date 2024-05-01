import os

HMMER_PATH = os.environ["HMMER_PATH"]
IGBLAST_PATH = os.environ["IGBLAST_PATH"]
IGDATA = os.environ["IGDATA"]

if HMMER_PATH is None:
    print("Please set the HMMER_PATH environment variable")
    exit(1)

if IGBLAST_PATH is None:
    print("Please set the IGBLAST_PATH environment variable")
    exit(1)

if IGDATA is None:
    print("Please set the IGDATA environment variable")
    exit(1)
