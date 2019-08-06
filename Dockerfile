FROM ubuntu:latest
MAINTAINER Eduardo Bezerra "ebezerra@cefet-rj.br"

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip  

RUN git clone https://github.com/MLRG-CEFET-RJ/coletaisbn.git

ENTRYPOINT ["/bin/bash"]

