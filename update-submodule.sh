#!/bin/bash

# read
while read LINE
do
    echo $LINE
    (cd ./$LINE && git checkout master && git add . && git commit -m "jiaoben" && git push)
done <  /Users/mac/Desktop/ucloud-documents-overall/study-git-submodule-dirs

