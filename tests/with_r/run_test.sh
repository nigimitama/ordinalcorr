#!/bin/bash -eux
#
# Regenerate the R fixtures used by tests/test_r_comparison_*.py.
#
# This script only produces CSV files (input data and R's estimation
# results); it does not run or compare against the Python implementation.
# The pytest tests read the committed CSVs directly and do not need R or
# Docker to run. Re-run this script (and commit the resulting CSV changes)
# whenever the data-generation or R estimation logic changes.

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$THIS_DIR"

docker build -t ordinalcorr-r-fixtures .

# point biserial
docker run -it --rm \
    -v "$THIS_DIR/point_biserial:/point_biserial" \
    ordinalcorr-r-fixtures bash -c "
    cd point_biserial && \
    rm -rf data results_r.csv && \
    Rscript gen_data.R && \
    Rscript test.R
"

# polychoric
docker run -it --rm \
    -v "$THIS_DIR/polychoric:/polychoric" \
    ordinalcorr-r-fixtures bash -c "
    cd polychoric && \
    rm -rf data results_r.csv && \
    Rscript gen_data.R && \
    Rscript test.R
"

# polyserial
docker run -it --rm \
    -v "$THIS_DIR/polyserial:/polyserial" \
    ordinalcorr-r-fixtures bash -c "
    cd polyserial && \
    rm -rf data results_r.csv && \
    Rscript gen_data.R && \
    Rscript test.R
"

# hetcor
docker run -it --rm \
    -v "$THIS_DIR/hetcor:/hetcor" \
    ordinalcorr-r-fixtures bash -c "
    cd hetcor && \
    rm -rf data results_r.csv && \
    Rscript gen_data.R && \
    Rscript test.R
"
