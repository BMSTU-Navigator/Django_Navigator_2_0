#!/usr/bin/env bash

echo "install python"
apt-get install python3
apt-get install git

t = "./Django_Navigator_2_0"
if [ -d t ]; then
    if [ -L t ]; then
        rm t
    else
        rmdir t
    fi
fi

git clone https://github.com/BMSTU-Navigator/Django_Navigator_2_0.git
cd ./Django_Navigator_2_0

pip3 install -r requirements.txt

python3 manage.py runserver localhost:8000
