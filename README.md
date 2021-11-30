# Jupyter-Prolog-Docker

The aim of this part of the directory is to get a jupyter notebook running in a docker container with prolog functionality. Each of these steps will be taken one at a time.

## Running this project
- Pull the Docker image: `docker pull gamma749/jupyter-swipl`
    - Alternatively, build the image yourself using the provided dockerfile. If renaming the image, please ensure your also rename the image called on in `create-container.sh`
- Run `./create-container.sh` to destroy the previous container (if any) and start a new container, running jupyter notebook
- Once jupyter starts, it will print a link to the terminal. Cmd+click (or copy paste) to follow this link in your host browser.

## Configuration
Note that your notebooks are kept in the `notebooks` directory. This is for persistent storage of the notebooks outside of the docker container. To change where your notebooks are kept, change the volume mount in `create-container` from `-v $(pwd)/notebooks:/notebooks` to `-v {YOUR_DIR_HERE}:/notebooks`

The SWIPL kernel for jupyter is kept in the `kernels` directory. If you want to make further changes to the kernel, do so here so the changes are persistent.

## Development

### Running SWIPL in docker
The more difficult part of this process is getting SWIPL working, as installing and building everything ourselves would be a nightmare to do in a container.

Luckily for us, there is an [SWIPL docker image](https://hub.docker.com/_/swipl) already available. Using this as our base, we now just need to install python and jupyter!

### Jupyter notebook in Docker container
We can install python3, pip, and jupyter while building our custom image, to avoid downloads at run time. This is the least painful part of set up. We will also need to pip install jswipl for later integration.

### Integrating SWIPL into Jupyter 
To get SWIPL to run in Jupyter we need a new kernel. Following the steps in [this helpful git repo](https://github.com/veracitylab/jupyter-swi-prolog) we will create a new kernel. Note that because we are using the SWIPL base image, our kernels are stored in a different location (`/usr/local/share/jupyter/kernels/`) to what the git repo would indicate.

In this project, we got the SWIPL kernel before hand and stored it in the `kernels` directory. This means we can simply use a docker mount to put the kernel where it needs to be at runtime. This also means if we want to alter the kernel later it can be done from host and can be persistent.

### Running SWIPL in Jupyter in Docker
We will create another bind mount from `notebooks` to the containers `/notebooks` directory so our notebooks will be persistent. We can access the container using 

`docker exec -it jupyter-swipl bash`

From the containers command line we can then boot up our jupyter notebook using:

`jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser /notebooks`
- `--ip=0.0.0.0` as docker will only port forward ports on address 0.0.0.0
- `--port=8888` is the default jupyter notebook port
- `--allow-root` as our base SWIPL image has no other users but root
- `--no-browser` our container has no browser, so don't bother trying to run one
- `/notebooks` the mounted directory where our persistent notebooks are

Jupyter will then give us a link to our notebook, which we can open in a host browser.

### Easy Run
The provided script `create-container` will run all of this for you, creating the container and starting jupyter notebook.

## TODO:
- Get the remainder of the SWIPL git repo running in jupyter notebooks (specifically looking at the magic file consultation)

- Get the event calculus prolog set up.