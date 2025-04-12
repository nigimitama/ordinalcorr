FROM rocker/r-ver:4.3.2

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    r-cran-polycor

# RUN pip3 install pandas scipy
RUN pip3 install scipy==1.9.0 semopy pandas

WORKDIR /
COPY . /
