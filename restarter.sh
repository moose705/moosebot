#!/bin/bash

myscript(){
    python3 main.py
}

until myscript; do
    echo "'MooseBot' crashed with exit code $?. Restarting..." >&2
    sleep 1
done