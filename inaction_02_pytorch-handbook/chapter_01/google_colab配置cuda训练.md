# 在 Google Colab 中配置并使用 CUDA 训练

Google Colab 提供免费（或付费 Pro）的云端 GPU，是在没有本地 NVIDIA 显卡的情况下（比如 Mac）体验 CUDA 训练最简单的方式。本教程介绍从零开始的配置步骤。

## 1. 打开 Colab 并新建笔记本

1. 浏览器访问 `https://colab.research.google.com/`（需要 Google 账号登录）。
2. 点击左上角「文件」→「新建笔记本」，会打开一个 Jupyter Notebook 风格的界面。

## 2. 切换运行时为 GPU

这是最关键的一步——默认新建的笔记本是 **CPU** 运行时，必须手动切换：

1. 顶部菜单：`代码执行程序` (Runtime) → `更改运行时类型` (Change runtime type)。
2. 「硬件加速器」(Hardware accelerator) 选择 **GPU**。
   - 免费版一般分配 **Tesla T4**。
   - Colab Pro/Pro+ 付费用户可能分到 A100/V100 等更强的 GPU。
3. 点击「保存」。

> 注意：更改运行时类型后，如果之前已经运行过代码，环境会重置，需要重新执行所有 cell。

## 3. 验证 GPU 是否分配成功

新建一个代码 cell，运行：

```python
!nvidia-smi
```

如果配置成功，会打印出类似下面的信息（显卡型号、显存、驱动版本等）：

```
+-----------------------------------------------------------------------+
| NVIDIA-SMI 535.xx    Driver Version: 535.xx    CUDA Version: 12.2     |
|-------------------------------+----------------------+----------------|
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr|
|   0  Tesla T4               Off | 00000000:00:04.0 Off |                0 |
+-----------------------------------------------------------------------+
```

如果报错 `NVIDIA-SMI has failed...`，说明运行时还是 CPU，回到第 2 步重新设置。

## 4. 在 PyTorch 中确认 CUDA 可用

Colab 自带的环境通常已经预装了带 CUDA 支持的 PyTorch，无需额外安装：

```python
import torch

print(torch.__version__)              # PyTorch 版本
print(torch.cuda.is_available())      # 应该是 True
print(torch.cuda.get_device_name(0))  # 例如 'Tesla T4'
```

如果 `torch.cuda.is_available()` 仍是 `False`，检查：
- 运行时类型是否已切换为 GPU（第 2 步）。
- 是否切换后重新运行了所有代码（尤其是 import 语句）。

## 5. 一个完整的 CUDA 训练小例子

下面用一个简单的全连接网络在随机数据上训练，展示如何把模型和数据搬到 GPU：

```python
import torch
import torch.nn as nn
import torch.optim as optim

# 1. 指定 device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("使用设备:", device)

# 2. 构造一个简单模型
model = nn.Sequential(
    nn.Linear(10, 64),
    nn.ReLU(),
    nn.Linear(64, 1)
).to(device)   # 模型搬到 GPU

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# 3. 构造一些随机训练数据
x = torch.randn(256, 10, device=device)   # 直接在 GPU 上创建
y = torch.randn(256, 1, device=device)

# 4. 训练循环
for epoch in range(100):
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

print("训练完成，最终 loss:", loss.item())
```

运行后可以观察到 loss 逐渐下降，并且全程数据都在 GPU 上计算。

## 6. 挂载 Google Drive（保存数据集/模型权重）

Colab 的虚拟机运行结束后文件会清空，如果要持久化数据集或训练好的模型，建议挂载 Google Drive：

```python
from google.colab import drive
drive.mount('/content/drive')

# 之后可以像普通路径一样读写，例如：
torch.save(model.state_dict(), '/content/drive/MyDrive/model.pth')
```

首次运行会弹出授权链接，登录 Google 账号并允许访问即可。

## 7. 常见注意事项

- **会话有时间限制**：免费版 Colab 长时间空闲（约 30 分钟无操作）或连续运行超过一定时长（约 12 小时）会自动断开，训练大模型建议定期保存 checkpoint。
- **显存有限**：T4 一般是 16GB 显存，batch size 太大会报 `CUDA out of memory`，适当调小 batch size 即可。
- **GPU 并非独占**：免费版 GPU 资源有使用配额限制，频繁大量使用可能会被临时限制分配 GPU。
- **安装额外依赖**：Colab 已预装常见深度学习库（PyTorch、TensorFlow、numpy 等），额外的包用 `!pip install xxx` 安装即可，重启运行时后需要重新安装。
- **查看显存占用**：可以用 `torch.cuda.memory_allocated()` / `torch.cuda.memory_reserved()` 监控显存使用情况，或直接运行 `!nvidia-smi` 查看整体占用。

## 8. 小结

| 步骤 | 操作 |
|---|---|
| 1 | 打开 colab.research.google.com，新建笔记本 |
| 2 | 代码执行程序 → 更改运行时类型 → 选择 GPU |
| 3 | `!nvidia-smi` 确认 GPU 已分配 |
| 4 | `torch.cuda.is_available()` 确认 PyTorch 能识别 GPU |
| 5 | 模型 `.to(device)`，数据 `.to(device)` 或直接在 GPU 上创建，正常训练即可 |
| 6 | 需要持久化时挂载 Google Drive |

这样就能在没有本地 NVIDIA 显卡（比如 Mac）的情况下，免费体验完整的 CUDA 训练流程。
