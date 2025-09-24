#!/bin/bash

# Require Docker image name (from argument or environment variable)
DOCKER_IMAGE=${1:-$DOCKER_IMAGE_NAME}

if [ -z "$DOCKER_IMAGE" ]; then
  echo "=============================================="
  echo "ERROR: Docker image name is not set!"
  echo "You must provide a Docker image either as an argument or via the environment variable DOCKER_IMAGE_NAME."
  echo
  echo "Usage examples:"
  echo "  1) As a command-line argument:"
  echo "     sh run_docker_interactive.sh yolov8-STUDENT_ID:jetpack5.1"
  echo "  2) Via environment variable:"
  echo "     export DOCKER_IMAGE_NAME=yolov8-STUDENT_ID:jetpack5.1"
  echo "     sh run_docker_interactive.sh"
  echo "=============================================="
  exit 1
fi

# Create a wildcard Xauthority cookie (once per session)
XAUTH=${XAUTH:-/tmp/.docker.xauth}
touch "$XAUTH"
xauth nlist "$DISPLAY" | sed -e 's/^..../ffff/' | xauth -f "$XAUTH" nmerge -

# Allow only root inside the container to access X (safer than +local:)
xhost +SI:localuser:$(whoami)

# Run container with GPU, V4L2 camera, and X11 GUI access
sudo docker run -it --rm \
  --runtime nvidia \
  --net=host \
  --shm-size="1g" \
  --device /dev/video0 \
  --device /dev/gpiochip0 \
  -e DISPLAY="$DISPLAY" \
  -e XAUTHORITY="$XAUTH" \
  -e QT_X11_NO_MITSHM=1 \
  -v /tmp/.X11-unix:/tmp/.X11-unix:ro \
  -v "$XAUTH":"$XAUTH":ro \
  -v "$HOME/CMPE6012/20820550":/workspace \
  -v "/ssd/datasets":/datasets \
  -w /workspace \
  "$DOCKER_IMAGE"