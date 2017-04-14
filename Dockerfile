FROM debian:jessie
MAINTAINER bibi21000 <bibi21000@gmail.com>
ENV PYOZW_DOCKER 1
ADD . /home/docker-py2
WORKDIR /home/docker-py2
RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y  make sudo && make ci-deps && make venv-deps
RUN env
RUN make openzwave.gzip
RUN make venv-pypilive-autobuild-tests || true
RUN make venv-pypitest-autobuild-tests || true
