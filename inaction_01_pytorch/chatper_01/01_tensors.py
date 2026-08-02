from __future__ import print_function
import torch

# 构造一个 5行3列的 数值全部为0的矩阵
x = torch.empty(5, 3)
print(x)
print('---------------------------------------------------------------')

# 构造一个 5行3列 数值全部为1的矩阵
y = torch.ones(5, 3)
print(y)
print('---------------------------------------------------------------')

# 构造一个 5行3列的 随机矩阵
z = torch.rand(5, 3)
print(z)
print('---------------------------------------------------------------')

# 构造一个 数值为0 且数据类型为 long 类型的 矩阵
m = torch.zeros(5, 3, dtype=torch.long)
print(m)
print('---------------------------------------------------------------')

# 构造一个张量 直接使用
n = torch.tensor([[1, 2, 3], [2, 3, 4]])
print(n)
print('n.size = ' + str(n.size()) + ", n.dtype = " + str(n.dtype))
print('---------------------------------------------------------------')

# 根据已经存在的 张量n 构造一个 long 类型的张量
p = torch.ones_like(n, dtype=torch.float)
print(p)
print('---------------------------------------------------------------')

# 矩阵的加法 相关的东西
tx = torch.tensor([[1, 2, 3], [2, 3, 4]], dtype=torch.long)
ty = torch.tensor([[1, 2, 3], [2, 3, 4]])
print(torch.add(tx, ty))

result = torch.empty(2, 3, dtype=torch.long)
torch.add(tx, ty, out=result)
print(result)
print('---------------------------------------------------------------')

pm = torch.rand(5, 3, dtype=torch.float)
# 打印整个矩阵
print(pm)

print(pm[1])

# 打印整个矩阵的第一行, 保持矩阵纬度不变
print(pm[:1])

print('---------------------------------------------------------------')
x = torch.ones(2, 5, 3, dtype=torch.long)
print(str(x) + ', x.dim = ' + str(x.dim()) + ', x[0] = ' + str(x[0]) + ', x[0].dim = ' + str(x[0].dim()))

print('二维张量转置前: ---------------------------------------------------------------')
x = torch.tensor([[1, 1, 1, 1, 1], [2, 2, 2, 2, 2], [3, 3, 3, 3, 3]], dtype=torch.int32)
print(x)
print('二维张量转置后: ---------------------------------------------------------------')
y = x.t()
print(y)

print('---------------------------------------------------------------')
x = torch.rand(2, 3, 2, dtype=torch.float)
print(x)

print(torch.Size([3, 2, 2]))
print('四维张量转置前: ---------------------------------------------------------------')
x = torch.tensor([
    [
        [
            [1, 1, 1, 1],
            [2, 2, 2, 2],
            [3, 3, 3, 3]
        ],
        [
            [4, 4, 4, 4],
            [5, 5, 5, 5],
            [6, 6, 6, 6]
        ]
    ],
    [
        [
            [7, 7, 7, 7],
            [8, 8, 8, 8],
            [9, 9, 9, 9]
        ],
        [
            [10, 10, 10, 10],
            [11, 11, 11, 11],
            [12, 12, 12, 12]
        ]
    ]], dtype=torch.int32)
print(x)
print('四维张量转置后: ---------------------------------------------------------------')
print(x.is_contiguous())
x.contiguous()
x.transpose_(0, 1)
print(x)
