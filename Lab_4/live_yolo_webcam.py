import cv2
from ultralytics import YOLO
import time

model = YOLO("yolov8s.pt")

# 1) Open webcam
cap = cv2.VideoCapture(0)  # try CAP_V4L2 on Linux

# 2) Set a reasonable resolution for speed
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

prev_time = time.time()
fps = 0.0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        start_time = time.time()

        # Inference, keep BGR, Ultralytics handles it
        results = model(frame, device="cuda")  # adjust imgsz for speed vs accuracy

        # Draw boxes and labels on a copy
        annotated = results[0].plot()  # returns BGR image with overlays

        # Calculate FPS and Latency
        now = time.time()
        dt = now - prev_time
        prev_time = now
        if dt > 0:
            fps = 0.9 * fps + 0.1 * (1.0 / dt) if fps > 0 else (1.0 / dt)

        latency_ms = (time.time() - start_time) * 1000  # per-frame latency

        # Overlay FPS
        cv2.putText(
            annotated,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        # Overlay Latency
        cv2.putText(
            annotated,
            f"Latency: {latency_ms:.1f} ms",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        # Show GUI window
        cv2.imshow("Test", annotated)

        # Exit on q
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
