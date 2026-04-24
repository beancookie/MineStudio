# MineStudio Examples

本目录包含 MineStudio 的使用示例。

## 示例列表

| 脚本 | 说明 |
|------|------|
| `run_simulator.py` | 基础模拟器，随机策略 |
| `run_vpt_policy.py` | VPT 预训练模型推理 |
| `run_rocket_policy.py` | ROCKET-1 预训练模型推理 |

## 本地运行

### 1. 安装依赖

```bash
pip install MineStudio
```

### 2. 运行示例

```bash
# 基础模拟器（随机策略）
python run_simulator.py

# VPT 模型推理
python run_vpt_policy.py

# ROCKET-1 模型推理
python run_rocket_policy.py
```

### GPU 渲染（可选）

```bash
MINESTUDIO_GPU_RENDER=1 python run_simulator.py
```

## Docker 运行

### 构建镜像

```bash
docker build --platform=linux/amd64 -t minestudio -f ../assets/Dockerfile ..
```

### 运行容器

**Linux/macOS：**

```bash
docker run -it --rm \
  -v $(pwd)/examples:/workspace/examples \
  -w /workspace/examples \
  minestudio \
  python run_simulator.py
```

**Windows PowerShell：**

```powershell
docker run -it --rm -v ${PWD}\examples:/workspace/examples -w /workspace/examples minestudio python run_simulator.py
```

### 运行其他示例

```bash
docker run -it --rm -v ${PWD}\examples:/workspace/examples -w /workspace/examples minestudio python run_vpt_policy.py

docker run -it --rm -v ${PWD}\examples:/workspace/examples -w /workspace/examples minestudio python run_rocket_policy.py
```

## 输出

视频文件保存在 `./output` 目录：

```
output/
└── episode_0.mp4
└── episode_1.mp4
└── ...
```

## 目录结构

```
examples/
├── README.md
├── run_simulator.py       # 基础模拟器示例
├── run_vpt_policy.py     # VPT 模型示例
├── run_rocket_policy.py   # ROCKET-1 模型示例
└── output/               # 生成的视频文件
```
