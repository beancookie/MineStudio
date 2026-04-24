# MineStudio Hackathon Dockerfile
# 预下载 ROCKET-1 模型

FROM minestudio

# pip / huggingface 镜像加速
ENV HF_ENDPOINT=https://hf-mirror.com

# 预下载 ROCKET-1 模型
RUN python -c "from minestudio.models import RocketPolicy; RocketPolicy.from_pretrained('CraftJarvis/MineStudio_ROCKET-1.12w_EMA')"

# 下载 Minecraft 引擎
RUN python -m minestudio.simulator.entry -y

WORKDIR /workspace

CMD ["python", "-m", "minestudio.simulator.entry"]
