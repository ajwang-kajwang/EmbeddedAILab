FROM dustynv/l4t-pytorch:2.2-r35.4.1

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_ROOT_USER_ACTION=ignore \
    YOLO_CONFIG_DIR=/tmp \
    LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1

WORKDIR /workspace

# System: OpenCV from apt (avoid pip OpenCV), make 'python' point to Python 3, and add devtools repo
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils python3-opencv python-is-python3 ca-certificates gnupg wget \
 && rm -rf /var/lib/apt/lists/*

# Prereqs for repo/key setup
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates gnupg wget \
 && rm -rf /var/lib/apt/lists/*

# Add NVIDIA DevTools repo with signed-by keyring and install Nsight tools
RUN set -eux; \
  . /etc/lsb-release; \
  rel="$(echo "$DISTRIB_RELEASE" | tr -d .)"; \
  arch="$(dpkg --print-architecture)"; \
  # 1) Add devtools repo entry with its own keyring
  echo "deb [signed-by=/usr/share/keyrings/nvidia-devtools-archive-keyring.gpg] https://developer.download.nvidia.com/devtools/repos/ubuntu${rel}/${arch} /" \
    > /etc/apt/sources.list.d/nvidia-devtools.list; \
  # 2) Import the legacy devtools/CUDA key (7fa2af80) into that keyring
  wget -qO- https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub \
    | gpg --dearmor > /usr/share/keyrings/nvidia-devtools-archive-keyring.gpg; \
  # 3) Also install the new CUDA repo key package for future-proofing
  wget -q https://developer.download.nvidia.com/compute/cuda/repos/ubuntu${rel}/${arch}/cuda-keyring_1.1-1_all.deb; \
  dpkg -i cuda-keyring_1.1-1_all.deb; rm -f cuda-keyring_1.1-1_all.deb; \
  # 4) Update and install profiler CLIs
  apt-get update && apt-get install -y --no-install-recommends nsight-systems-cli nsight-compute \
 && rm -rf /var/lib/apt/lists/*

# Ensure pip can reach public PyPI (keeps NVIDIA index as extra)
RUN printf "[global]\nindex-url = https://pypi.org/simple\nextra-index-url = https://pypi.nvidia.com\n" > /etc/pip.conf

# Override any pip index settings from base image
ENV PIP_INDEX_URL=https://pypi.org/simple \
    PIP_EXTRA_INDEX_URL=https://pypi.nvidia.com

# Python: upgrade pip, satisfy Ultralytics deps (requests>=2.23), keep apt cv2 to avoid duplication
RUN PIP_INDEX_URL=https://pypi.org/simple \
    PIP_EXTRA_INDEX_URL=https://pypi.nvidia.com \python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir "requests>=2.31.0" "numpy>=1.23,<2" pyyaml pillow matplotlib psutil scipy seaborn onnx onnxruntime \
                               jupyterlab polars py-cpuinfo "ultralytics-thop>=2.0.0" && \
    pip install --no-deps --no-cache-dir ultralytics

# Quick sanity check for versions (single-line to avoid Dockerfile heredoc issues)
RUN python3 -c "import cv2, torch, torchvision; print('cv2:', cv2.__version__); print('torch:', torch.__version__); print('torchvision:', torchvision.__version__)"

CMD ["/bin/bash"]