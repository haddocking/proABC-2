import os
import re
import subprocess as sub
from pathlib import Path

from Bio.Seq import Seq

from proabc_2.ParseHmmer import read_align, readhmmscan

from . import HMMER_PATH, IGBLAST_PATH


def read_input_single(file, jobid, hmmpath):
    """Read input file. Check if sequence is a protein or a nucleotide. Scan and align the sequences.
    Return a dictionary with sequence header as key and heavy and light chain as sequences.
    """
    thr = float(10e-40)
    aligned = ""
    isotype = ""
    filename = f"{jobid}{file}"
    handle = open(filename, "r")
    # can be heavy or light
    header = ""

    for line in handle:
        line = line.rstrip("\n")
        line = line.rstrip("\r")
        line = line.rstrip()
        matchObj1 = re.match(">", line)
        if matchObj1:
            header = line.replace(">", "")

        else:

            if isDNA(line):

                write_warning(
                    "DNA sequence found in: {}. Sequence has been translated".format(
                        file
                    ),
                    jobid,
                )

                line = Seq(line.replace("\n", ""))
                # Translate sequence using biopython
                line = str(line.translate())
                line = line.replace("*", "")
                # check if translated sequence has strange amino acid inside
                if not isProtein(line):
                    write_error(
                        header
                        + " includes unknown amino acids. Please check your sequence\n",
                        jobid,
                    )

                # replace dna seq with the translated one
                # it is needed because later it will be used by igblastp
                new_seq = f">{header}\n{line}"
                with open(filename, "w") as f:
                    f.write(new_seq)
            else:
                # check if sequence is protein
                if not isProtein(line.replace("\n", "")):
                    write_error(
                        header
                        + " includes unknown amino acids. Please check your sequence\n",
                        jobid,
                    )

            searchInputName = os.path.join(jobid, "tmp", "search.fasta")
            searchOutputName = os.path.join(jobid, "tmp", "scan.txt")
            alignOutputName = os.path.join(jobid, "tmp", "align.ali")

            fh = open(searchInputName, "w")
            fh.write(">" + header + "\n" + line + "\n")
            fh.close()

            # Define paths to .hmm files
            if os.path.exists(os.path.join(jobid, "MarkovModels/")):
                src_path = os.path.join(jobid, "MarkovModels/")
            else:
                base_dir = os.path.dirname(__file__)
                src_path = os.path.join(base_dir, "MarkovModels/")

            heavy_hmm = os.path.join(src_path, "HEAVY.hmm")
            kapp_hmm = os.path.join(src_path, "KAPPA.hmm")
            lambda_hmm = os.path.join(src_path, "LAMBDA.hmm")

            # Calculate evalues
            evalueH = float(
                scan(searchInputName, heavy_hmm, hmmpath, jobid, searchOutputName)
            )
            evalueK = float(
                scan(searchInputName, kapp_hmm, hmmpath, jobid, searchOutputName)
            )
            evalueL = float(
                scan(searchInputName, lambda_hmm, hmmpath, jobid, searchOutputName)
            )

            # more than one domain found in the input sequence. HMM failed to align sequence
            if not evalueH:
                message = "Alignment failed for chain H:\n" + line
                write_error(message, jobid)

            if not evalueK:
                message = "Alignment failed for chain L (Kappa):\n" + line
                write_error(message, jobid)

            if not evalueL:
                message = "Alignment failed for chain L (Lambda):\n" + line
                write_error(message, jobid)

            if (evalueH > thr) and (evalueK > thr) and (evalueL > thr):

                message = "Your input sequence has not been recognized as an antibody. Please check your input: {}".format(
                    header
                )
                write_error(message, jobid)

            if (evalueH < thr and evalueK < thr) or (evalueH < thr and evalueL < thr):
                message = "Single chain antibody found in {}. Please provide heavy and light chain as separate sequences.".format(
                    header
                )
                write_error(message, jobid)

            # identify isotype
            if evalueH < thr:

                if file == "light_format.fasta":
                    warn = "Heavy chain found when light expected"
                    write_error(warn, jobid)
                aligned = align(
                    searchInputName, heavy_hmm, hmmpath, jobid, alignOutputName
                )

                if not aligned:
                    message = "Alignment failed for chain H:\n" + line
                    write_error(message, jobid)
                isotype = "H"

            if (evalueK < evalueL) and (evalueK < thr):
                if file == "heavy_format.fasta":
                    warn = "Kappa chain found when heavy expected."
                    write_error(warn, jobid)
                aligned = align(
                    searchInputName, kapp_hmm, hmmpath, jobid, alignOutputName
                )

                if not aligned:
                    message = "Alignment failed for chain L:\n" + line + "\n"
                    write_error(message, jobid)
                isotype = "K"

            if (evalueL < evalueK) and (evalueL < thr):
                if file == "heavy_format.fasta":
                    warn = "Lambda chain found when heavy expected."
                    write_error(warn, jobid)
                aligned = align(
                    searchInputName, lambda_hmm, hmmpath, jobid, alignOutputName
                )

                if not aligned:
                    message = "Alignment failed for chain L:\n" + line + "\n"
                    write_error(message, jobid)
                isotype = "L"

    handle.close()
    return aligned, isotype


def isDNA(seq):
    """Check if nucleotide.

    Allowable characters are A,C,G,T.
    Other characters will invalid the sequence.
    """
    nn = 1

    aset = ["A", "C", "G", "T"]
    # Check whether sequence seq contains ONLY items in aset.
    for c in seq:

        if c not in aset:
            nn = 0

    return nn


def isProtein(seq):
    """Check if protein.

    Alphabet used is the 20-aa.
    Other characters will invalid the sequence.
    """
    pp = 1

    aset = [
        "A",
        "C",
        "G",
        "T",
        "R",
        "V",
        "W",
        "P",
        "F",
        "Q",
        "N",
        "Y",
        "H",
        "S",
        "I",
        "M",
        "D",
        "E",
        "L",
        "K",
        "X",
    ]

    for c in seq:

        if c not in aset:

            pp = 0

    return pp


def scan(searchInputName, hmm, hmmpath, jobid, searchOutputName):
    """Scan sequence with HMM"""

    # build hmmscan command
    hmmscan_exec = str(Path(HMMER_PATH, "hmmscan"))
    command = [
        hmmscan_exec,
        "--domtblout",
        searchOutputName,
        hmm,
        searchInputName,
    ]

    # run hmmscan
    p = sub.Popen(command, stdout=sub.PIPE, stderr=sub.PIPE)
    out, errors = p.communicate()

    # If there are errors stop the program
    if errors:
        # write errors
        write_error(f"Error with hmmscan: {errors}", jobid)

    # parse hmmscan output file
    score = readhmmscan(searchOutputName)

    return score


def get_germline(jobid, ig_database, chain, germfile):
    """Calculate the germline

    chain = path to the .fasta file of the desired chain
    germfile = path to the output of igblastp
    """
    igbplastp_exec = str(Path(IGBLAST_PATH, "igblastp"))
    command = [
        igbplastp_exec,
        "-germline_db_V",
        ig_database,
        "-query",
        jobid + chain,
        "-out",
        germfile,
    ]
    p = sub.Popen(command, stderr=sub.PIPE)
    out, errors = p.communicate()

    if errors:
        write_error(f"Error in running igblastp for {germfile}: {errors}", jobid)

    with open(germfile) as f:
        line = f.read().split("\n")
        # Raise an error if there are no hits from igblastp
        if "***** No hits found *****" in line:
            message = f"No hits found for: {germfile}"
            write_error(message, jobid)

        match = line[11].split("|")
        species = re.match("\w+", match[2]).group()
        germ = re.match("IG\wV\d+", match[1]).group()
        germ_spec = f"{germ}-{species}"

    return germ_spec


def align(searchInputName, hmm, hmmpath, jobid, alignOutputName):
    """Align sequence with HMM"""

    # hmmalign output file
    fhIn = open(alignOutputName, "w")
    # build hmmalign command
    hmmalign_exec = str(Path(HMMER_PATH, "hmmalign"))
    command = [hmmalign_exec, "--trim", hmm, searchInputName]

    # Run hmmalign
    p = sub.Popen(command, stdout=fhIn, stderr=sub.PIPE)
    out, errors = p.communicate()

    # If there are still errors stop the program
    if errors:
        # write errors
        write_error(f"Error with hmmalign: {errors}", jobid)

    # Parsing alignment file
    aligned = read_align(alignOutputName)

    fhIn.close()
    return aligned


def rmTmpFile(jobid):
    """Remove  file from tmp folder"""
    for f in os.listdir(jobid + "tmp/"):
        os.remove(jobid + "tmp/" + f)


def BothChains(session, jobid):
    """Check if input antibodies have both chains"""
    count = 0

    OutH = open(jobid + "heavy_format.fasta", "w")  # TODO to modify
    OutL = open(jobid + "light_format.fasta", "w")

    for key in session:

        count = count + 1

        if (session[key]["H"] and session[key]["L"]) or (
            session[key]["H"] and session[key]["K"]
        ):

            fhOut = open(jobid + "alignments/heavy_" + str(count) + ".fasta", "w")
            fhOut.write(">heavy" + "\n" + session[key]["H"] + "\n")
            fhOut.close()

            OutH.write(">" + key + "\n" + session[key]["H"].replace("-", "") + "\n")
            fhOut = open(jobid + "alignments/light_" + str(count) + ".fasta", "w")

            if session[key]["K"]:
                fhOut.write(">light" + "\n" + session[key]["K"] + "\n")
                OutL.write(">" + key + "\n" + session[key]["K"].replace("-", "") + "\n")
            else:
                fhOut.write(">light" + "\n" + session[key]["L"] + "\n")
                OutL.write(">" + key + "\n" + session[key]["L"].replace("-", "") + "\n")

            fhOut.close()

        else:

            if (
                not session[key]["L"]
                and not session[key]["K"]
                and not session[key]["H"]
            ):
                write_error("antibody missing both heavy and light chain", jobid)

            elif not session[key]["H"]:
                write_error("antibody is missing heavy chain", jobid)

            else:
                write_error("antibody missing light chain", jobid)

    OutH.close()
    OutL.close()

    return session


def write_error(message, jobid):
    """Open error.log write error and exit job"""
    with open(jobid + "error.log", "w") as fhErr:
        fhErr.write("{}\n".format(message))
    raise SystemExit("An error occurred. Check error.log file")


def write_warning(message, jobid):
    """Open warning.log and write message"""
    with open(jobid + "warnings.log", "a") as fhWar:
        fhWar.write("{}\n".format(message))


def checkInput(input, jobid):
    myheaders = []
    mysequences = []
    seq = ""
    flag = 0
    validChars = [
        "A",
        "C",
        "G",
        "T",
        "R",
        "V",
        "W",
        "P",
        "F",
        "Q",
        "N",
        "Y",
        "H",
        "S",
        "I",
        "M",
        "D",
        "E",
        "L",
        "K",
        "X",
    ]

    file_tocheck = os.path.join(jobid, input)

    # check if it is an empty file
    if os.stat(file_tocheck).st_size == 0:
        message = "File {} is empty. Please check your input".format(input)
        write_error(message, jobid)

    with open(file_tocheck) as fhIn:

        for line in fhIn:

            line = line.rstrip("\n")
            line = line.rstrip("\r")
            line = line.rstrip()

            # check if line is a header
            matchObj = re.match("(>\S+)", line)
            if matchObj:
                head = matchObj.group(1)
                myheaders.append(head)
                flag = 1
                if seq:
                    mysequences.append(seq)
                    seq = ""
            else:
                if flag:
                    line = line.upper()
                    seq = seq + line
                else:
                    message = "Missing header at the beginning of the {} file. Please check your input.".format(
                        input
                    )
                    write_error(message, jobid)

        if seq:
            mysequences.append(seq)

        # Check if something rather than an header is provided
        if len(mysequences) == 0:
            message = (
                "No sequence present in {} file. Please check your input file".format(
                    input
                )
            )
            write_error(message, jobid)

        # Check number of headers
        if len(myheaders) > 1:
            message = "More than one header present in {} file. Please check your input file".format(
                input
            )
            write_error(message, jobid)

        # check if line is only composed of alphabet characters
        for i in mysequences:
            violations = [char for char in i if char not in validChars]
            if len(violations) > 0:
                inval = " ".join(violations)
                message = (
                    "Invalid character(s) "
                    + inval
                    + " in sequence:\n "
                    + i
                    + "\nPlease check your input file"
                )
                write_error(message, jobid)


def oneLiner_fasta(jobid, fileIn, fileOut):
    with open(jobid + fileIn, "r") as fhIn:
        seq = ""
        header = ""
        # read input file
        for line in fhIn:
            # removing new line
            line = line.rstrip("\n")
            line = line.rstrip("\r")
            if line.startswith(">"):
                header = line
            else:
                # define header as a key unless already in mydict
                seq = seq + line.upper()

    # write file in jobpath
    with open(jobid + fileOut, "w") as fhOut:
        fhOut.write(header + "\n" + seq + "\n")
