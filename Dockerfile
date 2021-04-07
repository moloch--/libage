FROM golang:latest

RUN apt-get update --fix-missing && apt-get -y install \
  git build-essential python3


RUN mkdir -p /opt/libage
ADD . /opt/libage
WORKDIR /opt/libage
RUN make


WORKDIR /opt/libage/src/age
RUN chmod +x ./age.py

# Test with ed25519
RUN ssh-keygen -t ed25519 -f ./id_ed25519
RUN echo "hello world" > ./plaintext.txt
RUN ./age.py ./id_ed25519.pub ./plaintext.txt

# Test with RSA
RUN ssh-keygen -t rsa -b 4096 -f ./id_rsa
RUN echo "hello world" > ./plaintext.txt
RUN ./age.py ./id_rsa.pub ./plaintext.txt
