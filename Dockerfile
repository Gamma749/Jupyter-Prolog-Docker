FROM swipl AS prolog
RUN apt-get update
RUN apt-get -y install python3 python3-pip wget
RUN python3 -m pip install --upgrade jswipl jupyterlab notebook
COPY run-notebook /usr/bin
COPY setup /setup
RUN mkdir swi-kernel
RUN cd swi-kernel && wget https://raw.githubusercontent.com/targodan/jupyter-swi-prolog/master/kernel.json
RUN jupyter kernelspec install swi-kernel --user
RUN rmdir --ignore-fail-on-non-empty swi-kernel
ENV DEFAULT_KERNEL_NAME SWI-Prolog
WORKDIR /setup
RUN pip install -r /setup/requirements.txt
