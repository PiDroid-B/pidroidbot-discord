#!/bin/bash
#set -x

export PYTHONPATH=./..

sphinx-apidoc -o source/ "${PYTHONPATH}" -f -d 1
make gettext
sphinx-intl update -p build/gettext

for d in $(ls -d locales/*/ ); do
  lang="$( basename ${d})"
  for f in $(ls -d "${d}"/*/*.po ); do
    if ! grep -q "Language:" "${f}" ; then
      echo "Add Language to ${f}"
      awk '/Language-Team/ { print; print "\"Language: '${lang}'\\n\""; next }1' "${f}" > "${f}.tmp"
      mv "${f}.tmp" "${f}"
    fi
  done
done

#set -x
#
#export PYTHONPATH=./..
#
#sphinx-apidoc -o source/ "${PYTHONPATH}" -f -d 1
#make gettext
#
#for d in $(ls -d locales/*/ ); do
#  lang="$( basename ${d})"
#  sphinx-intl update -p build/gettext -l "$lang"
#done