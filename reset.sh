#!/bin/bash

# I really don't think this file works any more - it's rather outdated

CONTENT_DIR=/Users/david/Documents/MacTutor/actual-work/mathshistory-lektor/mathshistory/content/

# delete all except the root contents.lr (probably an index)
DIRS=("Chronology" "EMS" "Extras" "Glossary" "HistTopics" "Honours" "Map" "Obituaries" "Societies")
for dir in "${DIRS[@]}"
do
  mv "${CONTENT_DIR}${dir}/contents.lr" /tmp/contents.lr.tmp
  rm -r "${CONTENT_DIR}${dir}"
  mkdir "${CONTENT_DIR}${dir}"
  mv /tmp/contents.lr.tmp "${CONTENT_DIR}${dir}/contents.lr"
done

mkdir "${CONTENT_DIR}EMS/Zagier" # yes
cat <<EOF >> "${CONTENT_DIR}EMS/Zagier/contents.lr"
_model: indexes
---
_template: indexes.html
---
indexof: /EMS/Zagier
EOF

# delete (all contents.lr except the root index) but leave everything else
DIRS=("Biographies" "Curves" "Projects")
for dir in "${DIRS[@]}"
do
  mv "${CONTENT_DIR}${dir}/contents.lr" /tmp/contents.lr.tmp
  find "${CONTENT_DIR}${dir}/" -type f -name 'contents.lr' -exec rm {} +
  mv /tmp/contents.lr.tmp "${CONTENT_DIR}${dir}/contents.lr"
done

# delete all contents.lr but leave everything else
DIRS=("Strick" "Tait" "Wallace")
for dir in "${DIRS[@]}"
do
  find "${CONTENT_DIR}${dir}/" -type f -name 'contents.lr' -exec rm {} +
done

rm -r "${CONTENT_DIR}Ledermann/" #yes
rm -r "${CONTENT_DIR}Astronomy/" #yes

# ignore attachment stores:
  # Bookpages
  # BSHM
  # Diagrams
  # DNB
  # DSB
  # Publications
  # TimesObituaries
