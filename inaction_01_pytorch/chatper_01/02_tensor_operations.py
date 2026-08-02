from __future__ import print_function
import torch

SEP = '---------------------------------------------------------------'

# =================================================================
# 1. 基本算术运算：加、减、乘、除（都是逐元素 element-wise 运算）
# =================================================================
a = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
b = torch.tensor([[1.0, 1.0, 1.0], [2.0, 2.0, 2.0]])

print('a =')
print(a)
print('b =')
print(b)
print(SEP)

print('加法 a + b:')
print(a + b)
print('等价写法 torch.add(a, b):')
print(torch.add(a, b))
print(SEP)

print('减法 a - b:')
print(a - b)
print(SEP)

print('逐元素乘法 a * b (注意不是矩阵乘法):')
print(a * b)
print(SEP)

print('逐元素除法 a / b:')
print(a / b)
print(SEP)

# 带下划线 _ 的方法是"原地操作"（in-place），会直接修改调用者本身
c = a.clone()
print('原地加法 c.add_(b) 之前 c =')
print(c)
c.add_(b)
print('c.add_(b) 之后 c 被修改了:')
print(c)
print(SEP)


# =================================================================
# 2. 矩阵乘法：mm / matmul / @ / bmm
# =================================================================
x = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])  # 3行2列
y = torch.tensor([[1.0, 0.0], [0.0, 1.0]])               # 2行2列

print('x (3x2):')
print(x)
print('y (2x2):')
print(y)
print(SEP)

print('矩阵乘法 torch.mm(x, y)  结果形状 3x2:')
print(torch.mm(x, y))
print('等价写法 torch.matmul(x, y):')
print(torch.matmul(x, y))
print('等价写法 x @ y  (Python 3.5+ 的 @ 运算符):')
print(x @ y)
print(SEP)

# bmm 用于批量矩阵乘法，输入形状是 [batch, n, m]
batch_x = torch.rand(4, 3, 2)   # 4 个 3x2 矩阵
batch_y = torch.rand(4, 2, 5)   # 4 个 2x5 矩阵
batch_result = torch.bmm(batch_x, batch_y)
print('批量矩阵乘法 torch.bmm(batch_x, batch_y) 结果形状:')
print(batch_result.size())  # torch.Size([4, 3, 5])
print(SEP)


# =================================================================
# 3. 矩阵的转置 (重点)
# =================================================================
m = torch.tensor([[1, 2, 3], [4, 5, 6]])  # 2行3列
print('原始矩阵 m (2行3列):')
print(m)
print(SEP)

# 3.1 .t() 只适用于 2 维张量的转置，最常用最简单
print('m.t()  转置成 3行2列:')
print(m.t())
print('转置后形状:', m.t().size())
print(SEP)

# 3.2 .T 属性，是 .t()/.permute() 的简写（2维等价于 .t()）
print('m.T  效果和 m.t() 一样:')
print(m.T)
print(SEP)

# 3.3 .transpose(dim0, dim1) 可以指定交换任意两个维度，适用于任意维数的张量
print('m.transpose(0, 1)  交换第0维和第1维，效果和 m.t() 相同:')
print(m.transpose(0, 1))
print(SEP)

# 3.4 高维张量转置要用 transpose 或 permute，.t() 不支持 2 维以上
m3d = torch.rand(2, 3, 4)  # 形状 [2, 3, 4]
print('三维张量 m3d 形状:', m3d.size())
print('m3d.transpose(1, 2)  只交换第1维和第2维，形状变为:')
print(m3d.transpose(1, 2).size())  # [2, 4, 3]
print('m3d.permute(2, 0, 1)  按任意顺序重排全部维度，形状变为:')
print(m3d.permute(2, 0, 1).size())  # [4, 2, 3]
print(SEP)

# 3.5 转置是"视图操作"，不拷贝数据，和原张量共享内存
t = m.t()
print('m 和 m.t() 是否共享内存 (t[0][0] = 100 会影响 m):')
t[0][0] = 100
print('修改 t 后, m 变成:')
print(m)
print(SEP)

# 3.6 转置后内存不连续，某些操作(如 view)需要先 .contiguous()
print('m.t().is_contiguous():', m.t().is_contiguous())
print('m.t().contiguous().view(-1):')
print(m.t().contiguous().view(-1))
print(SEP)

# 3.7 t_() 是转置的原地版本，直接修改自身
n = torch.tensor([[1, 2], [3, 4]])
print('n 原地转置前:')
print(n)
n.t_()
print('n.t_() 之后 n 被原地修改:')
print(n)
print(SEP)


# =================================================================
# 4. 形状变换：view / reshape / squeeze / unsqueeze
# =================================================================
v = torch.arange(12)
print('v =', v)
print(SEP)

print('v.view(3, 4)  改成 3行4列 (共享内存，要求内存连续):')
print(v.view(3, 4))
print(SEP)

print('v.reshape(2, 6)  和 view 类似，但在不连续时会自动拷贝:')
print(v.reshape(2, 6))
print(SEP)

sq = torch.zeros(1, 3, 1)
print('sq 形状:', sq.size())
print('sq.squeeze()  去掉所有长度为1的维度，形状变为:', sq.squeeze().size())
print('sq.unsqueeze(0)  在第0维插入一个长度为1的维度，形状变为:', sq.unsqueeze(0).size())
print(SEP)


# =================================================================
# 5. 拼接与堆叠：cat / stack
# =================================================================
p = torch.tensor([[1, 2], [3, 4]])
q = torch.tensor([[5, 6], [7, 8]])

print('torch.cat([p, q], dim=0)  按行拼接 (增加行数):')
print(torch.cat([p, q], dim=0))
print('torch.cat([p, q], dim=1)  按列拼接 (增加列数):')
print(torch.cat([p, q], dim=1))
print(SEP)

print('torch.stack([p, q], dim=0)  堆叠出新的一维，形状变为:')
print(torch.stack([p, q], dim=0).size())  # [2, 2, 2]
print(SEP)


# =================================================================
# 6. 归约运算：sum / mean / max / min / argmax
# =================================================================
r = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
print('r =')
print(r)
print(SEP)

print('r.sum()  全部元素求和:', r.sum().item())
print('r.sum(dim=0)  按列求和(压缩行维度):', r.sum(dim=0))
print('r.sum(dim=1)  按行求和(压缩列维度):', r.sum(dim=1))
print(SEP)

print('r.mean()  全部元素求平均:', r.mean().item())
print('r.max()  全部元素最大值:', r.max().item())
print('r.max(dim=1)  每行最大值及其下标 (values, indices):')
print(r.max(dim=1))
print('r.argmax(dim=1)  每行最大值所在的下标:', r.argmax(dim=1))
print(SEP)


# =================================================================
# 7. 广播机制 (broadcasting)：形状不同的张量也能运算
# =================================================================
row = torch.tensor([1, 2, 3])          # 形状 [3]
mat = torch.tensor([[0, 0, 0], [10, 10, 10], [20, 20, 20]])  # 形状 [3, 3]

print('mat + row  row 会被广播到每一行:')
print(mat + row)
print(SEP)


# =================================================================
# 8. 与 NumPy 互转
# =================================================================
import numpy as np

t1 = torch.ones(3)
np1 = t1.numpy()
print('t1.numpy() ->', np1, type(np1))

np2 = np.array([1.0, 2.0, 3.0])
t2 = torch.from_numpy(np2)
print('torch.from_numpy(np2) ->', t2)
print(SEP)


# =================================================================
# 9. 设备切换：CPU / GPU (.to(device))
# =================================================================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('当前可用设备:', device)
t3 = torch.rand(2, 2).to(device)
print('t3 所在设备:', t3.device)
