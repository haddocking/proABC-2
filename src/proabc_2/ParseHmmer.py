import os
import re

#
# These functions always return something. Control of the alignment will be performed later in the program.
# In the meanwhile, if the input consists of multiple sequences the program will still run if one sequence
# raise an error.
#


def readhmmscan(file):
    """parse the hmmscan output"""

    evalue = 1

    # Check if file exists
    if not os.path.isfile(file):
        return evalue

    else:
        domains = 0
        handle = open(file, "r")
        for line in handle:
            if not line.startswith("#"):
                domains = domains + 1
                split = line.split()
                evalue = float(split[6])

        handle.close()
    return evalue


def read_align(file):
    """parse the hmmalign output
    4fp8_J         EVQLQESGGGLVQPGESLRLSCVGSGSSFGESTlsY----YAVSWVRQAPGKGLEWLSIINA-------GGGDIDYADSVEGRFTISR...
    #=GR 4fp8_J PP 8**************************997765445....**********************.......*******************...
    #=GC PP_cons   8**************************997765..5....**********************.......*******************...
    #=GC RF        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx..xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx...
    """
    aligned = ""

    if not os.path.isfile(file):  # Check if file exists
        return aligned
    else:
        handle = open(file, "r")

        for line in handle:

            # Extract aligned sequence
            if (
                not line.startswith("#")
                and not line.startswith("\n")
                and not line.startswith("//")
            ):
                split = line.split()
                aligned = aligned + split[1]

            # Check if alignment failed'''
            elif re.match("\#\=GC RF", line):
                split = line.split()
                if re.search(
                    "\.", split[2]
                ):  # Correct alignments do not present any dot in the GC RF line
                    aligned = ""
                    break

        handle.close()

    return aligned
