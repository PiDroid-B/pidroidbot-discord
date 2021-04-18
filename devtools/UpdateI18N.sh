#!/bin/bash
set -x

dir_before=`mktemp -d`
dir_after=`mktemp -d`

mkdir -p "$dir_before"/locales/
rsync -vr -f '+ *.po' -f '+ **/' -f '- *' --prune-empty-dirs locales/. "$dir_before"/locales/
mkdir -p "$dir_before"/docs/locales/
rsync -vr -f '+ *.po' -f '+ **/' -f '- *' --prune-empty-dirs docs/locales/. "$dir_before"/docs/locales/

pushd devtools/
bash UpdateI18N.sh
popd

mkdir -p "$dir_after"/locales/
rsync -vr -f '+ *.po' -f '+ **/' -f '- *' --prune-empty-dirs locales/. "$dir_after"/locales/
mkdir -p "$dir_after"/docs/locales/
rsync -vr -f '+ *.po' -f '+ **/' -f '- *' --prune-empty-dirs docs/locales/. "$dir_after"/docs/locales/

git diff --check $dir_before/ $dir_after/ || {
  echo "i18n require an update, please run devtools/updateI18N.sh"
  exit 1
}
(environment) root@8e032461f1b7:/tmp/pidroidbot-discord# cat devtools/UpdateI18N.sh
#!/bin/bash

[ "$(dirname "$0")" != "." ] && {
  echo "Please go to the devtools' directory before run this script"
  exit 1
}

pushd ..

pybabel extract -o locales/base.pot pidroidbot_discord/
pybabel update -i locales/base.pot -d locales

pushd docs/

export PYTHONPATH=..

#sphinx-apidoc -o source/ "${PYTHONPATH}" -f -d 1
make gettext
sphinx-intl update -p _build/gettext

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

popd
popd
