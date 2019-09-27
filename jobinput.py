import subprocess as sub
import string
import sys
import re
import os
from ParseHmmer import readhmmsearch, read_align
from Bio.Seq import Seq


def read_input_single(file, jobid, hmmpath, TargetName):
    """Read input file. Check if sequence is a protein or a nucleotide. Scan and align the sequences.
    Return a dictionary with sequence header as key and heavy and light chain as sequences.
    """
    invalidChars = string.punctuation
    thr = float(10e-40)
    aligned = ''
    isotype = ''
    message = []
    handle = open(jobid + file, "r")
    # can be heavy or light
    header = ''

    for line in handle:
        line = line.rstrip("\n")
        line = line.rstrip('\r')
        line = line.rstrip()
        matchObj1 = re.match(">", line)
        if matchObj1:
            header = line.replace('>', '')

        else:

            if any(char in invalidChars for char in line):
                write_error('Not allowed characters in ' + file[0:5] + ' chain. Please check your input file\n', jobid)

            if isDNA(line):

                line = Seq(line.replace("\n", ""))
                # Translate sequence using biopython
                line = str(line.translate())
                line = line.replace('*', '')
                # check if translated sequence has strange amino acid inside
                if not isProtein(line):
                    write_error(header + " includes unknown amino acids. Please check your sequence\n", jobid)

            else:
                # check if sequence is protein
                if not isProtein(line.replace("\n", "")):
                    write_error(header + " includes unknown amino acids. Please check your sequence\n", jobid)

            searchInputName = os.path.join(jobid, "tmp", "search.fasta")
            searchOutputName = os.path.join(jobid, "tmp", "scan.txt")
            alignOutputName = os.path.join(jobid, "tmp", "align.ali")

            fh = open(searchInputName, "w")
            fh.write(">" + header + "\n" + line + '\n')
            fh.close()

            # Calculate HMMER paths
            base_dir = os.path.dirname(__file__)
            heavy_hmm = os.path.join(base_dir, "MarkovModels/HEAVY.hmm")
            kapp_hmm = os.path.join(base_dir, "MarkovModels/KAPPA.hmm")
            lambda_hmm = os.path.join(base_dir, "MarkovModels/LAMBDA.hmm")

            evalueH = float(scan(searchInputName, heavy_hmm, hmmpath, jobid, searchOutputName))
            evalueK = float(scan(searchInputName, kapp_hmm, hmmpath, jobid, searchOutputName))
            evalueL = float(scan(searchInputName, lambda_hmm, hmmpath, jobid, searchOutputName))

            # more than one domain found in the input sequence. HMM failed to align sequence
            if not evalueH:
                message = 'Alignment failed for chain H:\n' + line + '\n'
                write_error(message, jobid)

            if not evalueK:
                message = 'Alignment failed for chain L:\n' + line + '\n'
                write_error(message, jobid)

            if not evalueL:
                message = 'Alignment failed for chain L:\n' + line + '\n'
                write_error(message, jobid)

            if (evalueH > thr) and (evalueK > thr) and (evalueL > thr):

                message.append('Your input sequence has not been recognized as an antibody. Please check your input:')
                message.append(line)
                message.append(header)

            if (evalueH < thr and evalueK < thr) or (evalueH < thr and evalueL < thr):
                message.append('Single chain antibody found. Please provide heavy and light chain as separate sequences.')
                message.append(line)
                message.append(header)
            
            # identify isotype
            if evalueH < thr:

                if file == 'light_format.fasta':
                    warn = "Heavy chain found when light expected."
                    write_warning(warn, jobid)

                aligned = align(searchInputName, heavy_hmm, hmmpath, jobid, alignOutputName, TargetName, header)
                if not aligned:
                    message = 'Alignment failed for chain H:\n' + line + '\n'
                    write_error(message, jobid)
                isotype = 'H'

            if (evalueK < evalueL) and (evalueK < thr):
                if file == 'heavy_format.fasta':
                    warn = "Kappa chain found when heavy expected."
                    write_warning(warn, jobid)
                aligned = align(searchInputName, kapp_hmm, hmmpath, jobid, alignOutputName, TargetName, header)
                if not aligned:
                    message = 'Alignment failed for chain L:\n' + line + '\n'
                    write_error(message, jobid)
                isotype = 'K'

            if (evalueL < evalueK) and (evalueL < thr):
                if file == 'heavy_format.fasta':
                    warn = "Lambda chain found when heavy expected."
                    write_warning(warn, jobid)
                aligned = align(searchInputName, lambda_hmm, hmmpath, jobid, alignOutputName, TargetName, header)
                if not aligned:
                    message = 'Alignment failed for chain L:\n' + line + '\n'
                    write_error(message, jobid)
                isotype = 'L'

    handle.close()
    return (aligned, isotype, message)


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

    return (nn)


def isProtein(seq):
    """Check if protein. 

    Alphabet used is the 20-aa.
    Other characters will invalid the sequence.
    """
    pp = 1

    aset = ["A", "C", "G", "T", "R", "V", "W", "P", "F", "Q", "N", "Y", "H", "S", "I", "M", "D", "E", "L", "K", "X"]

    for c in seq:

        if c not in aset:

            pp = 0

    return (pp)


def scan(searchInputName, hmm, hmmpath, jobid, searchOutputName):
    """Scan sequence with HMM"""

    # run hmmsearch exacutable
    command = [hmmpath + 'hmmscan', '--domtblout', searchOutputName, hmm, searchInputName]

    # run hmmscan
    p = sub.Popen(command, stdout=sub.PIPE, stderr=sub.PIPE)
    out, errors = p.communicate()

    if errors:
        # write errors
        write_warning(errors, jobid)

    # parse hmmsearch output file
    score = readhmmsearch(searchOutputName)

    return(score)


def get_germline(jobid, ig_database, chain, germfile):
    """Calculate the germline
    
    chain = path to the .fasta file of the desired chain
    germfile = path to the output of igblastp
    """
    command = ['igblastp', '-germline_db_V', ig_database, '-query', jobid + chain, '-out', germfile]
    p = sub.Popen(command, stderr=sub.PIPE)
    out, errors = p.communicate()

    if errors:
        write_error('Error in calculating the germline of {}'.format(germfile) , jobid)
        for error in errors:
            write_error(error, jobid)

    with open(germfile) as f:
        line = f.read().split('\n')[11].split('|')
        species = re.match('\w+', line[2]).group()
        germ = re.match("IG\wV\d+", line[1]).group()
        germ_spec = germ + '-' + species

    return(germ_spec)


def align(searchInputName, hmm, hmmpath, jobid, alignOutputName, TargetName, header):
    """Align sequence with HMM"""

    # hmmalign output file
    fhIn = open(alignOutputName, 'w')
    # run hmmalign
    command = [hmmpath + 'hmmalign', '--trim', hmm, searchInputName]

    p = sub.Popen(command, stdout=fhIn, stderr=sub.PIPE)
    out, errors = p.communicate()

    if errors:
        # write errors
        write_warning(errors, jobid)

    # Parsing alignment file
    aligned = read_align(alignOutputName, TargetName, jobid)

    fhIn.close()
    return (aligned)


def rmTmpFile(jobid):
    """Remove  file from tmp folder"""
    for f in os.listdir(jobid + 'tmp/'):
        os.remove(jobid + 'tmp/' + f)


def BothChains(session, jobid):
    """Check if input antibodies have both chains"""
    count = 0

    OutH = open(jobid + 'heavy_format.fasta', 'w')
    OutL = open(jobid + 'light_format.fasta', 'w')

    for key in session:

        count = count + 1
        TargetName = jobid.replace("../jobs/","")
        TargetName = TargetName.replace("/", "_") + str(count)

        if (session[key]['H'] and session[key]['L']) or (session[key]['H'] and session[key]['K']):

            fhOut = open(jobid + 'alignments/heavy_' + str(count) + '.fasta', 'w')
            fhOut.write(">heavy" + "\n" + session[key]['H'] + '\n')
            fhOut.close()

            OutH.write('>' + key + '\n' + session[key]['H'].replace('-','')+ '\n')
            fhOut = open(jobid + 'alignments/light_' + str(count) + '.fasta', 'w')

            if session[key]['K']:
                fhOut.write(">light" + "\n" + session[key]['K'] + '\n')
                OutL.write('>' + key + '\n' + session[key]['K'].replace('-','') + '\n')
            else:
                fhOut.write(">light" + "\n" + session[key]['L'] + '\n')
                OutL.write('>' + key + '\n' + session[key]['L'].replace('-','') + '\n')

            fhOut.close()

        else:

            if not session[key]['L'] and not session[key]['K'] and not session[key]['H']:
                write_error('antibody missing both heavy and light chain.\n', jobid)

            elif not session[key]['H']:
                write_error('antibody is missing heavy chain.\n', jobid)

            else:
                write_error('antibody missing light chain.\n', jobid)

    OutH.close()
    OutL.close()

    return(session)


def writeMessage(message, message2, jobid):
    if message:
        if message2:
            if message2[2] in ['light','heavy'] or message[2] in ['light','heavy']:
                error = message[0] + '\n' + message[1] + '\n' + message2[1]+'\n'
                write_error(error,jobid)
            else:
                error = message[0] + '\n' +message[2] +'\n' + message[1] + '\n'+message2[2] +'\n'  + message2[1]+'\n'
                write_error(error, jobid)
        else:
            if message[2] in ['light', 'heavy']:
                error = message[0] + '\n' + message[1] + '\n'
                write_error(error, jobid)
            else:
                error = message[0] + '\n' +message[2] + '\n' +  message[1] + '\n'
                write_error(error, jobid)
    elif message2:
        if message2[2] in ['light', 'heavy']:
            error = message2[0] + '\n' + message2[1]
            write_error(error, jobid)
        else:
            error = message2[0] + '\n' + message2[2] + '\n' + message2[1] + '\n'
            write_error(error, jobid)


def write_error(message, jobid):
    """Open error.log write error and exit job"""
    with open(jobid + 'error.log', 'w') as fhErr:
        fhErr.write('{}\n'.format(message))


def write_warning(message, jobid):
    """Open warning.log and write message"""
    with open(jobid + 'error.log', 'a') as fhWar:
        fhWar.write(message.decode('utf-8'))


def checkInput(input, jobid):
    myheaders = []
    mysequences = []
    seq = ''
    flag = 0
    validChars = ["A", "C", "G", "T", "R", "V", "W", "P", "F", "Q", "N", 
                  "Y", "H", "S", "I", "M", "D", "E", "L", "K", "X"]

    # check if input file exists
    if os.path.isfile(jobid + input):

        with open(jobid + input) as fhIn:

            for line in fhIn:

                line = line.rstrip('\n')
                line = line.rstrip('\r')
                line = line.rstrip()
                # if line not blank
                if line:
                    # check if line is a header
                    matchObj = re.match("(>\S+)", line)

                    if matchObj:
                        head = matchObj.group(1)
                        myheaders.append(head)
                        flag =1
                        if seq:
                            mysequences.append(seq)
                            seq = ''

                        # check if line is only composed of alphabet characters
                    else:
                        if flag:
                            line=line.upper()
                            seq = seq + line
                        else:
                            message = 'Missing header at the beginning of the input file. Please check your sequence\n'
                            write_error(message, jobid)
            if seq:
                mysequences.append(seq)

            if len(myheaders) != len(mysequences):
                message = 'Different number of headers and sequences. Please check your input file.\n'
                write_error(message, jobid)

            if len(myheaders) > 1:
                message = 'More than one header present in ' + input + ' file. Please check your input file\n'
                write_error(message, jobid)
            
            if len(mysequences) > 1:
                message = 'More than one sequences present in ' + input + ' file. Please check your input file\n'
                write_error(message, jobid)

            for i in mysequences:
                violations = [char for char in i if char not in validChars]
                if len(violations) > 0:
                    inval = " ".join(violations)
                    message = 'Invalid character(s) ' + inval + ' in sequence:\n ' + i + '\nPlease check your input file.'
                    write_error(message, jobid)


def oneLiner_fasta(jobid, fileIn, fileOut):
    with open(jobid + fileIn, 'r') as fhIn:
        seq = ''
        header= ''
        # read input file
        for line in fhIn:
            # removing new line
            line = line.rstrip('\n')
            line = line.rstrip('\r')
            if line.startswith(">"):
                header = line
            else:
                # define header as a key unless already in mydict
                seq =seq + line.upper()

    # write file in jobpath
    with open(jobid + fileOut,'w') as fhOut:
        fhOut.write(header + "\n" + seq + '\n')
