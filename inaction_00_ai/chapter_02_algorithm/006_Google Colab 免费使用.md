# Google Colab 免费使用教程

Google Colab（Colaboratory）是 Google 提供的免费云端 Jupyter Notebook 环境，无需任何本地配置即可编写和运行 Python 代码，并且免费提供 GPU / TPU 算力，非常适合学习深度学习、跑本仓库中的 NN / CNN / RNN / LSTM / Transformer 等示例代码。

---

## 一、Colab 是什么，能用来做什么

- 浏览器里的 Jupyter Notebook，代码运行在 Google 的云服务器上，不占用本地电脑资源。
- 免费账号即可使用 CPU，并可申请免费的 GPU（常见为 T4）或 TPU 加速。
- 笔记本文件（`.ipynb`）自动保存到 Google Drive，也可以直接读取 GitHub 上的 notebook。
- 常用于：机器学习/深度学习实验、数据分析、教学演示、跑本仓库里的神经网络示例。

---

## 二、开始使用（免费）

1. 使用 Google 账号登录 <https://colab.research.google.com>。
2. 点击「新建笔记本」（New Notebook），即可得到一个可以直接写代码的 `.ipynb` 文件。
3. 笔记本会保存在 Google Drive 的 `Colab Notebooks` 文件夹下。

无需信用卡、无需安装任何软件，打开网页即可用。

---

## 三、开启免费 GPU / TPU 加速

1. 菜单栏选择 **修改（Runtime）→ 更改运行时类型（Change runtime type）**。
2. 「硬件加速器」（Hardware accelerator）选择：
   - `GPU`（免费额度下通常分配到 T4）
   - `TPU`
   - `None`（纯 CPU）
3. 点击保存，Colab 会重新连接一个带 GPU/TPU 的虚拟机。

验证 GPU 是否可用：

```python
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "无 GPU")
```

或者用 TensorFlow：

```python
import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))
```

---

## 四、免费额度的限制（重要）

免费版 Colab 不是无限使用，了解限制可以避免踩坑：

| 限制项 | 免费版情况 |
|---|---|
| 会话时长 | 一次会话最长约 12 小时，超时自动断开 |
| 空闲断开 | 浏览器长时间无操作（约 90 分钟）会断开连接 |
| GPU 配额 | 每天/每段时间有使用上限，用得多会被限速甚至临时禁用 GPU |
| 显存/内存 | 免费 GPU 显存有限（T4 约 16GB），大模型容易 OOM |
| 无法保证机型 | 免费用户不能指定具体 GPU 型号，忙时可能分配较弱资源或排队 |
| 存储 | 断开连接后，未保存到 Drive 的本地文件（`/content` 下）会丢失 |

如果需要更长时间、更稳定的 GPU、更大显存，可以升级 **Colab Pro / Pro+**（付费），但学习和跑中小型模型免费版完全够用。

---

## 五、挂载 Google Drive（持久化保存数据/模型）

Colab 虚拟机重启后 `/content` 里的文件会清空，重要文件建议放到 Drive：

```python
from google.colab import drive
drive.mount('/content/drive')
```

首次运行会弹出授权链接，登录并允许访问后，Drive 内容会挂载到 `/content/drive/MyDrive/`。

```python
# 例如把训练好的模型保存到 Drive
torch.save(model.state_dict(), '/content/drive/MyDrive/model.pth')
```

---

## 六、安装第三方库

Colab 已预装常见库（numpy、pandas、torch、tensorflow、matplotlib 等），缺什么用 `!pip install` 临时安装即可：

```python
!pip install -q transformers
```

- 前面的 `!` 表示在 shell 中执行命令，而不是 Python 代码。
- 每次重新连接运行时都要重新安装（不会持久化），除非把安装步骤放在 notebook 开头每次运行。

---

## 七、上传/下载文件

**上传本地文件：**

```python
from google.colab import files
uploaded = files.upload()
```

**下载文件到本地：**

```python
from google.colab import files
files.download('result.csv')
```

**直接用 wget/curl 从网上下载数据集：**

```python
!wget https://example.com/dataset.zip
!unzip dataset.zip
```

---

## 八、从 GitHub 打开 / 保存 Notebook

- 打开方式：Colab 首页 → 「文件」→「打开笔记本」→「GitHub」标签，粘贴仓库地址或搜索用户名/仓库。
- 也可以直接把 GitHub 上 `.ipynb` 文件链接中的 `github.com` 换成 `colab.research.google.com/github`，直接在浏览器打开。
- 保存回 GitHub：「文件」→「在 GitHub 中保存副本」，可直接提交到指定仓库和分支。

---

## 九、在 Colab 中跑本仓库的神经网络示例

本仓库 `chapter_02_algorithm` 下有 NN / CNN / RNN / LSTM / Transformer 的教学代码，可以按以下步骤在 Colab 中运行：

1. 新建笔记本，开启 GPU（见第三节）。
2. 把代码克隆到 Colab 的临时环境：

   ```python
   !git clone https://github.com/<你的用户名>/PyCharmMiscProject.git
   %cd PyCharmMiscProject/chapter_02_algorithm
   ```

3. 安装依赖（按需）：

   ```python
   !pip install -q torch numpy matplotlib
   ```

4. 直接在 notebook 里运行/调试对应的示例代码，或用 `!python xxx.py` 执行脚本文件。

---

## 十、常见问题排查

- **GPU 显示不可用**：先检查「修改运行时类型」是否已选 GPU；免费额度用尽也会导致暂时无法分配 GPU，等待一段时间或换个时间段再试。
- **代码跑到一半断开连接**：多是空闲超时或超过 12 小时会话上限，重要中间结果要及时保存到 Drive。
- **显存不足（CUDA out of memory）**：减小 batch size，或 `Runtime → Restart runtime` 释放显存后重试。
- **重新连接后包/文件都没了**：`/content` 下内容不持久化，环境和大文件建议放 Drive，或在 notebook 开头统一重新安装依赖。

---

## 十一、小结

- 完全免费即可用浏览器打开、免费用 GPU/TPU，是学习深度学习最低门槛的方式之一。
- 免费版有会话时长、GPU 配额、显存等限制，适合学习和中小规模实验，不适合长时间大规模训练。
- 配合 Google Drive 挂载和 GitHub 克隆，可以把本地项目（如本仓库的算法示例）无缝搬到 Colab 上用免费 GPU 跑起来。
