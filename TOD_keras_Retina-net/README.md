# Nvidia Docker + TF API Object Detection training
## 1. *Docker image create*  
**docker build -t wanted_name:tag Dockerfile_path**  
!! Must be changed the file name to **'Dokerfile'**!!
## 2. *Docker Container create*  
```
sudo docker run \
--runtime=nvidia \
--shm-size=1g \
--ulimit memlock=-1 \
--ulimit stack=67108864 \
-it -p 8888:8888 -p 6006:6006 \
--name TOD_keras_retina \
-v /ssd2/TOD_keras_volume:/workspace/TOD_keras_volume \
nvcr.io/nvidia/tensorflow:18.08-py3
```
## 3. *Tensorflow Object Detection API model training*  
### 3.1. *KITTI DATA SET tree : Host-Container Shared folder(-v)*
```
.
├── inference
└── kitti
    ├── train
    │   ├── images
    │   └── labels
    └── val
        ├── images
        └── labels
```
### 3.2. *From /workspace/keras-retinanet/*
#### 3.2.1. Training run!
```
python keras_retinanet/bin/train.py \
    --batch-size=6 \
    --epochs=10 \
    --steps=1000 \
    --workers=2 \
    --max-queue-size=8 \
    --multi-gpu=2 \
    --multi-gpu-force \
    kitti /workspace/TOD_keras_volume/kitti/
```
##### 3.2.1.1. Result
```
From/workspace/keras-retinanet/logs/
logs/
└── events.out.tfevents.1548551959.09f90905e83c

From/workspace/keras-retinanet/snapshots/
snapshots/
└── resnet50_kitti_01.h5
```
#### 3.2.2. Transfer learning
```
python keras_retinanet/bin/train.py \
    --weights /workspace/TOD_keras_volume/resnet50_kitti_100.h5 \
    --batch-size=6 \
    --epochs=10 \
    --steps=1000 \
    --workers=2 \
    --max-queue-size=8 \
    --multi-gpu=2 \
    --multi-gpu-force \
    kitti /workspace/TOD_keras_volume/kitti
```
##### 3.2.2.1. Result
*Same 3.2.1.1.*
#### 3.2.3. Converting train *.h5 to inference *.h5
##### 3.2.3.1. Coverting
```
keras_retinanet/bin/convert_model.py \
    /workspace/keras-retinanet/snapshots/resnet50_kitti_01.h5 \
    /workspace/TOD_keras_volume/inference/resnet50_kitti_01.h5
```
##### 3.2.3.2. Result
*From /workspace/TOD_keras_volume*
```
inference/
└── resnet50_kitti_01.h5
```
