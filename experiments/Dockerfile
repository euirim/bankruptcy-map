FROM python:3.7.4-stretch

USER root

# Install packages for textract
RUN apt-get update
RUN apt-get install -y --no-install-recommends software-properties-common curl
RUN apt-add-repository contrib
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
    libtesseract-dev

# Microsoft fonts for missing pdf fonts error
RUN apt-get update
RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections
RUN apt-get install -y --no-install-recommends fontconfig ttf-mscorefonts-installer
RUN fc-cache -fv

RUN mkdir /opt/bankruptcy-map
COPY requirements.txt /opt
WORKDIR /opt

# Install python packages
RUN pip install -r requirements.txt

# Install Spacy Models
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en_core_web_lg

WORKDIR /opt/bankruptcy-map

EXPOSE 8888

LABEL maintainer="euirim@stanford.edu"
