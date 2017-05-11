FROM ubuntu:latest
MAINTAINER bibi21000 <bibi21000@gmail.com>
ENV PYOZW_DOCKER 1
ADD . /home/pyozw
WORKDIR /home/pyozw
RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y make sudo
RUN ls
WORKDIR /home/pyozw/
RUN make docker-deps
RUN make openzwave.gzip
RUN make venv-dev-autobuild-tests
#RUN make venv-pypi-autobuild-tests
RUN make venv-pypilive-autobuild-tests
