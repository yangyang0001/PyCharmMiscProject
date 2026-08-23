import torch

# 标记该张量是否需要追踪梯度; 主动打开 张量追踪梯度
print('\nrequires_grad_: -----------------------------------------------------------')
x = torch.rand(2, 3)
print(x)
x.requires_grad_(True)
print('x.requires_grad = ' + str(x.requires_grad))

print('\nis_leaf: ------------------------------------------------------------------')
print('x.is_leaf = ' + str(x.is_leaf))

print('\ngrad_fn: ------------------------------------------------------------------')
y = x + 2
print(y)
print('x.grad_fn = ' + str(y.grad_fn))

print('\ngrad: ------------------------------------------------------------------')
print('x.grad = '+ str(x.grad))
y.retain_grad()
y.sum().backward()
print('y.grad = ' + str(y.grad))

print('\nrequires_grad_: --------------------------------------------------------')
x = torch.rand(2, 2)
print('x = ' + str(x))
print('x.requires_grad = ' + str(x.requires_grad))
x.requires_grad_(True)
print('x.requires_grad = ' + str(x.requires_grad))

print('\nleaf_ref: --------------------------------------------------------------')
leaf_ref = x
print('leaf_ref = ' + str(leaf_ref))
print('leaf_ref.requires_grad = ' + str(leaf_ref.requires_grad))
print('leaf_ref.grad = ' + str(leaf_ref.grad))

print('\ngrad_fn: --------------------------------------------------------------')
x = (x * 3) / (x - 1)
print('x = ' + str(x.grad_fn))

print('\nbackward: --------------------------------------------------------------')
print('x = ' + str(x))
y = x * x
y.sum().backward()
print('y = ' + str(y))
print(y.sum())
# 因为 x 不是叶子节点 所以 x.grad 会警告
# print(x.grad)

print('\nbackward: --------------------------------------------------------------')
m = torch.rand(2, 2)
m.requires_grad_(True)
print('m = ' + str(m))
print('m.requires_grad = ' + str(m.requires_grad))
print('m.grad = ' + str(m.grad))
n = (m * m) / (m + 1)
print('n = ' + str(n))
print('n.requires_grad = ' + str(n.requires_grad))
n.sum().backward()
print('m.grad = ' + str(m.grad))

print('\nmean1: --------------------------------------------------------------')
a = torch.rand(2, 2, requires_grad=True)
print('a = ' + str(a))
# 计算 算数平均值
print(a.mean())

print('\nmean2: --------------------------------------------------------------')
print('a = ' + str(a))
b = a * a + 3 * a + 1
b.retain_grad()
print('b = ' + str(b))

c = b * 3 + 1
c.retain_grad()
print('c = ' + str(c))
out = c.sum()
print('out = ' + str(out))
print(out.size())
out.backward()
print('a.grad = ' + str(a.grad))
print('b.grad = ' + str(b.grad))
print('c.grad = ' + str(c.grad))

print('out = ' + str(out))

print(torch.tensor(1.0))
print(torch.tensor(2.0))

p = torch.tensor(1.0)
q = torch.tensor([1.0])
k = torch.tensor([[1.0]])
print('p.size = ' + str(p.size()))
print('q.size = ' + str(q.size()))
print('k.size = ' + str(k.size()))

aa = torch.rand(2, 2, 3, 1)
print('aa = ' + str(aa.size()))

print(3**2)