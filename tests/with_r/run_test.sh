#!/bin/bash -eux

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEST_DIR="$( cd "$( dirname "${THIS_DIR}" )" && pwd )"
PROJECT_ROOT_DIR="$( cd "$( dirname "${TEST_DIR}" )" && pwd )"

cp -r "$PROJECT_ROOT_DIR/ordinalcorr" "$THIS_DIR/ordinalcorr"

docker build -t test .
docker run -it --rm test bash -c "
    python3 -u gen_data.py && \
    Rscript test.R && \
    python3 -u test.py && \
    python3 -u compare.py
" 

rm -r "$THIS_DIR/ordinalcorr"
