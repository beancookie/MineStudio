"""
MineStudio 示例 - 使用 ROCKET-1 预训练模型运行
"""
import os
import torch
from minestudio.simulator import MinecraftSim
from minestudio.simulator.callbacks import RecordCallback
from minestudio.models import RocketPolicy

# 使用 Hugging Face 国内镜像
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")


def main():
    # 加载预训练模型（CPU 模式）
    print("Loading ROCKET-1 policy model...")
    model = RocketPolicy.from_pretrained("CraftJarvis/MineStudio_ROCKET-1.12w_EMA")
    model = model.to("cpu")  # Windows WSL 不支持 GPU，使用 CPU
    model.eval()
    print("Model loaded successfully!")

    # 创建环境，录制视频
    env = MinecraftSim(
        obs_size=(224, 224),
        callbacks=[
            RecordCallback(
                record_path="./output",
                fps=30,
                frame_type="pov",
            )
        ],
    )

    # 运行推理
    memory = None
    obs, info = env.reset()
    print("Start running...")

    for i in range(1200):
        # 构造输入 (batch=1, timesteps=1)
        input_data = {
            "image": obs["image"].unsqueeze(0).unsqueeze(0),  # (1, 1, H, W, 3)
            "segment": {
                "obj_id": torch.tensor([[6]]),  # 交互类型
                "obj_mask": torch.zeros(1, 1, 224, 224, dtype=torch.uint8),
            }
        }

        # 获取动作
        action, memory = model.get_action(input_data, memory, input_shape="*")

        # 转换为环境动作并执行
        obs, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            obs, info = env.reset()

    env.close()
    print("Done! Video saved to ./output")


if __name__ == "__main__":
    main()