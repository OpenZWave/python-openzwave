FROM debian:wheezy
MAINTAINER bibi21000 <bibi21000@gmail.com>
ADD . /home/docker-py2
WORKDIR /home/docker-py2
RUN apt-get update && apt-get install -y make python
RUN make -C .. python-deps
RUN make -C .. autobuild-deps
RUN env
RUN make -C .. update
RUN make -C .. build
RUN make -C .. install
RUN make -C .. autobuild-tests
