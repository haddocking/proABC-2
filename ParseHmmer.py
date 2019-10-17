import re
import os


'''
These functions always return something. Control of the alignment will be performed later in the program.
In the meanwhile, if the input consists of multiple sequences the program will still run if one sequence
raise an error.
'''

''' parse the hmmsearch output '''

def readhmmsearch(file):

    evalue = 1

    ''' Check if file exists'''
    if not os.path.isfile(file):
        return (evalue)

    else:
        domains = 0
        handle = open(file, "r")
        for line in handle:
            if not line.startswith("#"):
                domains = domains + 1
                split = line.split()
                evalue = float(split[6])

        handle.close()
    ''' I check for the presence of multiple domains, only if the sequence has been recognized as an antibody'''
    #if evalue <= 10e-40:
        #if domains > 1:
            #evalue = False

    return (evalue)

''' parse the hmmalign output '''


''' Correct alingment does not present any dot in the GC RF line

4fp8_J         EVQLQESGGGLVQPGESLRLSCVGSGSSFGESTlsY----YAVSWVRQAPGKGLEWLSIINA-------GGGDIDYADSVEGRFTISRDNSKETLYLQMTNLRVEDTGVYYCAKHMSMQQVVSAGWERADLVGDAF------DVWGQGTMVTVSS
#=GR 4fp8_J PP 8**************************997765445....**********************.......*******************************************************************......************9
#=GC PP_cons   8**************************997765..5....**********************.......*******************************************************************......************9
#=GC RF        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx..xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

'''

def read_align(file):

    aligned = ""

    ''' Check if file exists'''
    if not os.path.isfile(file):
        return(aligned)

    else:
        handle = open(file, "r")

        for line in handle:
            ''' file '''

            if not line.startswith('#') and not line.startswith('\n') and not line.startswith('//'):
                split = line.split()
                aligned = aligned + split[1]
                '''Check if alignment failed'''

            elif re.match('\#\=GC RF', line):
                split = line.split()

                if re.search('\.', split[2]):
                    aligned =''
                    break

        handle.close()

    return (aligned)
