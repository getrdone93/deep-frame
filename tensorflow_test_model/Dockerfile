# Docker image for running examples in Tensorflow models.
# base_image depends on whether we are running on GPUs or non-GPUs
FROM nvidia/cuda:10.0-cudnn7-runtime-ubuntu18.04

ENV DEBIAN_FRONTEND=noninteractive 
ENV MODELS=models 
ENV RESEARCH_PATH=/${MODELS}/research 
ENV SLIM_PATH=${RESEARCH_PATH}/slim 
ENV PYTHONPATH=$PYTHONPATH:${RESEARCH_PATH}:${SLIM_PATH}

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    git \
    python-dev \
    python-pip \
    python-setuptools \
    protobuf-compiler \
    python-pil \
    python-lxml \
    python-tk \
    unzip
    
RUN pip install Keras Cython contextlib2 jupyter matplotlib tensorflow-gpu==1.13.1

#probably do git clone in future
COPY ${MODELS} /${MODELS}
COPY cocoapi /cocoapi

RUN cd /cocoapi/PythonAPI \
       && make \
       && cp -r pycocotools /${MODELS}/research

RUN cd /${MODELS}/research \
        && protoc object_detection/protos/*.proto --python_out=.

COPY test_container.py /test_container.py

#CMD ["python", "/test_container.py"]
WORKDIR /models/research
ENTRYPOINT [""]
