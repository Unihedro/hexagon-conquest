#! /usr/bin/env bash
set -e 

if ! hash virtualenv 2>/dev/null; then
    echo "install virtualenv from pip."
else

    if [ ! -d ".env"  ]; then
        echo "virtualenv not found"
        echo "Initialising in directory .env"
        virtualenv .env
    fi

    source .env/bin/activate
    echo "Installing dependencies..."
    pip3 install -r requirements.txt

fi
