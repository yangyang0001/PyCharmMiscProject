# 在 macOS 虚拟机中的 Ubuntu 能否使用 CUDA？

**结论先说：不能。** 在 macOS 上用虚拟机（Parallels、VMware Fusion、UTM、VirtualBox 等）跑 Ubuntu，**无法**在里面使用 CUDA。下面说明原因，以及真正能用 GPU/CUDA 的替代方案。

## 1. 为什么不行

### 原因一：Mac 硬件本身没有 NVIDIA GPU
CUDA 是 NVIDIA 显卡专属技术。而现在的 Mac：

- **Apple Silicon (M1/M2/M3/M4...)**：只有 Apple 自研 GPU，从硬件层面就没有 NVIDIA 芯片，无论装什么系统都不可能有 CUDA。
- **Intel Mac**：大多数机型用的是 AMD 显卡或核显；即使少数老款 Intel Mac 曾经用过 NVIDIA 显卡，macOS 从 10.14 之后也已停止官方支持 NVIDIA 驱动。

也就是说，**物理层面 Mac 上基本不存在可用的 NVIDIA GPU**。

### 原因二：虚拟机不支持 GPU 直通（passthrough）
即便物理机上真的有 NVIDIA GPU（比如少数场景），常见的 macOS 虚拟化软件也不支持把 GPU 直通给 Linux 虚拟机：

- Parallels Desktop、VMware Fusion、UTM（QEMU）、VirtualBox 在 macOS 上都**不提供 NVIDIA GPU 的 PCIe 直通**功能。
- 虚拟机里看到的"显卡"只是 hypervisor 模拟出来的虚拟显示设备，用于图形界面显示，**不具备 CUDA 计算能力**。

所以即使你在虚拟机里装了 Ubuntu + NVIDIA 驱动 + CUDA Toolkit，运行 `nvidia-smi` 或 `torch.cuda.is_available()` 也只会报错或返回 `False`，因为系统根本探测不到真实的 NVIDIA 硬件。

## 2. 如何验证（避免误判）

如果想亲自确认，可以在虚拟机里跑：

```bash
lspci | grep -i nvidia    # 查看 PCI 设备列表里有没有 NVIDIA 显卡
nvidia-smi                # 如果没有驱动/硬件，这里会直接报错
```

在 Python/PyTorch 里：

```python
import torch
print(torch.cuda.is_available())  # 在 Mac 虚拟机里几乎必然是 False
```

## 3. 真正能用 CUDA 的方案

既然虚拟机这条路走不通，以下是几种可行方案：

### 方案一：云端 GPU（最简单，推荐新手）
在有真实 NVIDIA GPU 的云服务器上跑 Ubuntu + CUDA，通过 SSH 或 Jupyter 远程使用：

- AWS EC2（如 g4dn、g5 系列实例）
- Google Cloud (GCP) Compute Engine + NVIDIA GPU
- 阿里云 / 腾讯云 GPU 云主机
- Google Colab（免费/付费，浏览器里直接用，最省事）
- Kaggle Notebooks（免费提供 GPU）

对于学习 PyTorch，**强烈建议先用 Google Colab**，不用装任何环境，浏览器打开就能用免费 GPU。

### 方案二：远程连接一台真实 Linux + NVIDIA 主机
如果实验室/公司有一台带 NVIDIA 显卡的 Linux 服务器，直接用 SSH + VS Code Remote / Jupyter Remote 连过去开发，Mac 只是客户端，计算在远程机器上完成。

### 方案三：使用 Windows/Linux 物理机（非 Mac）
如果本地必须要用 GPU 训练，需要一台真实带 NVIDIA 显卡的 PC，直接装 Ubuntu（双系统或独立主机），这样 GPU 是物理直通的，没有虚拟化限制。

### 方案四（Mac 本地加速）：使用 Apple 自己的 MPS，而不是 CUDA
如果就是想在 Mac 本地跑一些 GPU 加速（不追求 CUDA），可以直接在 macOS 上（不装虚拟机）用 PyTorch 的 MPS 后端，利用 Apple GPU 加速：

```python
import torch

if torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")

x = torch.rand(3, 3, device=device)
print(x)
```

注意：MPS 不是 CUDA，两者 API 类似但底层完全不同，某些 CUDA 专属算子在 MPS 上可能不支持。

## 4. 总结对比

| 方案 | 是否需要真实 NVIDIA GPU | 是否可行 |
|---|---|---|
| macOS 虚拟机跑 Ubuntu + CUDA | 是，但拿不到 | ❌ 不可行 |
| 云端 GPU 实例 / Colab | 云厂商提供 | ✅ 推荐 |
| 远程 SSH 到真实 NVIDIA 服务器 | 是（对方提供） | ✅ 可行 |
| 本地 Windows/Linux + NVIDIA 显卡物理机 | 是（本地） | ✅ 可行 |
| macOS 本地用 MPS（非虚拟机） | 否（用 Apple GPU） | ✅ 可行，但不是 CUDA |

**一句话总结**：CUDA 依赖真实 NVIDIA 显卡直接驱动硬件，macOS 上的虚拟机既没有 NVIDIA 硬件，也不支持 GPU 直通，所以无法使用。想用 GPU 加速，要么上云（推荐 Colab），要么用一台真正带 NVIDIA 显卡的物理机。
