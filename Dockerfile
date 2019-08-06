FROM ubuntu:latest
MAINTAINER Eduardo Bezerra "ebezerra@cefet-rj.br"

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip  

RUN git clone https://github.com/MLRG-CEFET-RJ/coletaisbn.git

RUN pip install disamby
RUN pip install pandas
RUN pip install argparse
RUN pip install crossrefapi
RUN pip install json2xml
RUN pip install isbnlib

ENTRYPOINT ["/bin/bash"]

