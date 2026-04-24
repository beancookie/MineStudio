"""
MineStudio 示例 - 使用 VPT 预训练模型运行
"""
import os
from minestudio.simulator import MinecraftSim
from minestudio.simulator.callbacks import RecordCallback
from minestudio.models import VPTPolicy

# 使用 Hugging Face 国内镜像
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")


def main():
    # 加载预训练模型（CPU 模式）
    print("Loading VPT policy model...")
    policy = VPTPolicy.from_pretrained("CraftJarvis/MineStudio_VPT.rl_from_early_game_2x")
    policy = policy.to("cpu")  # Windows WSL 不支持 GPU，使用 CPU
    policy.eval()
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

    # 运行推理
    memory = None
    obs, info = env.reset()
    print("Start running...")

    for i in range(1200):
        action, memory = policy.get_action(obs, memory, input_shape='*')
        obs, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            obs, info = env.reset()

    env.close()
    print("Done! Video saved to ./output")


if __name__ == "__main__":
    main()