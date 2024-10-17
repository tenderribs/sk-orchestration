#!/bin/bash

pip install -r /workspace/requirements.txt

sleep 30

while true; do
    echo "Fetching INNET data"
    python3 /workspace/innet-pull.py

    sleep 600 # wait 10 minutes
done
