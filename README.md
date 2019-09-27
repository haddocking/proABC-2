[![codecov](https://codecov.io/gh/Francesco03/ParaNet/branch/master/graph/badge.svg?token=i6iY65xa32)](https://codecov.io/gh/Francesco03/ParaNet) [![Build Status](https://travis-ci.com/Francesco03/ParaNet.svg?token=Y28CupxHnupoqQHW4Vse&branch=master)](https://travis-ci.com/Francesco03/ParaNet)
# ParaNet

It predicts the antibody residues that will make contact with the antigen and the type of interaction using a **convolutional neural network (CNN)**.

# Installation

The easiest way is using anaconda (https://www.anaconda.com/distribution/).

``` bash
git clone https://github.com/Francesco03/ParaNet.git
cd ParaNet
conda env create #Create a conda enviroment named ParaNet with dependecies
```


# Usage

``` bash
cd ParaNet
conda activate ParaNet #activate enviroment
python ParaNet.py <input folder> <heavy fasta file> <light fasta file> #run code
conda dectivate #deactivate enviroment

#Example:
python ParaNet.py Example heavy.fasta light.fasta
```

# Output

It returns 2 .csv files: **heavy-pred.csv** and **light-pred.csv** (inside the <*input folder*>) respectively for the heavy and the light antibody chains. 
They consist of  several columns: 

* Chothia: position of the residue according to the Chothia numbering scheme
* Sequence: residue type for each position 
* pt_pred: probability of making an interaction with the antigen
* hb_pred: probability of making a hydrogen bonds with the antigen
* hy_pred: probability of making a hydrophobic interaction with the antigen

| Chothia | Sequence | pt_pred | hb_pred | hy_pred | 
|:-------:|:--------:|:-------:|:-------:|:-------:|
| 1       | E        | 0.23    | 0.17    | 0.24    | 
| 2       | V        | 0.23    | 0.15    | 0.23    | 
| 3       | Q        | 0.14    | 0.14    | 0.16    | 
| ...     | ...      | ...     | ...     | ...     | 


# Requirements

ParaNet runs on **Python 3.6+** only.

Dependencies should be installed via ```conda``` using ```conda env create```
