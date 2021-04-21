#!/bin/bash
set -e
PYPATH="$1"
FILEPATH="$2"
PRJPATH="$3"

pushd "${PRJPATH}"

echo "### BLACK ###"
"${PYPATH}"/black "${FILEPATH}"
echo "### ISORT ###"
"${PYPATH}"/isort "${FILEPATH}"
echo "### FLAKE8 ###"
"${PYPATH}"/flake8 "${FILEPATH}"

popd

set +e