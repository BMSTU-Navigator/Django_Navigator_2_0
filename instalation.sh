#!/usr/bin/env bash

#sudo -s
#apt-get install python3
#t as a variable of dir path
if [ -d t ]; then
    if [ -L t ]; then
        rm t
    else
        rmdir t
    fi
fi

#git clone command
#cd git dir

#sudo pip3 install -r requirements.txt

#python3 manage.py runserver localhost:8000
