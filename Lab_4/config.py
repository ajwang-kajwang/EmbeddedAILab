# Import YOLO from ultralytics
from ultralytics import YOLO
import time

# Load the YOLOv8 small model (pretrained on COCO)
model = YOLO("yolov8x.pt")

# Measure inference time
start_time = time.time()
# Run inference on an example image (URL or local path)
results = model("a.jpg",
                device=0,  # Use GPU for inference
)
end_time = time.time()
total_time = end_time - start_time
print(f"Inference Time Costs: {total_time:.3f} seconds")

# Show and save results
for r in results:
    r.save() 
