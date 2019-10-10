FROM python:3.7.4-buster

RUN mkdir /opt/bankruptcy-map
COPY . /opt/bankruptcy-map
WORKDIR /opt/bankruptcy-map

# Install python packages
RUN pip install -r requirements.txt

EXPOSE 8888
ENTRYPOINT ["jupyter", "notebook", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=", "--notebook-dir='/root'"]

LABEL maintainer="euirim@stanford.edu"
