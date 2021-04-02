#!/bin/bash
set -x

export PYTHONPATH=./..

sphinx-apidoc -o source/ "${PYTHONPATH}" -f -d 1
make gettext

for d in $(ls -d locales/*/ ); do
  lang="$( basename ${d})"
  sphinx-intl update -p build/gettext -l "$lang"
done