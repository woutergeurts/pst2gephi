#
# Makefile for pst2gephi
#
#
PSTP=./pstprocessor.py 
all: perftest

test:
	$(PSTP) -v -c config.test

perftest:
	$(PSTP) -v -c config.perftest

#
# note: the make user must have docker privileges. 
# (as sudo-user)$ sudo adduser <user> docker
# (as user)     $ newgrp docker
#
# to get the sources of libpff:
#
DOCKER_BASE=pypffbase
DOCKERFILE_BASE=docker/Dockerfile.pypff
DOCKER_IMAGE=pst2gephi.img
DOCKER_NAME=pst2gephi.name
DOCKERFILE_RUN=docker/Dockerfile.pst2gephi

make.build_git: 
	echo "if docker does not work add the current user to group docker"
	echo "see Makefile for details"
	docker ps
	git submodule update --init --recursive
	touch make.build_git

make.build_base: $(DOCKERFILE_BASE) make.build_git
	docker image rm $(DOCKER_BASE) || true
	docker build -f $(DOCKERFILE_BASE) -t $(DOCKER_BASE) .
	touch make.build_base

make.build_img: $(DOCKERFILE_RUN) make.build_base
	docker image rm $(DOCKER_IMAGE) || true
	docker build -f $(DOCKERFILE_RUN) -t $(DOCKER_IMAGE) .
	touch make.build_img

run: make.build_img
	echo "to test: run ./go.sh in the docker container"
	docker run -it --rm --name $(DOCKER_NAME) $(DOCKER_IMAGE)
