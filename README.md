# proABC-2

![PyPI - License](https://img.shields.io/pypi/l/proabc-2)
![PyPI - Status](https://img.shields.io/pypi/status/proabc-2)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/proabc-2)
[![ci](https://github.com/haddocking/proABC-2/actions/workflows/ci.yml/badge.svg)](https://github.com/haddocking/proABC-2/actions/workflows/ci.yml)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ce83248d0f1f47ff96e0bc7656c83514)](https://app.codacy.com/gh/haddocking/proABC-2/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/ce83248d0f1f47ff96e0bc7656c83514)](https://app.codacy.com/gh/haddocking/proABC-2/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B%20%20%E2%97%8F-yellow)](https://fair-software.eu)

![proabc2 logo](https://raw.githubusercontent.com/haddocking/proABC-2/main/logo/logo.png)

Predicts the antibody residues that will make contact with the antigen and the type of interaction using a Convolutional Neural Network (CNN).

## Installation

proABC-2 is available both locally as a python package and as a Docker container. See below instructions for each case.

### Docker

The docker image is available on the Github Container Registry and can be pulled using the following command:

```bash
docker pull ghcr.io/haddocking/proabc-2:latest
```

### Local

> proABC-2 has some [third-party](THIRD_PARTY.md) dependencies that must be installed before running the software.

proABC-2 is available on PyPI and can be installed using pip using Python3.7:

```text
pip install proabc-2
```

It also depends on two third-party software, HMMER and IGBLAST, check the [third-party](THIRD_PARTY.md) section for more information.

## Example (Local and Docker)

Set up the data to run the example:

- Create a folder named `proabc2-prediction` in the root directory.

```bash
mkdir proabc2-prediction
```

- Create a heavy and light fasta file **inside** `proabc2-prediction` with the following content:

```text
echo ">APDB_H\nEVQLVESGGGLVQPGGSLRLSCAASGYTFTNYGMNWVRQAPGKGLEWVGWINTYTGEPTYAADFKRRFTFSLDTSKSTAYLQMNSLRAEDTAVYYCAKYPHYYGSSHWYFDVWGQGTLVTVSS" > proabc2-prediction/heavy.fasta
```

```text
echo ">APDB_L\nDIQMTQSPSSLSASVGDRVTITCSASQDISNYLNWYQQKPGKAPKVLIYFTSSLHSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQYSTVPWTFGQGTKVEIKRTV" > proabc2-prediction/light.fasta
```

### Execution (Docker)

```bash
docker run \
  --rm \
  --user $(id -u):$(id -g) \
  -v `pwd`:/data \
  ghcr.io/haddocking/proabc-2:latest \
  proabc2-prediction/ heavy.fasta light.fasta
```

### Execution (Local)

```text
proabc2 proabc2-prediction/ heavy.fasta light.fasta
```

### Results

The output will be in the same folder as the input files, named as `heavy-pred.csv` and `light-pred.csv`.

They consist of several columns:

- **Chothia**: position of the residue according to the Chothia numbering scheme
- **Sequence**: residue type for each position
- **pt**: probability of making a general interaction with the antigen
- **hb**: probability of making a hydrogen bonds with the antigen
- **hy**: probability of making a hydrophobic interaction with the antigen

| Chothia | Sequence |  pt  |  hb  |  hy  |
| :-----: | :------: | :--: | :--: | :--: |
|    1    |    E     | 0.23 | 0.17 | 0.24 |
|    2    |    V     | 0.23 | 0.15 | 0.23 |
|    3    |    Q     | 0.14 | 0.14 | 0.16 |
|   ...   |   ...    | ...  | ...  | ...  |

```bash
$ head proabc2-prediction/*pred.csv
==> proabc2-prediction/heavy-pred.csv <==
,Chothia,Sequence,pt,hb,hy
0,1,E,0.24,0.18,0.24
1,2,V,0.25,0.15,0.25
2,3,Q,0.16,0.16,0.17
3,4,L,0.14,0.14,0.17
4,5,V,0.14,0.15,0.15
5,6,E,0.16,0.16,0.16
6,7,S,0.14,0.16,0.13
7,8,G,0.17,0.13,0.16
8,9,G,0.14,0.14,0.15

==> proabc2-prediction/light-pred.csv <==
,Chothia,Sequence,pt,hb,hy
0,1,D,0.25,0.18,0.2
1,2,I,0.23,0.15,0.2
2,3,Q,0.15,0.16,0.17
3,4,M,0.15,0.14,0.15
4,5,T,0.16,0.15,0.16
5,6,Q,0.15,0.16,0.14
6,7,S,0.15,0.14,0.12
7,8,P,0.15,0.14,0.13
8,9,S,0.14,0.14,0.14
```

**proABC-2** also accepts the DNA sequences of the antibody chains and uses the [_Biopython Seq module_](https://biopython.org/DIST/docs/api/Bio.Seq-module.html) for the translation into protein sequences.

## Citation

- F. Ambrosetti, T.H. Olsen, P.P. Olimpieri, B. Jiménez-García, E. Milanetti, P. Marcatilli, A.M.J.J. Bonvin. ["proABC-2: PRediction Of AntiBody Contacts v2 and its application to information-driven docking"](https://doi.org/10.1093/bioinformatics/btaa644), _Bioinformatics_, , btaa644,
