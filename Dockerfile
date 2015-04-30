FROM debian:jessie
MAINTAINER bibi21000 <bibi21000@gmail.com>
ADD . /home/docker-py
WORKDIR /home/docker-py
RUN apt-get update && apt-get install -y make python
RUN make python-deps
RUN make autobuild-deps
RUN env
RUN make update
RUN make build
RUN make install
RUN make tests
