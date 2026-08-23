# 如何使用 CUDA

CUDA 是 NVIDIA 提供的 GPU 并行计算平台，PyTorch 通过 CUDA 把张量计算放到 GPU 上执行，从而大幅加速训练和推理。本教程介绍 PyTorch 中使用 CUDA 的基本方法。

## 1. 检查 CUDA 是否可用

```python
import torch

print(torch.cuda.is_available())   # True / False
```

- `torch.cuda.is_available()`：判断当前环境是否有可用的 CUDA 设备（即是否装有 NVIDIA GPU + 对应驱动 + CUDA 版 PyTorch）。
- 如果返回 `False`，可能原因：
  - 机器没有 NVIDIA 显卡（例如 Mac 电脑通常没有 CUDA，只能用 CPU 或 MPS）。
  - 安装的是 CPU 版 PyTorch，而不是 CUDA 版。
  - 显卡驱动或 CUDA 版本与 PyTorch 不匹配。

其他常用的辅助函数：

```python
torch.cuda.device_count()      # 可用 GPU 数量
torch.cuda.get_device_name(0)  # 第 0 张 GPU 的名称
torch.cuda.current_device()    # 当前默认 GPU 编号
```

## 2. 创建 `device` 对象

`torch.device` 用来统一描述"张量/模型应该放在哪个设备上"，推荐写成一段兼容 CPU/GPU 的代码：

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)  # cuda 或 cpu
```

这样代码在没有 GPU 的机器上也能正常跑（自动退回 CPU），无需手动改代码。

## 3. 把张量移动到 GPU

有三种常见方式：

```python
x = torch.tensor([1.0])

# 方式一：创建时直接指定 device
y = torch.ones_like(x, device=device)

# 方式二：用 .to(device) 移动已有张量
x = x.to(device)

# 方式三：用 .cuda() （只能用于 CUDA，不推荐，兼容性不如 .to）
x = x.cuda()
```

张量在同一设备上才能进行运算：

```python
z = x + y   # x, y 都在 GPU 上，结果 z 也在 GPU 上
print(z)    # tensor([...], device='cuda:0')
```

> 注意：不同设备上的张量不能直接运算（比如一个在 CPU、一个在 GPU），会报错 `RuntimeError: Expected all tensors to be on the same device`。

## 4. `.to()` 的两个作用：换设备 + 换类型

`.to()` 既可以搬运设备，也可以顺便转换数据类型：

```python
print(z.to("cpu", torch.double))
# tensor([...], dtype=torch.float64)
```

上面这行把 `z` 从 GPU 搬回 CPU，同时把类型转成 `float64`（`torch.double`）。

## 5. 模型也需要移动到 GPU

不仅是张量，`nn.Module` 模型同样需要显式移动到 GPU：

```python
model = MyModel()
model = model.to(device)

for x, y in dataloader:
    x, y = x.to(device), y.to(device)
    output = model(x)
    loss = criterion(output, y)
    ...
```

要点：**模型和输入数据必须在同一个 device 上**，否则会报错。

## 6. 常见注意事项

- **GPU 显存有限**：张量、模型都会占用显存，用完及时释放（`del tensor` + `torch.cuda.empty_cache()`）。
- **多卡场景**：可以用 `cuda:0`、`cuda:1` 指定具体某张卡，或用 `torch.nn.DataParallel` / `DistributedDataParallel` 做多卡并行。
- **数据搬运有开销**：CPU ↔ GPU 之间频繁搬数据会拖慢速度，尽量减少不必要的 `.to(device)` / `.cpu()` 调用。
- **Mac 用户**：Apple Silicon 没有 CUDA，可以用 `torch.backends.mps.is_available()` 判断并使用 `"mps"` 设备代替 `"cuda"` 加速。

## 7. 完整示例

```python
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

x = torch.tensor([1.0])
y = torch.ones_like(x, device=device)  # 直接在 GPU 上创建
x = x.to(device)                       # 把 x 搬到 GPU
z = x + y
print(z)                     # tensor([2.], device='cuda:0')
print(z.to("cpu", torch.double))  # tensor([2.], dtype=torch.float64)
```

## 8. 没有本地 NVIDIA 显卡怎么办？用 Google Colab

如果本地机器没有 NVIDIA 显卡（比如 Mac），可以用 Google Colab 免费体验 CUDA。Colab 依附于 Google 账号，不需要单独注册。

### 8.1 注册/使用 Google 账号

- 如果已有 Gmail/Google 账号（比如日常用的 Gmail 邮箱），可以直接用。
- 没有的话，访问 `https://accounts.google.com/signup` 免费注册一个，填手机号、邮箱、密码即可，几分钟搞定。

### 8.2 直接访问 Colab

1. 登录 Google 账号后，浏览器打开 `https://colab.research.google.com/`。
2. 会自动进入 Colab 首页，点击「新建笔记本」即可开始使用（完全免费，含免费 GPU 额度）。

不需要额外的"开通"或"申请"步骤——只要有 Google 账号，登录即可用。

### 8.3 （可选）付费升级 Colab Pro

如果免费版 GPU 配额不够用（经常被限速或分不到 GPU），可以在 Colab 里点右上角「Colab Pro」升级：

- **Colab Pro**（约 $9.99/月）：更长运行时间、更高优先级的 GPU（更容易分到 V100/A100）。
- **Colab Pro+**：更长后台运行、更高优先级。
- 免费版对于学习和小规模训练完全够用，建议先用免费版试试。

> 具体如何在 Colab 中切换 GPU 运行时、验证 CUDA、写训练代码，见同目录下的 [00_google_colab配置cuda训练.md](./00_google_colab配置cuda训练.md)。
