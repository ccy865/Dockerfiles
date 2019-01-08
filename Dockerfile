FROM nvcr.io/nvidia/tensorflow:18.08-py3
MAINTAINER ccy865 <ccy865@gmail.com>

RUN pip install Cython
RUN pip install --upgrade pip
RUN pip install contextlib2
RUN pip install jupyter
RUN pip install matplotlib
RUN pip install pillow
RUN pip install lxml
RUN git clone https://github.com/tensorflow/models
RUN git clone https://github.com/cocodataset/cocoapi.git

WORKDIR /workspace/cocoapi/PythonAPI
RUN make
RUN cp -r pycocotools /workspace/models/research/

WORKDIR /workspace/models/research/
RUN wget -O protobuf.zip https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip
RUN unzip protobuf.zip
RUN ./bin/protoc object_detection/protos/*.proto --python_out=.
RUN export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
RUN pip install OpenCV-Python
RUN apt update && apt install -y libsm6 libxext6
RUN apt-get install -y libsm6 libxrender1 libfontconfig1

WORKDIR /workspace
RUN pip install --upgrade tensorflow-gpu
RUN git clone https://github.com/JongsooKeum/RetinaNet-tensorflow.git

EXPOSE 6006
EXPOSE 8888
