FROM debian:jessie
MAINTAINER bibi21000 <bibi21000@gmail.com>
ADD . /home/docker-py3
WORKDIR /home/docker-py3
RUN apt-get update && apt-get install -y make python3
RUN make -C .. PYTHON_EXEC=python3 python-deps
RUN make -C .. PYTHON_EXEC=python3 autobuild-deps
RUN env
RUN make -C .. PYTHON_EXEC=python3 update
RUN make -C .. PYTHON_EXEC=python3 build
RUN make -C .. PYTHON_EXEC=python3 install
RUN make -C .. PYTHON_EXEC=python3 autobuild-tests
