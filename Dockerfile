FROM ubuntu:latest
MAINTAINER bibi21000 <bibi21000@gmail.com>
ENV PYOZW_DOCKER 1
RUN apt-get update && apt-get dist-upgrade -y
RUN apt-get install -y --no-install-recommends make sudo apt-utils
ADD . /home/pyozw
WORKDIR /home/pyozw
RUN ls
WORKDIR /home/pyozw/
RUN make docker-deps
RUN make openzwave.gzip
RUN make venv-dev-autobuild-tests
#RUN make venv-pypi-autobuild-tests
RUN make venv-pypilive-autobuild-tests
RUN apt-get install --force-yes -y pkg-config
RUN venv-git_shared-autobuild-tests
