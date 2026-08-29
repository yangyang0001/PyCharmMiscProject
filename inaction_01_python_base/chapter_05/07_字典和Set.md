# 字典（dict）和 Set 常用知识点

## 一句话理解

- **dict（字典/map/json）**：用 `{}` 定义，`{key: value}` 形式，按 key 查找、修改、删除。
- **set（集合）**：也用 `{}` 定义，但只放"值"不放"键值对"，**自动去重、无序**。

## dict：增删改查

```python
d = {'zhangsan': 85.5, 'lisi': 22.5, 'wangwu': 88}
print(d['wangwu'])        # 88

# 修改（key存在则更新）
d['wangwu'] = 100
print(d)

# 判断 key 是否存在
print('wangwu' in d)      # True

# 取值，不存在时给默认值（不会报错，也不会新增）
print(d.get('zhaoliu', '默认值'))
```

### dict 添加元素的几种方式

```python
d = {'a': 1}

# 1. 中括号赋值（最常用）：key存在则更新，不存在则新增
d['b'] = 2

# 2. update()：一次加多个，或合并另一个 dict
d.update({'c': 3})
d.update(x=4, y=5)          # 关键字参数形式
d.update([('z', 6)])        # 键值对列表形式

# 3. 字典解包：生成新字典，不改原字典
d3 = {**d, 'e': 5}

# 4. setdefault(key, default)：只在 key 不存在时才添加
d.setdefault('f', 6)

# 5. |= 合并运算符（Python 3.9+）
d |= {'g': 7}
```

### dict 删除元素

```python
d = {'zhangsan': 10, 'lisi': 20, 'wangwu': 100}
d.pop('wangwu')
print(d)   # {'zhangsan': 10, 'lisi': 20}
```

## set：自动去重的集合

```python
s = {1, 2, 3}
print(s)

# 用 list 构造 set，重复元素会被去重
s = set([10, 10, 20, 30, 30])
print(s)   # {10, 20, 30}
```

### set 添加元素

```python
s = {10, 20, 30}
s.add(5.5)     # add() 只能加单个元素
print(s)
```

### 踩坑：`True`/`False` 和 `1`/`0` 是"同一个元素"

Python 中 `bool` 是 `int` 的子类，`True == 1`、`False == 0`，并且哈希值也相同（`hash(True) == hash(1)`）。set 判断元素是否重复就是靠"相等 + 哈希相同"，所以：

```python
s = set()
s.add(True)
print(s)          # {True}   —— 集合里还没有1，正常添加

s2 = {1, 2, 3}
s2.add(True)
print(s2)         # {1, 2, 3}  —— 没有变化！True 被判定为和已有的 1 重复
```

**结论**：只要集合里已经有 `1`（或 `0`），再 `add(True)`（或 `add(False)`）就不会新增元素，也不会报错——这不是"不能添加"，而是被当成重复值忽略了。

### 踩坑：set / dict key 要求元素"可哈希"，list 不行

set 的元素（以及 dict 的 key）必须是**可哈希（hashable）**的，而 `list` 是可变对象，不可哈希。如果 tuple 里嵌套了 list，这个 tuple 也会变得不可哈希：

```python
a = (1, 2, [3, 4])
print(a)

b = set(a)   # TypeError: unhashable type: 'list'
```

报错原因：`set(a)` 是把 `a` 当作**可迭代对象**，依次取出元素 `1`、`2`、`[3, 4]` 放进集合，等价于：

```python
b = set()
b.add(1)
b.add(2)
b.add([3, 4])   # 这里报错，list 不可哈希
```

几种相关场景对比：

```python
a = (1, 2, [3, 4])

# 情况1：set(a) 遍历元组内部元素 → 报错（元素里有list）
b = set(a)            # TypeError

# 情况2：把整个 tuple a 当一个元素加入 set → 同样报错
c = set()
c.add(a)               # TypeError，因为 hash(a) 内部要哈希 [3, 4]，失败

# 情况3：tuple 里全是可哈希元素才行（用嵌套tuple代替list）
a2 = (1, 2, (3, 4))
b2 = set(a2)            # {1, 2, (3, 4)}  正常
c2 = set()
c2.add(a2)               # {(1, 2, (3, 4))}  正常，因为 a2 本身可哈希
```

**结论**：tuple 本身能不能当 set 元素 / dict 的 key，取决于它**内部所有元素是否都可哈希**。只要 tuple 里嵌套了 list（或 dict、set 这些可变类型），这个 tuple 就是不可哈希的，不能放进 set，也不能当 dict 的 key。

### 踩坑：dict 的 key 不能直接用 list

同样因为 list 不可哈希，dict 的 key 也不能是 list：

```python
# 尝试 dict 中 数组作为 key 使用
d = {[1, 2, 3]: 'zhangsan'}
# TypeError: unhashable type: 'list'
```

改用 tuple 就没问题（前提是 tuple 内部元素也都可哈希）：

```python
d = {(1, 2, 3): 'zhangsan'}
print(d)   # {(1, 2, 3): 'zhangsan'}
```

## dict / set 小结

| | dict | set |
|---|---|---|
| 定义 | `{key: value}` | `{value1, value2}` |
| 存的内容 | 键值对 | 只有值 |
| 是否去重 | key 天然唯一 | 值自动去重 |
| 是否有序 | 插入顺序（3.7+） | 无序 |
| 能否用下标取值 | 能（`d[key]`） | 不能 |
| key/元素要求 | key 必须可哈希 | 元素必须可哈希 |
