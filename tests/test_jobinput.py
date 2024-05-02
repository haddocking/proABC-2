import os
from pathlib import Path

import pytest

import proabc_2.jobinput as ji
import proabc_2.numbering as nu

# Constants for file paths and isotypes
# jobid = 'Test_data/'
jobid = str(Path(Path(__file__).parent, "golden_data")) + "/"
hmmpath = ""
out_h = "heavy_test.fasta"
out_l = "light_test.fasta"


@pytest.fixture
def setup_environment():
    # Paths for input files
    file_h = "heavy.fasta"
    file_l = "light.fasta"

    # Create directories if not exists
    if not os.path.exists(os.path.join(jobid, "tmp")):
        os.makedirs(os.path.join(jobid, "tmp"))

    # Run processing functions
    ji.oneLiner_fasta(jobid, file_h, out_h)
    ji.oneLiner_fasta(jobid, file_l, out_l)

    yield

    # Cleanup
    for f in os.listdir(jobid + "tmp/"):
        os.remove(jobid + "tmp/" + f)
    os.rmdir(jobid + "tmp/")


def test_readInput(setup_environment):
    seq_h, isotype_h = ji.read_input_single(out_h, jobid, hmmpath)
    seq_l, isotype_l = ji.read_input_single(out_l, jobid, hmmpath)

    # Expected values
    golden_h = "EVQLVESGGGLVQPGGSLRLSCAASGYTFTN-------YGMNWVRQAPGKGLEWVGWINT-------YTGEPTYAADFKRRFTFSLDTSKSTAYLQMNSLRAEDTAVYYCAKYPHYYGSSHWYF----------------DVWGQGTLVTVSS"
    golden_l = "DIQMTQSPSSLSASVGDRVTITCSASQDIS----------NYLNWYQQKPGKAPKVLIYF--------TSSLHSGVPSRFSGSGSG--------TDFTLTISSLQPEDFATYYCQQYSTVP--------WTFGQGTKVEIKRTV"
    isotype_h = "H"
    isotype_l = "K"

    assert golden_h == seq_h, "Heavy chain is different"
    assert isotype_h == isotype_h, "Heavy chain isotype is different"
    assert golden_l == seq_l, "Light chain is different"
    assert isotype_l == isotype_l, "Light chain isotype is different"


def test_loopLen():
    golden_h = "EVQLVESGGGLVQPGGSLRLSCAASGYTFTN-------YGMNWVRQAPGKGLEWVGWINT-------YTGEPTYAADFKRRFTFSLDTSKSTAYLQMNSLRAEDTAVYYCAKYPHYYGSSHWYF----------------DVWGQGTLVTVSS"
    golden_l = "DIQMTQSPSSLSASVGDRVTITCSASQDIS----------NYLNWYQQKPGKAPKVLIYF--------TSSLHSGVPSRFSGSGSG--------TDFTLTISSLQPEDFATYYCQQYSTVP--------WTFGQGTKVEIKRTV"
    golden_l_l = "---ALTQPASVSGSPGQSITISCTGTSSDVGGY-------NYVSWYQQHPGKAPKLMIYG--------VTNRPSGVSNRFSGSKSG--------NTASLTISGLQAGDEADYYCSSYTSTRTP------YVFGTGTKV------"
    gold_len_h = [7, 4, 12]
    gold_len_l_k = [7, 3, 6]
    gold_len_l_l = [11, 3, 8]

    assert (
        list(nu.H(golden_h).loopLen().values()) == gold_len_h
    ), "Heavy chain loop lengths are different"
    assert (
        list(nu.K(golden_l).loopLen().values()) == gold_len_l_k
    ), "Light chain (K) loop lengths are different"
    assert (
        list(nu.L(golden_l_l).loopLen().values()) == gold_len_l_l
    ), "Light chain (L) loop lengths are different"


def test_getCs():
    golden_h = "EVQLVESGGGLVQPGGSLRLSCAASGYTFTN-------YGMNWVRQAPGKGLEWVGWINT-------YTGEPTYAADFKRRFTFSLDTSKSTAYLQMNSLRAEDTAVYYCAKYPHYYGSSHWYF----------------DVWGQGTLVTVSS"
    golden_l = "DIQMTQSPSSLSASVGDRVTITCSASQDIS----------NYLNWYQQKPGKAPKVLIYF--------TSSLHSGVPSRFSGSGSG--------TDFTLTISSLQPEDFATYYCQQYSTVP--------WTFGQGTKVEIKRTV"
    golden_l_l = "---ALTQPASVSGSPGQSITISCTGTSSDVGGY-------NYVSWYQQHPGKAPKLMIYG--------VTNRPSGVSNRFSGSKSG--------NTASLTISGLQAGDEADYYCSSYTSTRTP------YVFGTGTKV------"
    golden_cs_h = [1, 2, "bulged"]
    golden_cs_k = [2, 1, 1]
    golden_cs_l = [6, 1, 1]

    assert (
        nu.H(golden_h).getCs() == golden_cs_h
    ), "Heavy chain canonical structures are different"
    assert (
        nu.K(golden_l).getCs() == golden_cs_k
    ), "Light chain (K) canonical structures are different"
    assert (
        nu.L(golden_l_l).getCs() == golden_cs_l
    ), "Light chain (L) canonical structures are different"
