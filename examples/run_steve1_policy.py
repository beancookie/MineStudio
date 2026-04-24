"""
MineStudio 示例 - 使用 STEVE-1 预训练模型运行
"""
import os
import torch
from minestudio.simulator import MinecraftSim
from minestudio.simulator.callbacks import RecordCallback
from minestudio.models import SteveOnePolicy

# 使用 Hugging Face 国内镜像
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")


def main():
    # 加载预训练模型（CPU 模式）
    print("Loading STEVE-1 policy model...")
    model = SteveOnePolicy.from_pretrained("CraftJarvis/MineStudio_STEVE-1.official")
    model = model.to("cpu")  # Windows WSL 不支持 GPU，使用 CPU
    model.eval()
    print("Model loaded successfully!")

    # 创建环境，录制视频
    env = MinecraftSim(
        obs_size=(128, 128),
        callbacks=[
            RecordCallback(
                record_path="./output",
                fps=30,
                frame_type="pov",
            )
        ],
    )

    # 准备文本条件
    instruction = {
        "text": ["forward"],  # 自然语言指令
        "cond_scale": 1.0,
    }
    condition = model.prepare_condition(instruction, deterministic=False)
    print(f"Condition prepared: {list(condition.keys())}")

    # 运行推理
    memory = None
    obs, info = env.reset()
    print("Start running...")

    for i in range(1200):
        # 构造输入（包含 condition）
        input_data = {
            "image": obs["image"].unsqueeze(0).unsqueeze(0),  # (1, 1, H, W, 3)
            "condition": condition,
        }

        # 获取动作
        action, memory = model.get_action(input_data, memory, input_shape="*")

        # 执行动作
        obs, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            obs, info = env.reset()

    env.close()
    print("Done! Video saved to ./output")


if __name__ == "__main__":
    main()