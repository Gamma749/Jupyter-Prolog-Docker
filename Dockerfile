FROM swipl AS prolog
RUN apt-get update
RUN apt-get -y install python3 python3-pip
RUN python3 -m pip install --upgrade jswipl jupyterlab notebook
COPY run-notebook /usr/bin