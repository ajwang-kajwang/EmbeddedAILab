# LAB_DIR/config.py
from pathlib import Path

LAB_DIR = Path.cwd()  # or Path('/workspace') inside container
LAB_DIR.mkdir(exist_ok=True, parents=True)

# Model and I/O
MODEL_PT = '../Lab4/yolov8x.pt'
IMG_SIZE = 640
BATCH = 1
DYNAMIC = False
HALF = False

# Artifacts
ONNX_PATH = LAB_DIR / 'yolov8x.onnx'
ENGINE_PATH = LAB_DIR / 'yolov8x_trt_from_onnx.engine'
ENGINE_PATH_T2T = LAB_DIR / 'yolov8x_trt_from_torch2trt.engine'
ENGINE_PATH_T2T_FP16 = LAB_DIR / 'yolov8x_trt_from_torch2trt_fp16.engine'
T2TRT_STATE = LAB_DIR / 'yolov8x_torch2trt.pth'
T2TRT_STATE_FP16 = LAB_DIR / 'yolov8x_torch2trt_fp16.pth'

# Dataset
DATA_YAML = '/datasets/coco/coco_mini_val.yaml'

# Camera
CAMERA_INDEX = 0  # replace with GStreamer string on Jetson if needed
