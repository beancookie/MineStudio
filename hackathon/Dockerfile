# MineStudio Hackathon Dockerfile
# 预下载 ROCKET-1 模型

FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/nvcr.io/nvidia/pytorch:24.01-py3

# apt 镜像加速
RUN sed -i 's|cn\.archive\.ubuntu\.com|mirrors.tuna.tsinghua.edu.cn|g' /etc/apt/sources.list 2>/dev/null || true && \
    apt-get update && \
    apt-get install -y \
    wget \
    git \
    gnutls-bin \
    openssh-client \
    libghc-x11-dev \
    gcc-multilib \
    g++-multilib \
    libglew-dev \
    libosmesa6-dev \
    libgl1-mesa-glx \
    libglfw3 \
    xvfb \
    mesa-utils \
    libegl1-mesa \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    unzip \
    openjdk-8-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# pip / huggingface 镜像加速
ENV HF_ENDPOINT=https://hf-mirror.com

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --upgrade pip && \
    pip install MineStudio

# 预下载 ROCKET-1 模型
RUN python -c "from minestudio.models import RocketPolicy; RocketPolicy.from_pretrained('CraftJarvis/MineStudio_ROCKET-1.12w_EMA')"

# 下载 Minecraft 引擎
RUN python -m minestudio.simulator.entry -y

WORKDIR /workspace

CMD ["python", "-m", "minestudio.simulator.entry"]
