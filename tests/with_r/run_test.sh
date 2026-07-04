#!/bin/bash -eux

# copy source code to test/with_r directory
THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEST_DIR="$( cd "$( dirname "${THIS_DIR}" )" && pwd )"
PROJECT_ROOT_DIR="$( cd "$( dirname "${TEST_DIR}" )" && pwd )"
cp -r "$PROJECT_ROOT_DIR/ordinalcorr" $THIS_DIR
cp "$PROJECT_ROOT_DIR/pyproject.toml" $THIS_DIR
cp "$PROJECT_ROOT_DIR/README.md" $THIS_DIR

docker build -t test .

# run the R-vs-Python comparison tests (each test regenerates its own data and R results)
docker run -it --rm test bash -c "python3 -m pytest polychoric polyserial point_biserial hetcor -v"

rm -r "$THIS_DIR/ordinalcorr" "$THIS_DIR/pyproject.toml" "$THIS_DIR/README.md"
