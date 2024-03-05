FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive
ENV FACESWAP_BACKEND cpu
ENV RESOURCE_PATH resources

RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN apt-get update -qq -y
RUN apt-get upgrade -y
RUN apt-get install -y gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
    python3 \
    python3-pip \
    python3-tk

RUN ln -s $(which python3) /usr/local/bin/python

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements/cpu.txt