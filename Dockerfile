FROM golang:latest

#
# This Dockerfile is mostly for using unit tests
#

RUN apt-get update --fix-missing && apt-get -y install \
  git build-essential python3


RUN mkdir -p /opt/libage
ADD . /opt/libage
WORKDIR /opt/libage
RUN make

RUN ssh-keygen -t ed25519 -f ./id_ed25519
RUN ssh-keygen -t rsa -b 4096 -f ./id_rsa
RUN cat id_ed25519
RUN cat id_ed25519.pub
RUN cat id_rsa
RUN cat id_rsa.pub

WORKDIR /opt/libage
RUN python3 -m unittest discover src

