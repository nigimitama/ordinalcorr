#!/bin/bash -eux

# copy source code to test/with_r directory
THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEST_DIR="$( cd "$( dirname "${THIS_DIR}" )" && pwd )"
PROJECT_ROOT_DIR="$( cd "$( dirname "${TEST_DIR}" )" && pwd )"
cp -r "$PROJECT_ROOT_DIR/ordinalcorr" $THIS_DIR
cp "$PROJECT_ROOT_DIR/pyproject.toml" $THIS_DIR
cp "$PROJECT_ROOT_DIR/README.md" $THIS_DIR

docker build -t test .

# polychoric
docker run -it --rm test bash -c "
    cd polychoric && \
    python3 -u gen_data.py && \
    Rscript test.R && \
    python3 -u test.py && \
    python3 -u compare.py
" 

# polyserial
docker run -it --rm test bash -c "
    cd polyserial && \
    python3 -u gen_data.py && \
    Rscript test.R && \
    python3 -u test.py && \
    python3 -u compare.py
" 


rm -r "$THIS_DIR/ordinalcorr" "$THIS_DIR/pyproject.toml" "$THIS_DIR/README.md"
