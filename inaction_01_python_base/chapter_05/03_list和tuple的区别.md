# list 和 tuple 到底有什么区别

## 一句话理解

- **list（数组/列表）**：用 `[]` 定义，**可变**（能增删改元素）。
- **tuple（元组）**：用 `()` 定义，**不可变**（一旦创建，元组本身的结构不能再改）。

除了"能不能改"这一点，list 和 tuple 在其他能力上几乎一样：都能按下标取值、都能存不同类型、都能嵌套。

## 对比表

| | list | tuple |
|---|---|---|
| 定义符号 | `[1, 2, 3]` | `(1, 2, 3)` |
| 能否修改元素 | 能 | 不能 |
| 能否增删元素 | 能（`append`/`insert`/`pop`...） | 不能 |
| 支持下标/切片取值 | 支持 | 支持 |
| 能否存不同类型 | 能 | 能 |
| 能否嵌套 | 能 | 能 |
| 性能 | 略慢（可变结构开销更大） | 略快、更省内存 |
| 能否当字典 key / 放进 set | 不能（可变对象不可哈希） | 能（前提是元组里的元素本身也都可哈希） |

## list：可变，操作丰富

```python
a = ['zhangsan', 'lisi', 'wangwu']
print(a)          # ['zhangsan', 'lisi', 'wangwu']

# 正向 / 反向取值
print(a[0], a[1])   # zhangsan lisi
print(a[-1])         # wangwu（-1 表示倒数第一个）

# 末尾追加
a.append('zhaoliu')
print(a)   # ['zhangsan', 'lisi', 'wangwu', 'zhaoliu']

# 指定位置插入
a.insert(1, 'gouzi')
print(a)   # ['zhangsan', 'gouzi', 'lisi', 'wangwu', 'zhaoliu']

# 删除指定位置的元素
a.pop(1)
print(a)   # ['zhangsan', 'lisi', 'wangwu', 'zhaoliu']
```

list 可以存不同类型，也可以嵌套另一个 list：

```python
L = ['zhangsan', 20, True]
print(L)   # ['zhangsan', 20, True]

arr = ['zhangsan', 'lisi', ['gouzi', 'xiaomao']]
print(len(arr))   # 3，嵌套的 list 只算一个元素
print(arr[2])     # ['gouzi', 'xiaomao']
```

## tuple：不可变，一旦定义不能改结构

```python
t = (1, 2, 3)
print(t)      # (1, 2, 3)
print(t[1])   # 2，取值和 list 用法一样

t[1] = 99     # TypeError: 'tuple' object does not support item assignment
```

**注意这个坑**：tuple 本身不可变，指的是**不能给 tuple 换绑一个新元素**（不能 `t[i] = xxx`）；但如果 tuple 里装的是一个 list，这个 list 本身还是可变的：

```python
a = ['zhangsan', True]
t = (1, 2, a)
print(t)          # (1, 2, ['zhangsan', True])

a.append('extra')
print(t)          # (1, 2, ['zhangsan', True, 'extra'])  tuple 结构没变，但里面的 list 内容变了

t[2].append('again')   # 这样写也合法，改的是 list，不是 tuple
print(t)          # (1, 2, ['zhangsan', True, 'extra', 'again'])
```

也就是说：**tuple 的"不可变"是指它内部各个位置绑定的对象不能被替换，而不是说它内部的对象本身也不可变。**

## 什么时候用 tuple，什么时候用 list

- 数据**不需要再变**（比如一个坐标 `(x, y)`、一行固定结构的数据）→ 用 tuple，语义上表达"这批数据是一个整体、不会再改"，也更安全（防止被意外修改）。
- 数据**需要动态增删改**（比如一个不断往里加东西的列表）→ 用 list。
- 需要把一组值当 **字典的 key** 或放进 **set** 去重 → 只能用 tuple（前提是元组里的元素都可哈希，比如别再嵌套 list）。

## 常见踩坑

- 只有一个元素的 tuple 要写成 `(1,)`，多加一个逗号；`(1)` 只是数字 `1` 加了个括号，不是 tuple。
- tuple "不可变"只保证结构不可变，内部如果装的是 list/dict 这类可变对象，照样能被修改（见上面的例子）。
- list 不能当字典的 key 或放进 set（因为可变对象不可哈希），tuple 可以（只要内部元素都可哈希）。
