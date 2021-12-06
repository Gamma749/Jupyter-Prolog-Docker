# Jupyter-Prolog-Docker

The aim of this part of the directory is to get a jupyter notebook running in a docker container with prolog functionality. Each of these steps will be taken one at a time.

## Running this project
- Pull the Docker image: `docker pull gamma749/jupyter-swipl`
    - Alternatively, build the image yourself using the provided dockerfile. If renaming the image, please ensure your also rename the image called on in `create-container.sh`
- Run `./create-container.sh` to start a new container running jupyter notebook
    - Alternatively, you can do this manually (as well as getting access to the bash shell) by running 
    ```
    docker run \
        --rm \
        -p 8888:8888 \
        -v $(pwd)/notebooks:/notebooks \
        -v $(pwd)/kernels:/usr/local/share/jupyter/kernels/jswipl \
        --name jupyter-swipl \
        -it gamma749/jupyter-swipl bash
    ```
    then running 
    
    `jupyter-lab --ip=0.0.0.0 --port=8888 --allow-root --no-browser /notebooks`
    
    from within the container.
- Once jupyter starts, it will print a link to the terminal. Cmd+click (or copy paste) to follow this link in your host browser.
- To use magic file consultation, start a cell of prolog with `%file: <name>.pl`.

## Configuration
Note that your notebooks are kept in the `notebooks` directory. This is for persistent storage of the notebooks outside of the docker container. To change where your notebooks are kept, change the volume mount in `create-container` from `-v $(pwd)/notebooks:/notebooks` to `-v {YOUR_DIR_HERE}:/notebooks`. 

Due to a quirk of the kernels magic consultation files, all files referenced will be placed in this `notebooks` directory under a `consulted_files` directory. 

**NOTE**: If you do not create this subdirectory before the kernel saves a file, the `consulted_files` directory will be created as root, and mortal users will not be able to access it.

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

