FROM rocker/r-ver:4.3.2

# setup python
RUN apt-get update
RUN apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install scipy==1.9.0 semopy pandas

# setup R
RUN Rscript -e "install.packages('polycor')"
RUN Rscript -e "install.packages('psych')"

WORKDIR /
COPY . /

# install this package
RUN pip3 install .
