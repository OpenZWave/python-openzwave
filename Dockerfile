FROM debian:jessie
MAINTAINER bibi21000 <bibi21000@gmail.com>
ADD . /home/docker-py3
WORKDIR /home/docker-py3
RUN apt-get update && apt-get install -y make python3
RUN make PYTHON_EXEC=python3 python-deps
RUN make PYTHON_EXEC=python3 autobuild-deps
RUN env
RUN make PYTHON_EXEC=python3 update
RUN make PYTHON_EXEC=python3 build
RUN make PYTHON_EXEC=python3 install
RUN make PYTHON_EXEC=python3 autobuild-tests
