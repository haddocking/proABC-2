#==============================================================================================
FROM continuumio/anaconda3:2022.10 AS build

ENV LC_ALL=C
ENV LC_NUMERIC=en_GB.UTF-8

#------------------------------------------------------------------
# ProABC-2 uses uses stderr to check for errors for virtualization,
# some errors are printed to stderr and then proabc-2 fails.
# This is a workaround to avoid this.
ENV KMP_AFFINITY=noverbose
#------------------------------------------------------------------

# Install dependencies
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  hmmer>=3.3.2+dfsg-1 \
  curl>=7.74.0-1.3+deb11u3 \
  git>=1:2.30.2-1 \
  libxml2>=2.9.10+dfsg-6.7+deb11u3 \
  &&  \
  apt-get clean && rm -rf /var/lib/apt/lists/*

#------------------------------------------------------------------
# Proabc-2 has a very complex dependency tree, use libmamba to solve it faster
#  - the time to install it pays off later!
# RUN conda install -n base conda-libmamba-solver

#------------------------------------------------------------------
# Install igblast
WORKDIR /opt/software
RUN curl \
  -o ncbi-igblast-1.14.0-x64-linux.tar.gz \
  -s ftp://ftp.ncbi.nih.gov/blast/executables/igblast/release/1.14.0/ncbi-igblast-1.14.0-x64-linux.tar.gz && \
  tar xzf ncbi-igblast-1.14.0-x64-linux.tar.gz && \
  rm ncbi-igblast-1.14.0-x64-linux.tar.gz

ENV PATH=$PATH:/opt/software/ncbi-igblast-1.14.0/bin
ENV IGDATA=/opt/software/ncbi-igblast-1.14.0

#------------------------------------------------------------------
# Install proABC-2
WORKDIR /opt/software/proABC-2
COPY . .

RUN conda env create

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "proABC-2", "/bin/bash", "-c"]

#------------------------------------------------------------------
# Setup proABC-2
WORKDIR /data

ENTRYPOINT ["conda", "run", "-n", "proABC-2", "python", "/opt/software/proABC-2/proABC.py"]
#==============================================================================================

FROM build AS test

RUN conda run -n proABC-2 pip install pytest coverage pytest pytest-cov hypothesis

WORKDIR /opt/software/proABC-2

ENTRYPOINT []

#==============================================================================================
