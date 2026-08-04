from __future__ import print_function
import torch

print('\nshape 方法: --------------------------------------------------------------------')
x = torch.rand(5, 3)
print(x.shape)

print('\nview 方法: ---------------------------------------------------------------------')
print(x.view(3, 5))

print('\nnumel 方法: --------------------------------------------------------------------')
print(x.numel())

print('\nstride 方法: -------------------------------------------------------------------')
print(x.stride())

print('\ntorch.arange 方法: -------------------------------------------------------------')
x = torch.arange(12)
print(x)

print('\nreshape 方法: ------------------------------------------------------------------')
y = x.reshape(4, 3)
print(y)

print('\ntorch.empty 方法: --------------------------------------------------------------')
# 构造一个 5行3列的 数值全部为0的矩阵
x = torch.empty(5, 3)
print(x)

print('\ntorch.ones: -------------------------------------------------------------------')
# 构造一个 5行3列 数值全部为1的矩阵
y = torch.ones(5, 3)
print(y)

print('\ntorch.rand: -------------------------------------------------------------------')
# 构造一个 5行3列的 随机矩阵
z = torch.rand(5, 3)
print(z)

print('\n torch.zeros ------------------------------------------------------------------')
# 构造一个 数值为0 且数据类型为 long 类型的 矩阵
m = torch.zeros(5, 3, dtype=torch.long)
print(m)

print('\n torch.tensor: ----------------------------------------------------------------')
# 构造一个张量 直接使用
n = torch.tensor([[1, 2, 3], [2, 3, 4]])
print(n)
print('\nn.size = ' + str(n.size()) + ", n.dtype = " + str(n.dtype))

print('\n ones_like: -------------------------------------------------------------------')
# 根据已经存在的 张量n 构造一个 long 类型的张量
p = torch.ones_like(n, dtype=torch.float)
print(p)

print('\n torch.add(tx, ty): -----------------------------------------------------------')
# 矩阵的加法 相关的东西
tx = torch.tensor([[1, 2, 3], [2, 3, 4]], dtype=torch.long)
ty = torch.tensor([[1, 2, 3], [2, 3, 4]])
print(torch.add(tx, ty))

result = torch.empty(2, 3, dtype=torch.long)
torch.add(tx, ty, out=result)
print(result)

print('\n torch.rand: -----------------------------------------------------------------')
pm = torch.rand(5, 3, dtype=torch.float)
# 打印整个矩阵
print(pm)

# 只打印 第一行 纬度变为 一维
print(pm[1])

# 打印整个矩阵的第一行, 保持矩阵纬度不变
print(pm[:1])

print('\n torch.ones: ----------------------------------------------------------------')
x = torch.ones(2, 5, 3, dtype=torch.long)
print(str(x) + ', x.dim = ' + str(x.dim()) + ', x[0] = ' + str(x[0]) + ', x[0].dim = ' + str(x[0].dim()))

print('\n二维张量转置前: ---------------------------------------------------------------')
x = torch.tensor([[1, 1, 1, 1, 1], [2, 2, 2, 2, 2], [3, 3, 3, 3, 3]], dtype=torch.int32)
print(x)

print('\n二维张量转置后: ---------------------------------------------------------------')
x.t_()
print(x.is_contiguous())
print(x)

print('\n四维张量转置前: ---------------------------------------------------------------')
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

print('\n四维张量转置后: ---------------------------------------------------------------')
# 转置 组 和 块; 张量矩阵中的 x, y 不动
x.transpose_(1, 0)
# 转置 x 和 y; 组 和 块 不动
# x.transpose_(2, 3)
# x.transpose(2, 3)

# 转置后内存不连续了为什呢？
print(x.is_contiguous())
print(x)

print('\n10维张量转置前: ---------------------------------------------------------------')
# rand/randn 只能生成浮点数，要 int 类型必须用 randint（并指定取值范围 low, high）
x = torch.randint(0, 10, (2, 2, 2, 2, 3, 3, 3, 3, 4, 4))
print(x)

print('\n10维张量转置后: ---------------------------------------------------------------')
# 交换 dim0、dim1，dim0/dim1 只是位置编号，跟"行、列"没有必然关系
x.transpose_(0, 1)
print(x[0, 0, 0, 0, 0, 0, 0, 0, 0, 0].item())
print(x.is_contiguous())
print(x.shape)

print('\nx[].item: ------------------------------------------------------------------')
x = torch.tensor([[1, 2, 3], [4, 5, 6]])
print(x[0, 0].item())

x = torch.randint(0, 10, (1,))
print(x)

print('\n纬度表示: ------------------------------------------------------------------')
x = torch.tensor([1])
print(x.shape)
x = torch.tensor([2, 2, 2, 3])
print(x.shape)
