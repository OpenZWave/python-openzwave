FROM $DOCKER_BASE
MAINTAINER bibi21000 <bibi21000@gmail.com>
ENV PYOZW_DOCKER 1
ADD . /home/docker
WORKDIR /home/docker
RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y make sudo
RUN make docker-deps
RUN make openzwave.gzip
