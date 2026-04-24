# MineStudio Examples

## 基础使用

运行随机策略模拟器：

```bash
xvfb-run -a python run_simulator.py
```

或使用 GPU 渲染：

```bash
MINESTUDIO_GPU_RENDER=1 python run_simulator.py
```

视频输出到 `./output` 目录。

## Docker 运行

**构建镜像：**

```bash
docker build --platform=linux/amd64 -t minestudio -f ../assets/Dockerfile ..
```

**运行示例：**

```bash
docker run -it --rm \
  --gpus all \
  -v $(pwd)/examples:/workspace/examples \
  -w /workspace/examples \
  minestudio \
  xvfb-run -a python run_simulator.py
```

**Windows PowerShell：**

```powershell
docker run -it --rm -v ${PWD}\examples:/workspace/examples -w /workspace/examples minestudio python run_simulator.py
```

## 目录结构

```
examples/
├── README.md
├── run_simulator.py   # 基础模拟器示例
└── output/           # 生成的视频文件
    └── episode_*.mp4
```
