#!/bin/bash

echo "### Script to setup flask db migrate ###"

read -p "What's the name of the app? " varapp

export FLASK_APP=$varapp

flask db init

read -p "Make a comment for Flask DB Migrate: " varcomment

flask db migrate -m "$varcomment"

flask db upgrade

if [ $? -eq 0 ]
then 
    echo "Flask DB Migrate process successfully executed!!!"
else
    echo "Flask DB Migrate process failed!!!"
fi