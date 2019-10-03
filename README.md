# proABC-2

It predicts the antibody residues that will make contact with the antigen and the type of interaction using a **convolutional neural network (CNN)**.

# Installation

The easiest way is using *Anaconda* (https://www.anaconda.com/distribution/).

``` bash
git clone https://github.com/haddocking/proABC-2.git
cd proABC-2
conda env create #Create a conda enviroment named proABC-2 with dependecies
```


# Usage

``` bash
cd proABC-2
conda activate proABC-2 #activate enviroment
python proABC.py <input folder> <heavy fasta file> <light fasta file> #run code
conda dectivate #deactivate enviroment

#Example:
python proABC.py Example heavy.fasta light.fasta
```
**proABC 2** also accepts the DNA sequences of the antibody chains and uses the *Biopython Seq module* (https://biopython.org/DIST/docs/api/Bio.Seq-module.html) for the translation into protein sequences.

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

**proABC-2** runs on **Python 3.6+** only.

Dependencies should be installed via ```conda``` using ```conda env create```
