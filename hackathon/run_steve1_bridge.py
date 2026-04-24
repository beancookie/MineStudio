"""
MineStudio 示例 - 使用 STEVE-1 实现自动造桥
纯视觉 + 文本指令，无需 LLM

STEVE-1 通过文本指令控制，可以预设一系列建造动作指令
"""
import os
import torch
import numpy as np
from minestudio.simulator import MinecraftSim
from minestudio.simulator.callbacks import RecordCallback
from minestudio.models import SteveOnePolicy

# 使用 Hugging Face 国内镜像
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")


def build_bridge_sequence():
    """
    预设的建桥动作序列
    实际使用时可替换为 LLM 生成的动态指令
    """
    instructions = [
        # 1. 面向河流
        "look at water",
        "go forward",

        # 2. 放置石头
        "place stone forward",
        "go forward",
        "place stone forward",
        "go forward",
        "place stone forward",

        # 3. 继续铺设
        "go forward",
        "place stone forward",
        "go forward",
        "place stone forward",
        "go forward",
        "place stone forward",

        # 4. 到达对岸
        "go forward",
        "go forward",
    ]
    return instructions


class BridgeBuilder:
    """STEVE-1 驱动的造桥 Agent"""

    def __init__(self, device="cpu"):
        print("Loading STEVE-1 model...")
        self.device = device
        self.model = SteveOnePolicy.from_pretrained(
            "CraftJarvis/MineStudio_STEVE-1.official"
        ).to(device)
        self.model.eval()
        print("Model loaded!")

        # 创建环境
        self.env = MinecraftSim(
            obs_size=(128, 128),
            callbacks=[
                RecordCallback(
                    record_path="./output",
                    fps=30,
                    frame_type="pov",
                )
            ],
        )

        self.memory = None
        self.condition = None

    def set_instruction(self, instruction):
        """设置当前指令"""
        self.condition = self.model.prepare_condition(
            {"text": [instruction], "cond_scale": 1.0},
            deterministic=False
        )

    def reset(self):
        """重置环境"""
        obs, info = self.env.reset()
        self.memory = None
        return obs

    def step(self, obs):
        """执行一步推理"""
        if self.condition is None:
            raise ValueError("请先设置指令 set_instruction()")

        # 构造输入
        input_data = {
            "image": obs["image"].unsqueeze(0).unsqueeze(0),
            "condition": self.condition,
        }

        # 获取动作
        action, self.memory = self.model.get_action(
            input_data, self.memory, input_shape="*"
        )

        # 执行动作
        obs, reward, terminated, truncated, info = self.env.step(action)
        return obs, reward, terminated, truncated, info

    def run_sequence(self, instructions, max_steps_per_instruction=100):
        """执行一系列指令"""
        obs = self.reset()
        total_steps = 0

        for i, instruction in enumerate(instructions):
            print(f"\n[{i+1}/{len(instructions)}] 执行指令: {instruction}")
            self.set_instruction(instruction)

            for step in range(max_steps_per_instruction):
                obs, reward, terminated, truncated, info = self.step(obs)
                total_steps += 1

                if terminated or truncated:
                    obs = self.env.reset()

                # 简单终止条件：奖励为正或步数过多
                if reward > 0:
                    print(f"  获得奖励: {reward:.2f}")

            print(f"  完成，步数: {step+1}")

        print(f"\n总共执行 {total_steps} 步")
        self.env.close()
        print("Done! Video saved to ./output")


def main():
    # 创建造桥 Agent
    builder = BridgeBuilder(device="cpu")

    # 获取建桥动作序列
    instructions = build_bridge_sequence()

    # 执行建桥
    builder.run_sequence(instructions)


if __name__ == "__main__":
    main()
