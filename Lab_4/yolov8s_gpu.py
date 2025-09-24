# Import YOLO from ultralytics
from ultralytics import YOLO
import time

# Load the YOLOv8 small model (pretrained on COCO)
model = YOLO("yolov8s.pt")
image_url = "a.jpg"

# Measure inference time
start_time = time.time()
# Run inference on an example image (URL or local path)
results = model(image_url,
                device='cpu',  # Use CPU for inference
)
end_time = time.time()
total_time = end_time - start_time
print(f"Inference Time Costs: {total_time:.3f} seconds")

# Show and save results
for r in results:
    r.save() 