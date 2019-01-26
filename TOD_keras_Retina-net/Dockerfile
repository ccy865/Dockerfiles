FROM nvcr.io/nvidia/tensorflow:18.08-py3
MAINTAINER ccy865 <ccy865@gmail.com>

RUN git clone https://github.com/fizyr/keras-retinanet.git
RUN pip install --upgrade pip
RUN pip install numpy --user
RUN pip install jupyter --user
RUN pip install --upgrade numpy
WORKDIR /workspace/keras-retinanet

RUN pip install . --user
RUN python setup.py build_ext --inplace
RUN pip install --user git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI
RUN apt update && apt install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev

WORKDIR /workspace

EXPOSE 6006
EXPOSE 8888
