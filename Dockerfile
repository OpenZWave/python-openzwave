FROM debian:wheezy
MAINTAINER bibi21000 <bibi21000@gmail.com>
ENV PYOZW_DOCKER 1
ADD . /home/docker-py2
WORKDIR /home/docker-py2
RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y make sudo wget unzip && make ci-deps
RUN env
RUN make openzwave.gzip
RUN make buildso
RUN make venv-git-autobuild-tests
RUN make venv-shared-autobuild-tests
RUN make venv-pypi-autobuild-tests 
RUN make venv-bdist_wheel-whl-autobuild-tests 
RUN make venv-bdist_wheel-autobuild-tests 
