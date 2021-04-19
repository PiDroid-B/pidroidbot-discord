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

for f in $( find $dir_before -type f -name "*.po" ) ; do
  sed -i 's/"POT-Creation-Date.*$//' "${f}"
done

for f in $( find $dir_after -type f -name "*.po" ) ; do
  sed -i 's/"POT-Creation-Date.*$//' "${f}"
done

git diff --check $dir_before/ $dir_after/ || {
  echo "i18n require an update, please run devtools/updateI18N.sh"
  exit 1
}
