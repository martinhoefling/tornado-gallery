FROM ubuntu:trusty
MAINTAINER Martin Hoefling <martin.hoefling@gmx.de>

COPY .bowerrc bower.json requirements.txt setup.py /opt/tgallery/
COPY tgallery /opt/tgallery/tgallery

WORKDIR /opt/tgallery

RUN DEBIAN_FRONTEND="noninteractive" apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -y nodejs npm python3 python3-pip python-virtualenv python3-dev build-essential zlib1g-dev libjpeg-dev libexempi3 git
RUN npm install -g bower
RUN ln -s /usr/bin/nodejs /usr/local/bin/node
RUN bower --allow-root install
RUN virtualenv -p python3  /opt/tgallery/venv
RUN /opt/tgallery/venv/bin/pip install -r requirements.txt
RUN /opt/tgallery/venv/bin/python setup.py develop

ENTRYPOINT '/opt/tgallery/venv/bin/tgallery'

