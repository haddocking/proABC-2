#==============================================================================================
FROM python:3.7 AS build

#------------------------------------------------------------------
# ProABC-2 uses uses stderr to check for errors for virtualization,
# some errors are printed to stderr and then proabc-2 fails.
# This is a workaround to avoid this.
ENV KMP_AFFINITY=noverbose
#------------------------------------------------------------------

# Install dependencies
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  build-essential \
  &&  \
  apt-get clean && rm -rf /var/lib/apt/lists/*

#------------------------------------------------------------------
# Install IGBLAST
WORKDIR /opt/software
RUN wget ftp://ftp.ncbi.nih.gov/blast/executables/igblast/release/1.14.0/ncbi-igblast-1.14.0-x64-linux.tar.gz && \
  tar -xvf ncbi-igblast-1.14.0-x64-linux.tar.gz

ENV IGBLAST_PATH=/opt/software/ncbi-igblast-1.14.0/bin
ENV IGDATA=/opt/software/ncbi-igblast-1.14.0

# Install HMMER
WORKDIR /opt/software
RUN wget http://eddylab.org/software/hmmer/hmmer.tar.gz && \
  tar zxf hmmer.tar.gz
WORKDIR /opt/software/hmmer-3.4

RUN ./configure --prefix=`pwd` && \
  make && \
  # make check && \
  make install && \
  (cd easel; make install)
ENV HMMER_PATH=/opt/software/hmmer-3.4/bin

# Install Poetry
RUN pip install --no-cache-dir poetry==1.5.1 \
  && poetry config virtualenvs.create false

#------------------------------------------------------------------
# Install proABC-2
WORKDIR /opt/software/proABC-2
COPY . .
RUN poetry install --only main

#==============================================================================================
FROM build AS prod

WORKDIR /data

ENTRYPOINT ["proabc2"]
#==============================================================================================

FROM build AS test

WORKDIR /opt/software/proABC-2

RUN poetry install

ENTRYPOINT [""]

#==============================================================================================

