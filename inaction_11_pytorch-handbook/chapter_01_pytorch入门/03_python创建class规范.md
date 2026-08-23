# Python 创建 Class 的规范

> 承接 [03_神经网络.md](./03_神经网络.md)：那一篇里 `class Net(nn.Module):` 这个写法只是"拿来用"，没有展开讲"为什么类要这样写、命名要遵循什么规则"——这一篇专门补上这块基础，讲清楚 Python 里定义类的通用规范，以及这些规范背后来自哪里（PEP 8）。

## 目录

1. PEP 是什么：规范从哪来
2. 命名规范
3. 类的基本结构与格式
4. `__init__` 与 `super().__init__()`
5. 属性访问：`@property` 而不是 `get_x()`/`set_x()`
6. 常用 dunder（双下划线）方法
7. 纯数据类：`@dataclass`
8. 继承相关：`super()`、方法重写、`isinstance`、多继承与 MRO、`abc.ABC`
9. 类型注解
10. 对照 `class Net(nn.Module)`：规范逐条落地
11. 工具：自动检查与格式化
12. 要点小结

## 1. PEP 是什么：规范从哪来

**PEP（Python Enhancement Proposal，Python 增强提案）** 是 Python 社区提议、讨论、记录"语言新特性、编码规范、开发流程"的官方文档机制，每份提案有唯一编号。和这篇文档最相关的是：

- **PEP 8**——代码风格指南（命名、缩进、空行、导入顺序……），本文档里几乎所有"规范"都出自这里，是 `flake8`、`pylint`、`black` 这类工具默认遵循的基准。
- **PEP 257**——docstring（文档字符串）应该怎么写的规范。
- **PEP 484**——类型注解（Type Hints）的规范来源，第9节会用到。

**一句话记住**：PEP 8 只是 PEP 体系里"管代码风格"的其中一份，PEP 本身是一整套涵盖语言特性、规范、流程的编号文档体系。

## 2. 命名规范

| 对象 | 命名风格 | 示例 |
|---|---|---|
| 类名 | `CapWords`（大驼峰 / PascalCase） | `class Net`、`class MyDataset` |
| 方法名、函数名、属性名 | `snake_case`（全小写+下划线） | `def forward(self)`、`self.learning_rate` |
| 常量 | 全大写+下划线 | `MAX_SIZE = 100` |
| "内部使用"属性/方法 | 单下划线前缀（约定俗成，不是强制私有） | `self._cache` |
| 避免子类命名冲突 | 双下划线前缀（触发 name mangling，谨慎使用） | `self.__state` |
| 魔法方法（dunder） | 双下划线前后包裹，**不要自己发明这种命名** | `__init__`、`__repr__` |

**反例**：`class my_net:`（类名不能用 snake_case）、`def Forward(self):`（方法名不能用大驼峰）——这两种写法不会报错，但违反 PEP 8，任何 linter 都会标红。

### 2.1 双下划线前缀触发的 "name mangling" 是什么

上面表格里"双下划线前缀"那一行提到会触发 **name mangling（名称改写）**，这是 Python 里一个容易让人意外的机制，单独展开说清楚。

**现象**：如果属性名以两个下划线开头、且**不是**以两个下划线结尾（比如 `__state`，但不是 `__init__` 这种前后都有下划线的 dunder 方法），Python 解释器会在类定义阶段**自动把这个名字改写成 `_ClassName__属性名`**：

```python
class A:
    def __init__(self):
        self.__state = 1        # 写的时候是 __state

a = A()
print(a.__dict__)                  # {'_A__state': 1}   —— 实际存成了 _A__state
print(a.__state)                    # AttributeError：找不到 __state 这个名字！
print(a._A__state)                  # 1，这才是真正存进去的名字
```

**为什么要有这个机制？** 目的是**防止子类不小心覆盖父类里"看起来是私有"的属性**。如果没有这层改写，下面这种情况会出问题：

```python
class Base:
    def __init__(self):
        self.__state = "base"     # 想表达"这是 Base 内部私有的东西，子类别碰"

    def show(self):
        print(self.__state)

class Child(Base):
    def __init__(self):
        super().__init__()
        self.__state = "child"     # 子类完全不知道父类也用了 __state 这个名字，以为在设自己的属性

c = Child()
c.show()    # 如果没有 name mangling，这里会打印 "child"，Base 的内部状态被子类意外覆盖了
```

有了 name mangling 之后，`Base.__init__` 里的 `self.__state` 被自动改写成 `self._Base__state`，`Child.__init__` 里的 `self.__state` 被改写成 `self._Child__state`——**两者变成了两个完全不同的名字，各自存在各自的 `__dict__` 键里，不会互相覆盖**：

```python
c = Child()
c.show()                       # "base"，Base 内部的状态没被子类影响
print(c.__dict__)                # {'_Base__state': 'base', '_Child__state': 'child'}
```

**几个实用要点：**

- name mangling 只在**类定义体内部**、**代码里直接写 `self.__xxx`**（或 `ClassName.__xxx`）这种形式时才会触发；它是**编译期的文本替换**，不是运行时按对象类型判断的动态机制——所以即使通过字符串拼出同样的名字，`getattr(obj, '__xxx')` 不会触发改写，行为和直接写 `obj.__xxx` 不同。
- 改写规则是 `_类名__属性名`，类名前面的下划线不算在"两个"里；如果类名本身以下划线开头，规则会去掉类名前导的下划线（这是极少数情况，不用特别记）。
- **name mangling 不是"真正的私有"**，只是让"意外撞名"变得很难发生；只要知道改写后的名字（`obj._ClassName__attr`），外部代码依然可以访问和修改，Python 没有 Java/C++ 那种编译期强制的私有访问控制，这也是"Python 里没有真正私有"这个说法的来源。
- **单下划线 `_state` 不会触发 name mangling**，只是约定俗成的"提示这是内部使用，请勿从外部访问"，没有任何语言层面的强制效果——这也是为什么第2节表格把单下划线和双下划线分成两行，前者是"君子协定"，后者才是"语言真的会动手改名字"。

**什么时候需要用双下划线？** 只有在写"基类里希望某个属性绝对不被子类意外撞名覆盖"这种场景才需要；日常业务代码里"想表达这是内部属性"，用单下划线 `_state` 就够了，双下划线用多了反而会让 `__dict__` 里的真实键名变得难以预测、调试时不好定位，不建议默认就用双下划线。

## 3. 类的基本结构与格式

```python
class Net(nn.Module):
    """一句话说明这个类是干什么的（可选，公共类建议写）"""

    class_attr = 0          # 类属性：所有实例共享同一份

    def __init__(self, in_features, out_features=10):
        super().__init__()
        self.in_features = in_features    # 实例属性：每个实例各自独立
        self.out_features = out_features

    def forward(self, x):
        ...
        return x

    def __repr__(self):
        return f"Net(in={self.in_features}, out={self.out_features})"
```

**格式上的硬性约定（PEP 8）：**

- 方法之间空一行，类与类之间空两行。
- `__init__` 的第一个形参永远是 `self`，约定名不能改。
- 类属性（写在方法外面）和实例属性（写在 `self.xxx = ...`）是两个不同的概念：类属性所有实例共享同一份内存，改一个实例的类属性不会影响其他实例（除非用可变对象踩坑，见下面提示）。

> **常见坑**：类属性如果是可变对象（列表、字典），所有实例会共享同一个对象，一个实例改了会影响所有实例：
> ```python
> class Bad:
>     items = []          # 危险：所有实例共享同一个列表
>     def __init__(self):
>         pass
>
> a, b = Bad(), Bad()
> a.items.append(1)
> print(b.items)          # [1] —— b 也被影响了，这通常不是想要的行为
> ```
> 需要"每个实例各自一份"的可变默认值，要在 `__init__` 里创建：`self.items = []`。

## 4. `__init__` 与 `super().__init__()`

- `__init__` 不是构造函数本身（真正创建对象的是 `__new__`），而是**初始化**方法：对象已经被创建好之后，用它来设置初始状态。
- **继承其他类时，`__init__` 第一行几乎总是先调用父类的初始化**：

```python
class Net(nn.Module):
    def __init__(self):
        super().__init__()   # Python 3 推荐写法
        # 或等价的旧式写法（教程里常见，两者完全等价）：
        # super(Net, self).__init__()
```

原因（呼应 [03_神经网络.md 第2节](./03_神经网络.md#2-定义网络以-lenet-5-为例逐层拆解)）：父类 `__init__` 往往会做必要的初始化工作（`nn.Module.__init__()` 会建立 `_parameters`、`_modules` 等簿记字典），跳过这一步会导致父类依赖的内部状态缺失，后续代码可能在毫无提示的情况下悄悄出错，而不是立刻报错——这是最难排查的一类 bug。

## 5. 属性访问：`@property` 而不是 `get_x()`/`set_x()`

Python 的风格是"属性访问看起来永远像访问字段"，不像 Java 那样用 `getX()`/`setX()` 包一层：

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius     # 单下划线：内部存储，不直接暴露

    @property
    def radius(self):              # 访问时写 circle.radius，不用加括号
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("radius 不能为负")
        self._radius = value

    @property
    def area(self):                 # 只读属性：没有 setter，不能被外部赋值
        return 3.14159 * self._radius ** 2
```

```python
c = Circle(5)
print(c.radius)     # 5，不是 c.radius()
c.radius = 10         # 触发 setter 里的校验逻辑
print(c.area)          # 314.159，只读，c.area = 100 会报错
```

**什么时候需要 `@property`？** 只有当"赋值时需要做校验/触发副作用"或者"某个值需要根据其他属性实时算出来"时才需要；如果只是单纯存取一个值，直接用普通属性 `self.x = x`，不需要为每个字段都套一层 `@property`——这是过度设计，Python 社区不推荐。

## 6. 常用 dunder（双下划线）方法

### 6.0 dunder 方法到底是什么

前后都带双下划线的方法（`__methodName__` 这种形式，全称 **double underscore**，简称 **dunder**）是 Python **预留给解释器的钩子（hook）**：你不需要、也不应该在业务代码里直接调用它们，而是**某个语法或内置函数被触发时，Python 自动帮你调用**。

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):        # v1 + v2 时自动调用，不是手动 v1.__add__(v2)
        return Vector(self.x + other.x, self.y + other.y)

v1, v2 = Vector(1, 2), Vector(3, 4)
v3 = v1 + v2       # 等价于 Python 在背后调用 v1.__add__(v2)
```

**两个关键点：**

- **不会被 2.1 节的 name mangling 改写**——改名机制只对"前有后无"的 `__attr` 生效，`__init__`、`__add__` 这种前后都有双下划线的名字是解释器保留的特殊语义，不参与改写。
- **不要自己发明新的 `__xxx__` 名字**——这个命名空间是 Python 语言保留的，自定义方法应该用普通 `snake_case` 名字（如 `calc_length`）；只有当你确实想让对象支持某个内置语法（`len()`、`+`、`for...in`、`with` 等）时，才去实现对应的、Python 已经定义好的 dunder 方法。

| 方法 | 触发场景 | 建议 |
|---|---|---|
| `__init__` | 创建实例后初始化 | 几乎每个类都会写 |
| `__repr__` | `repr(obj)`、在控制台/调试器里直接打印对象 | **建议每个类都实现**，应该返回"能用来重新构造这个对象"的字符串，面向开发者调试 |
| `__str__` | `print(obj)`、`str(obj)` | 面向用户展示，没定义时会自动回退用 `__repr__` |
| `__eq__` | `obj1 == obj2` | 需要按值比较两个实例时实现 |
| `__len__` | `len(obj)` | 类似容器的对象常用 |
| `__getitem__` | `obj[i]` | 类似容器/序列的对象常用（比如自定义 `Dataset`） |
| `__setitem__` | `obj[i] = value` | 需要支持下标赋值的容器类对象才实现 |
| `__iter__` / `__next__` | `for x in obj`，或手动 `iter(obj)`/`next(obj)` | 让对象变成可迭代对象；`__iter__` 返回迭代器（通常是 `self`），`__next__` 每次返回下一个元素，没有更多元素时 `raise StopIteration` |
| `__call__` | `obj(...)`，把实例当函数调用 | `nn.Module` 就是靠重写 `__call__` 才能写 `net(input)` 而不是 `net.forward(input)`（见 [03_神经网络.md 第2节](./03_神经网络.md#2-定义网络以-lenet-5-为例逐层拆解)） |
| `__enter__` / `__exit__` | `with obj:` 上下文管理器 | `__enter__` 在进入 `with` 块时调用（返回值赋给 `as` 后的变量），`__exit__` 在离开时调用（无论是否发生异常），常用于资源清理（文件句柄、锁、`torch.no_grad()` 这类场景） |

```python
class Net(nn.Module):
    def __repr__(self):
        return f"{self.__class__.__name__}(layers={len(list(self.children()))})"
```

### 6.1 `f"..."`：`__repr__`/`__str__` 里推荐用 f-string 拼字符串

上面 `__repr__` 例子里的 `f"..."` 是 **f-string（格式化字符串字面量）**，Python 3.6 起支持：在字符串前加一个 `f`，字符串里的 `{}` 会在运行时被自动替换成里面表达式的值。

```python
name = "zhangsan"
age = 18

print(f"Hello {name}, age {age}")     # "Hello zhangsan, age 18"
print(f"1+1={1+1}")                     # "1+1=2"，{} 里可以放任意表达式，不限于变量名
print(f"{name.upper()}")                 # "ZHANGSAN"，也可以调方法
print(f"{age:.2f}")                       # "18.00"，冒号后面跟格式化说明符（这里是保留2位小数）
```

**为什么 `__repr__`/`__str__` 里推荐用 f-string，而不是 `+` 拼接或 `.format()`：**

| 写法 | 示例 | 评价 |
|---|---|---|
| `%` 格式化（最老） | `"Hello %s" % name` | 不推荐，语法容易出错，可读性差 |
| `.format()` | `"Hello {}".format(name)` | 可用，但变量多了要么用位置编号、要么重复写变量名，比较啰嗦 |
| `+` 拼接 | `"Hello " + name` | 遇到非字符串类型（比如 `int`）要手动 `str()` 转换，多个变量拼接起来很啰嗦 |
| **f-string（推荐）** | `f"Hello {name}"` | 最简洁、可读性最好，变量名直接写在该出现的位置，`black`/`pylint` 等工具也默认推荐这种写法 |

所以第6节 `__repr__` 例子里的：

```python
return f"{self.__class__.__name__}(layers={len(list(self.children()))})"
```

是**符合现代 Python 规范的写法**——`self.__class__.__name__` 和 `len(list(self.children()))` 这两个表达式的结果，会被直接嵌进字符串该出现的位置，不需要手动拼接、也不需要额外调用 `str()`。

## 7. 纯数据类：`@dataclass`

如果一个类只是用来存一组数据、没什么复杂逻辑，手写 `__init__`/`__repr__`/`__eq__` 很啰嗦，用标准库的 `dataclasses` 自动生成：

```python
from dataclasses import dataclass

@dataclass
class TrainConfig:
    lr: float = 0.01
    batch_size: int = 32
    epochs: int = 10
```

等价于自动生成了：

```python
class TrainConfig:
    def __init__(self, lr: float = 0.01, batch_size: int = 32, epochs: int = 10):
        self.lr = lr
        self.batch_size = batch_size
        self.epochs = epochs

    def __repr__(self):
        return f"TrainConfig(lr={self.lr}, batch_size={self.batch_size}, epochs={self.epochs})"

    def __eq__(self, other):
        ...   # 按字段逐一比较
```

**什么时候用？** 配置项、参数打包（比如上面的训练超参数）、简单的数据容器——只存数据、没有复杂方法的类，优先用 `@dataclass`，不要手写重复的 `__init__`。**`nn.Module` 子类不适合用 `@dataclass`**：`nn.Module` 已经重写了 `__setattr__` 来做参数注册（见 [03_神经网络.md 第2节](./03_神经网络.md#2-定义网络以-lenet-5-为例逐层拆解)），`dataclass` 生成的 `__init__` 逻辑和这套机制没有冲突但也没有必要叠加，网络定义类还是按第10节的方式手写更清晰。

## 8. 继承相关：`super()`、方法重写、`isinstance`、多继承与 MRO、`abc.ABC`

### 8.1 基本语法

```python
class Animal:                    # 父类 / 基类
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} 发出声音"

class Dog(Animal):                # 子类继承父类，写在括号里
    pass

d = Dog("旺财")
print(d.speak())                    # "旺财 发出声音"——子类自动获得父类的方法和属性
```

### 8.2 `super()`：调用父类的方法

```python
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)       # 调父类的 __init__，把 name 的初始化逻辑复用过来
        self.breed = breed

    def speak(self):
        base = super().speak()        # 也可以在重写的方法里调用父类原本的实现
        return base + "，具体是汪汪叫"
```

`super()` 不是"调用某个具体的类"，而是按照**方法解析顺序（MRO，见8.5节）**找到"下一个"该调用的类——单继承时看不出区别，多继承时这一点特别重要。

### 8.3 方法重写（Override）：Python 没有方法重载（Overload）

子类定义一个和父类**同名**的方法，就会**覆盖**父类的版本——调用时优先用子类的：

```python
class Cat(Animal):
    def speak(self):                # 重写父类的 speak
        return f"{self.name} 喵喵叫"
```

**Python 没有方法重载**——不像 Java/C++ 那样可以定义多个同名但参数不同的方法，Python 里同名方法后定义的会直接覆盖前面的。想要"参数可变"的效果，用默认参数或 `*args`/`**kwargs`。

### 8.4 `isinstance()` / `issubclass()`：判断继承关系

```python
isinstance(d, Dog)      # True
isinstance(d, Animal)    # True——d 是 Dog，Dog 继承自 Animal，所以也是 Animal
issubclass(Dog, Animal)   # True
issubclass(Animal, Dog)   # False——反过来不成立
```

判断类型时优先用 `isinstance()`，不要用 `type(d) == Dog`——后者严格要求类型完全一致，无法识别继承关系，会破坏多态性。

### 8.5 多继承与 MRO（Method Resolution Order）

Python 支持多继承（一个类同时继承多个父类），查找方法/属性时按 **MRO（方法解析顺序）** 规则，遵循 **C3 线性化算法**：

```python
class A:
    def hello(self):
        print("A")

class B(A):
    def hello(self):
        print("B")

class C(A):
    def hello(self):
        print("C")

class D(B, C):     # 多继承：先 B 后 C
    pass

d = D()
d.hello()                # "B" —— 按 MRO 顺序，先找到 B 的 hello
print(D.mro())            # [D, B, C, A, object] —— 用 mro() 直接看查找顺序
```

**记忆规则**：大致是"深度优先，但同一个祖先只出现一次，且遵循括号里列出的顺序"——`class D(B, C)` 里 `B` 排在 `C` 前面，MRO 就会先查 `B` 这条线。不确定顺序时，直接打印 `ClassName.mro()` 看实际结果，比死记算法规则更可靠。

**多继承里 `super()` 会按 MRO 链式调用**，这是最容易搞混的地方：

```python
class B(A):
    def hello(self):
        print("B")
        super().hello()     # 这里调的不一定是 A，是 MRO 里 B 的下一个

class D(B, C):
    pass

D().hello()      # "B" -> "C" -> "A"，因为 MRO 是 [D, B, C, A, object]
```

### 8.6 抽象基类：`abc.ABC`

如果想定义一个"规定子类必须实现哪些方法，但自己不能被直接实例化"的基类，用 `abc.ABC` + `@abstractmethod`：

```python
from abc import ABC, abstractmethod

class Layer(ABC):
    @abstractmethod
    def forward(self, x):
        ...   # 只声明，不实现——强制子类必须重写

class MyLayer(Layer):
    def forward(self, x):
        return x * 2

Layer()      # TypeError：不能实例化抽象类
MyLayer()    # 正常
```

`nn.Module` 本身不是抽象类（它可以被直接实例化），但**约定俗成要求子类必须重写 `forward()`**——如果不重写，调用 `net(input)` 会因为父类默认的 `forward()` 抛 `NotImplementedError`，这是一种"软约束"，不像 `abc.ABC` 那样在实例化阶段就报错。

### 8.7 常见坑：忘记调用 `super().__init__()`

```python
class Base:
    def __init__(self):
        self.items = []          # 一定要在 __init__ 里创建，不要写成类属性（第3节讲过的坑）

class Child(Base):
    def __init__(self):
        super().__init__()        # 必须先调用，否则 self.items 根本不存在
        self.items.append("child专属")
```

**忘记调用 `super().__init__()`** 是继承里最常见的 bug 来源——父类 `__init__` 里创建的属性（比如 `nn.Module` 的参数注册字典，见 [03_神经网络.md](./03_神经网络.md)）如果没被执行，子类使用这些属性时会直接报错或者行为异常，而且往往不是"立刻报错"，是"用到那个属性的时候才报错"，排查起来比一般的 bug 更麻烦。

## 9. 类型注解

来自 **PEP 484**，给参数和返回值标注类型，不影响运行（Python 不做强制类型检查），但极大提升可读性，配合 IDE（PyCharm 的 `Ctrl+P`/`Ctrl+Q`）能给出更准确的自动补全和提示：

```python
class Net(nn.Module):
    def __init__(self, in_features: int, out_features: int = 10) -> None:
        super().__init__()
        self.fc = nn.Linear(in_features, out_features)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.fc(x)
```

`mypy` 这类工具可以静态检查类型注解是否自洽（比如传了个 `str` 给标注为 `int` 的参数会被 flag 出来），但这是可选的额外一层保障，不加类型注解代码依然能跑。

## 10. 对照 `class Net(nn.Module)`：规范逐条落地

回到 [03_神经网络.md](./03_神经网络.md) 里反复出现的这段代码，逐条对应上面讲的规范：

```python
class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, input):
        ...
        return output
```

| 代码 | 对应规范 |
|---|---|
| `class Net(nn.Module):` | 类名 `Net` 用 `CapWords`（第2节） |
| `super(Net, self).__init__()` | 继承时先调父类初始化（第4节）；等价于更简洁的 `super().__init__()` |
| `self.conv1 = nn.Conv2d(...)` | 实例属性用 `snake_case`，在 `__init__` 里赋值（第2、3节） |
| `def forward(self, input):` | 方法名 `snake_case`；重写父类约定的接口方法（第8.6节"软约束"） |
| 没有手写 `backward()` | 不是漏写，是 `nn.Module`/autograd 机制决定不需要（见 [03_神经网络.md](./03_神经网络.md) 第2节说明） |
| 调用写 `net(input)` 不是 `net.forward(input)` | 因为 `nn.Module` 重写了 `__call__`（第6节） |

**这里没有用 `@dataclass`、没有用 `@property`、没有用 `abc.ABC`**——不是规范要求必须避免，而是这几种工具解决的是"纯数据存储"、"受控属性访问"、"强制子类实现接口"这几类特定问题，`Net` 这个类的核心诉求是"注册可学习层 + 定义前向计算"，用最朴素的 `__init__` + `forward` 组合就是最贴切的写法——**规范不是"越花哨越好"，是"用最匹配当前需求的那一种"**。

## 11. 工具：自动检查与格式化

| 工具 | 作用 |
|---|---|
| `black` | 自动格式化代码（空格、空行、引号风格……），不用手动纠结格式细节 |
| `flake8` / `pylint` | 静态检查命名、未使用变量、是否符合 PEP 8 等问题 |
| `mypy` | 检查类型注解是否自洽（第9节） |
| PyCharm 内置检查 | 编辑器实时标黄/标红不符合 PEP 8 的写法，也能一键格式化 |

日常写代码不需要背熟所有 PEP 8 条款，跑一遍 `black` + `flake8` 基本能覆盖大部分格式问题。

## 12. 要点小结

- **PEP 8 是 Python 代码风格的官方基准**，类名用 `CapWords`，方法/属性名用 `snake_case`。
- **`__init__` 负责初始化，不是"构造"本身**；继承时第一行几乎总是 `super().__init__()`，跳过会导致父类依赖的内部状态缺失。
- **属性访问优先用普通字段或 `@property`，不用 `get_x()`/`set_x()`**——只有需要校验或计算派生值时才上 `@property`，不要为每个字段都套一层。
- **`__repr__` 建议每个类都写**，其余 dunder 方法（`__eq__`、`__len__`、`__call__`……）按需实现，`nn.Module` 能写 `net(input)` 正是靠重写了 `__call__`。
- **纯数据类用 `@dataclass` 省去重复的 `__init__`/`__repr__`**，但像 `nn.Module` 子类这种有特殊 `__setattr__` 机制、以计算逻辑为主的类，手写更清晰，不需要强套。
- **`super()` 用来复用父类逻辑，方法重写直接覆盖同名方法（Python 没有重载）**；判断继承关系用 `isinstance()`/`issubclass()`，不要用 `type() ==`。
- **多继承时方法查找顺序由 MRO 决定**，不确定顺序就打印 `ClassName.mro()` 看实际结果，`super()` 在多继承里是按 MRO 链式调用，不是"调父类"那么简单。
- **需要"强制子类必须实现某方法"时用 `abc.ABC` + `@abstractmethod`**；`nn.Module` 的 `forward()` 只是约定俗成的"软约束"，不实例化检查，运行时才报错。忘记调用 `super().__init__()` 是继承里最常见的 bug 来源。
- **类型注解（PEP 484）不影响运行，但提升可读性和 IDE 提示质量**，`mypy` 可选做静态检查。
- **规范的核心是"匹配需求"，不是"用满所有工具"**——`class Net(nn.Module)` 这个例子只用了最基础的 `__init__` + `forward`，已经是最贴切的写法，见第10节逐条对照。
