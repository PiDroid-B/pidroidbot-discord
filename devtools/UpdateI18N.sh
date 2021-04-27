#!/bin/bash
set -x

if [ "$(dirname "$0")" == "." ]; then
  pushd ..
elif [ "$(dirname "$0")" == "devtools" ]; then
  pushd .
else
  echo "Please go to the devtools' directory before run this script"
  exit 1
fi

pybabel extract -o locales/base.pot pidroidbot_discord/
pybabel update -i locales/base.pot -d locales

pushd docs/

export PYTHONPATH=..

#sphinx-apidoc -o source/ "${PYTHONPATH}" -f -d 1
make gettext
sphinx-intl update -p _build/gettext

for d in $(ls -d locales/*/ ); do
  lang="$( basename "${d}")"
  for f in $(ls -d "${d}"/*/*.po ); do
    if ! grep -q "Language:" "${f}" ; then
      echo "Add Language to ${f}"
      awk '/Language-Team/ { print; print "\"Language: '"${lang}"'\\n\""; next }1' "${f}" > "${f}.tmp"
      mv "${f}.tmp" "${f}"
    fi
  done
done

popd
popd
