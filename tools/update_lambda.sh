#!/bin/bash

tempzip=$(mktemp)
git archive --format=zip --output=$tempzip "$1"
tempdir=$(mktemp -d)
cd $tempdir
unzip -qq $tempzip
chmod -R ugo+r .
find . -type f | zip $tempzip -@
cd -
rm -r $tempdir
aws lambda update-function-code --function-name tapl_interpret --zip-file fileb://$tempzip
rm $tempzip
