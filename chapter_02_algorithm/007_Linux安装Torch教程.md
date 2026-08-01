# Linux 安装 PyTorch（Torch）教程

本教程介绍如何在 Linux 系统上安装 PyTorch，涵盖 CPU 版本、NVIDIA GPU（CUDA）版本的安装方式，以及安装后的验证和常见问题排查。适用于跑本仓库 `chapter_02_algorithm` 下 NN / CNN / RNN / LSTM / Transformer 等示例代码。

---

## 一、安装前确认环境

### 1. 确认 Python 版本

PyTorch 目前主流支持 Python 3.9 ~ 3.12，建议使用虚拟环境隔离依赖：

```bash
python3 --version
```

### 2. 确认是否有 NVIDIA 显卡（决定装 CPU 版还是 GPU 版）

```bash
lspci | grep -i nvidia
```

如果有输出，说明有 NVIDIA 显卡，可以继续检查驱动是否安装：

```bash
nvidia-smi
```

- 如果 `nvidia-smi` 能正常输出显卡信息和 **CUDA Version**（如 `CUDA Version: 12.4`），说明驱动已装好，可以直接装 GPU 版 PyTorch（无需单独安装完整 CUDA Toolkit，PyTorch 自带运行所需的 CUDA 库）。
- 如果没有装驱动或没有 NVIDIA 显卡，就安装 CPU 版本即可。

---

## 二、创建虚拟环境（推荐）

避免污染系统 Python，推荐用 `venv` 或 `conda` 创建独立环境。

### 方式一：venv

```bash
python3 -m venv ~/venvs/torch-env
source ~/venvs/torch-env/bin/activate
```

### 方式二：conda

```bash
conda create -n torch-env python=3.11 -y
conda activate torch-env
```

激活后终端提示符前会出现 `(torch-env)` 前缀。

---

## 三、安装 PyTorch

PyTorch 官方推荐通过 <https://pytorch.org/get-started/locally/> 页面选择系统/包管理器/计算平台生成安装命令。以下是常见组合：

### 1. CPU 版本（无 GPU 或只想用 CPU 跑）

```bash
pip install torch torchvision torchaudio
```

### 2. GPU 版本（NVIDIA CUDA）

先用 `nvidia-smi` 确认 CUDA 版本，再选择对应的安装命令（以下为示例，具体版本号以官网当前给出的为准）：

```bash
# CUDA 12.4
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# CUDA 12.1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

> `nvidia-smi` 显示的 CUDA Version 是驱动支持的**最高**版本，选择小于等于该版本的 PyTorch CUDA 构建即可，不需要完全一致。

### 3. 使用 conda 安装（可选）

```bash
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

---

## 四、验证安装

```python
import torch

print("torch 版本:", torch.__version__)
print("CUDA 是否可用:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("GPU 名称:", torch.cuda.get_device_name(0))
    print("CUDA 版本:", torch.version.cuda)
```

预期输出示例：

```
torch 版本: 2.4.0+cu121
CUDA 是否可用: True
GPU 名称: NVIDIA GeForce RTX 4090
CUDA 版本: 12.1
```

如果是 CPU 版本，`torch.cuda.is_available()` 会返回 `False`，属于正常现象。

简单跑一次张量运算确认可用：

```python
x = torch.rand(3, 3)
y = torch.rand(3, 3)
print(x @ y)

if torch.cuda.is_available():
    x = x.to("cuda")
    y = y.to("cuda")
    print((x @ y).device)
```

---

## 五、常见问题排查

| 问题 | 原因/解决方法 |
|---|---|
| `torch.cuda.is_available()` 返回 `False`，但确实有 NVIDIA 显卡 | 装的是 CPU 版本的 torch；或 NVIDIA 驱动未安装/版本过旧，先用 `nvidia-smi` 确认驱动正常 |
| 安装时下载极慢或超时 | 国内网络建议使用国内镜像源，例如清华源：`pip install torch --index-url https://pypi.tuna.tsinghua.edu.cn/simple`（注意：GPU 版需用官方 `download.pytorch.org` 的 index-url，镜像源可能没有对应 CUDA 构建） |
| `ImportError: libcudart.so` 或类似动态库找不到 | 通常是自己额外装了系统级 CUDA Toolkit 且版本冲突，优先只依赖 pip 安装的 torch 自带的 CUDA 运行库，不必单独装 CUDA Toolkit |
| `pip install` 报权限错误 | 没有激活虚拟环境就直接装到系统 Python，先执行 `source ~/venvs/torch-env/bin/activate` 再安装 |
| 多个 Python/pip 版本混乱，装完 import 不到 | 用 `which python` / `which pip` 确认当前生效的是虚拟环境里的可执行文件 |
| GPU 显存不足（`CUDA out of memory`） | 减小 batch size，或 `torch.cuda.empty_cache()` 释放缓存，必要时重启进程 |

---

## 六、卸载 / 重装

```bash
pip uninstall torch torchvision torchaudio -y
```

卸载后重新按第三节的命令安装即可切换 CPU/GPU 版本。

---

## 七、小结

- 先用 `nvidia-smi` 确认是否有可用的 NVIDIA 驱动，决定装 CPU 版还是对应 CUDA 版本的 GPU 版 PyTorch。
- 建议在虚拟环境（venv/conda）中安装，避免与系统环境冲突。
- 安装完成后用 `torch.cuda.is_available()` 和简单的张量运算验证是否正常工作，再运行本仓库中的神经网络示例代码。
