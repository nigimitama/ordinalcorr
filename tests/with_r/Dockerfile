FROM rocker/r-ver:4.3.2

# setup python
RUN apt-get update
RUN apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install pytest numpy scipy pandas

# setup R
RUN Rscript -e "install.packages('polycor')"
RUN Rscript -e "install.packages('ltm')"

WORKDIR /
COPY . /

# install this package
RUN pip3 install .
