FROM python:3.7.4-stretch

USER root

# Install packages for textract
RUN apt-get update
RUN apt-get install -y \
    python-dev \
    libxml2-dev \
    libxslt1-dev \
    antiword \
    unrtf \
    poppler-utils \
    pstotext \
    tesseract-ocr \
    flac \
    ffmpeg \
    lame \
    libmad0 \
    libsox-fmt-mp3 \
    sox \
    libjpeg-dev \
    swig \
    libpulse-dev \
    zlib1g-dev \
    tesseract-ocr

RUN mkdir /opt/bankruptcy-map
COPY requirements.txt /opt
WORKDIR /opt

# Install python packages
RUN pip install -r requirements.txt

# Install Spacy Models
RUN python -m spacy download en_core_web_sm
RUN pip install https://blackstone-model.s3-eu-west-1.amazonaws.com/en_blackstone_proto-0.0.1.tar.gz

WORKDIR /opt/bankruptcy-map

EXPOSE 8888

LABEL maintainer="euirim@stanford.edu"
