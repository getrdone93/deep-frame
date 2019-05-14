# Docker image for running examples in Tensorflow models.
# base_image depends on whether we are running on GPUs or non-GPUs

#original dockerfile: ~/graduateWork/project/models/official/Dockerfile.gpu
FROM nvidia/cuda:10.0-cudnn7-runtime-ubuntu18.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    git \
    python \
    python-pip \
    python-setuptools

RUN pip install tf-nightly-gpu
#RUN git clone https://github.com/tensorflow/models.git /tensorflow_models
COPY *.py test_model.py

CMD ["python", "./test_model.py"]
