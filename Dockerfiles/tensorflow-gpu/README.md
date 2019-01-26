# Nvidia Docker + TF API Object Detection training
## 1. *Docker image create*  
**docker build -t wanted_name:tag Dockerfile_path**  
<span style="color:red">Must be changed the file name to **Dokerfile**</span>
## 2. *Docker Container create*  
```
sudo docker run \
--runtime=nvidia \
--shm-size=1g \
--ulimit memlock=-1 \
--ulimit stack=67108864 \
-it -p 8888:8888 -p 6006:6006 \
--name TOD_slim_retina \
-v /ssd2/TOD_slim_volume:/workspace/TOD_slim_volume \
ccy865/gpu:v1_0
```
## 3. *Tensorflow Object Detection API model training*  
### 3.1 *Host-Container Shared folder(-v) tree*
```
├── data   
│   ├── kitti.record_train.tfrecord  
│   ├── kitti.record_val.tfrecord  
│   ├── kitti_label_map.pbtxt  
├── kitti_label_map.pbtxt  
├── models  
│   └── model  
│       ├── ssd_mobilenet_v1_kitti.config  
│       ├── eval  
│       └── train  
└── ssd_mobilenet_v1_coco_11_06_2017  
    ├── frozen_inference_graph.pb  
    ├── graph.pbtxt  
    ├── model.ckpt.data-00000-of-00001  
    ├── model.ckpt.index  
    └── model.ckpt.meta  
```
### 3.2 *From /workspace/models/research*
#### 3.2.1 Export PATH
```
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim:`pwd`/object_detection
```
#### 3.2.2 Training Config Set
```
PIPELINE_CONFIG_PATH='/workspace/TOD_slim_volume/models/model/ssd_mobilenet_v1_kitti.config'
MODEL_DIR='/workspace/TOD_slim_volume/data/'
NUM_TRAIN_STEPS=100
NUM_EVAL_STEPS=2
SAMPLE_1_OF_N_EVAL_EXAMPLES=10
```
#### 3.2.3 Training run!
```
python object_detection/model_main.py \
  --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
  --model_dir=${MODEL_DIR} \
  --num_train_steps=${NUM_TRAIN_STEPS} \
  --num_eval_steps=${NUM_EVAL_STEPS} \
  --sample_1_of_n_eval_examples=$SAMPLE_1_OF_N_EVAL_EXAMPLES \
  --alsologtostder
```
##### 3.2.3.1 Result
```
├── checkpoint
├── eval_0
│   └── events.out.tfevents.1548482211.f8a49746244a
├── events.out.tfevents.1548482119.f8a49746244a
├── export
│   └── Servo
│       └── 1548482212
│           ├── saved_model.pb
│           └── variables
│               ├── variables.data-00000-of-00001
│               └── variables.index
├── graph.pbtxt
├── kitti.record_train.tfrecord
├── kitti.record_val.tfrecord
├── kitti_label_map.pbtxt
├── model.ckpt-0.data-00000-of-00001
├── model.ckpt-0.index
├── model.ckpt-0.meta
├── model.ckpt-100.data-00000-of-00001
├── model.ckpt-100.index
└── model.ckpt-100.meta
```
#### 3.2.4 Converting *.ckpt to *.pb for inference
##### 3.2.4.1 Config set
```
INPUT_TYPE=image_tensor
PIPELINE_CONFIG_PATH='/workspace/TOD_slim_volume/models/model/ssd_mobilenet_v1_kitti.config'
TRAINED_CKPT_PREFIX='/workspace/TOD_slim_volume/data/model.ckpt-6000'
EXPORT_DIR='/workspace/TOD_slim_volume/6000out'
```
##### 3.2.4.2 Coverting
```
python object_detection/export_inference_graph.py \
  --input_type=${INPUT_TYPE} \
  --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
  --trained_checkpoint_prefix=${TRAINED_CKPT_PREFIX} \
  --output_directory=${EXPORT_DIR}
```
##### 3.2.4.3 Result
```
├── checkpoint
├── frozen_inference_graph.pb
├── model.ckpt.data-00000-of-00001
├── model.ckpt.index
├── model.ckpt.meta
├── pipeline.config
├── readme.txt
└── saved_model
    ├── saved_model.pb
    └── variables
```
