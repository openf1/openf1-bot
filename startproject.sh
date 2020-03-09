#!/bin/bash
set -e

usage() {
    echo "\n  Usage:\n      ./startproject.sh <project name>\n"
}

if [ -z "$1" ]; then
    usage
    exit
fi

echo "Starting new project $1..."

cp -r template $1
if [ "$(uname)" == "Darwin" ]; then
    #alias sed='sed -i'
    find $1 -type f | xargs sed -i '' "s/template/$1/"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    find $1 -type f | xargs sed -i "s/template/$1/"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    find $1 -type f | xargs sed -i "s/template/$1/"
fi
mv $1/template $1/$1

echo "Project $1 created!"
