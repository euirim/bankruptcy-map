FROM python:3.7.4-buster

RUN mkdir /opt/bankruptcy-map
COPY . /opt/bankruptcy-map
WORKDIR /opt/bankruptcy-map

# Install python packages
RUN pip install -r requirements.txt

# Install Spacy Models
RUN python -m spacy download en_core_web_sm
RUN pip install https://blackstone-model.s3-eu-west-1.amazonaws.com/en_blackstone_proto-0.0.1.tar.gz

EXPOSE 8888
ENTRYPOINT ["jupyter", "notebook", "--no-browser", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=", "--notebook-dir='/root'"]

LABEL maintainer="euirim@stanford.edu"
