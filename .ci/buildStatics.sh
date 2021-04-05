#!/bin/bash
set -x
################################################################################
# File:    buildBadges.sh
# Purpose: Script that builds some badges for static pages
#
# Authors: PiDroid-B
# Created: 2021-04-06
# Version: 0.1
################################################################################

TARGET_BRANCH="gh-statics"
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)

docroot=`mktemp -d`

git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"

pushd "${docroot}"

git init
git remote add deploy "https://token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
git checkout -b "${TARGET_BRANCH}"

touch .nojekyll

cat > i18n_cov.json <<EOF
{
  "schemaVersion": 1,
  "label": "i18n Coverage",
  "message": "$I18N_COV",
  "color": "orange"
}

EOF

cat > README.md <<EOF
# GitHub Badges

Nothing to see here.
Just a little space to stock some information

EOF

git add .

msg="Updating Badges for commit ${GITHUB_SHA} made on `date -d"@${SOURCE_DATE_EPOCH}" --iso-8601=seconds` from ${GITHUB_REF} by ${GITHUB_ACTOR}"
git commit -am "${msg}"

# overwrite the contents of the gh-pages branch on our github.com repo
git push deploy "${TARGET_BRANCH}" --force

popd # return to main repo sandbox root

# exit cleanly
exit 0