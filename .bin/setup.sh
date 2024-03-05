#!/bin/sh

echo "set environment variables"

echo "building the environment for the project"
apt-get update -qq -y
apt-get upgrade -y
apt-get install -y gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
    python3 \
    python3-pip \
    python3-tk

ln -s $(which python3) /usr/local/bin/python

echo "install package"
pip install --upgrade pip
pip install --no-cache-dir -r requirements_nvidia.txt

export DEBIAN_FRONTEND=noninteractive
export FACESWAP_BACKEND=nvidia
export RESOURCE_PATH=resources