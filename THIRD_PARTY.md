## HMMER

```text
wget http://eddylab.org/software/hmmer/hmmer.tar.gz
tar zxf hmmer.tar.gz
cd hmmer-3.4
./configure --prefix=`pwd`
make
make check
make install
(cd easel; make install)
export HMMER_PATH=`pwd`/bin
```

## IGBLAST

```text
wget ftp://ftp.ncbi.nih.gov/blast/executables/igblast/release/1.14.0/ncbi-igblast-1.14.0-x64-linux.tar.gz
tar -xvf ncbi-igblast-1.14.0-x64-linux.tar.gz
export IGBLAST_PATH=`pwd`/ncbi-igblast-1.14.0/bin
export IGDATA=`pwd`/ncbi-igblast-1.14.0
```
