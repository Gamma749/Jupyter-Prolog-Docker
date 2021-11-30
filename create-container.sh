#!/bin/bash

docker container rm jupyter-swipl

docker run \
	-p 8888:8888 \
	-v $(pwd)/notebooks:/notebooks \
	-v $(pwd)/kernels:/usr/local/share/jupyter/kernels/jswipl \
	--name jupyter-swipl \
	-it gamma749/jupyter-swipl run-notebook
