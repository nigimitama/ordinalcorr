FROM rocker/r-ver:4.3.2

# setup R packages
RUN Rscript -e "install.packages(c('MASS', 'polycor'))"

WORKDIR /
COPY . /
