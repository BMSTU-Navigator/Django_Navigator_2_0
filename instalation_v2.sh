#!/usr/bin/env bash

echo "cd django dir"

cd ./Django_Navigator_2_0
echo "pull from git"
`git pull`
echo "run django"

`python3 manage.py runserver localhost:8000`
