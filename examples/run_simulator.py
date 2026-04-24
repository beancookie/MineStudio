"""
MineStudio 基础使用示例 - 随机策略运行
"""
from minestudio.simulator import MinecraftSim
from minestudio.simulator.callbacks import RecordCallback


def main():
    # 1. 创建环境，录制视频保存到 ./output 目录
    env = MinecraftSim(
        obs_size=(128, 128),  # 观测图像分辨率
        callbacks=[
            RecordCallback(
                record_path="./output",  # 视频保存路径
                fps=30,  # 帧率
                frame_type="pov",  # 录制 pov 视角
            )
        ],
    )

    # 2. 重置环境，获取初始观测
    obs, info = env.reset()

    # 3. 运行 1200 步（大约 60 秒）
    for step in range(1200):
        # 随机采样动作
        action = env.action_space.sample()

        # 执行动作，获取下一个观测
        obs, reward, terminated, truncated, info = env.step(action)

        # 如果 episode 结束（terminated 或 truncated），重置环境
        if terminated or truncated:
            obs, info = env.reset()

    # 4. 关闭环境
    env.close()

    print("运行完成！视频保存在 ./output 目录")


if __name__ == "__main__":
    main()
