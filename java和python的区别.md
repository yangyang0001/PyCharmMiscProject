# Java 和 Python 的区别

> 面向有 Java 基础、正在学习 Python 的读者，从语法到工程使用规范做对比。

## 1. 基本定位

<table>
<tr><th></th><th>Java</th><th>Python</th></tr>
<tr><td>类型</td><td>静态类型、编译型（编译为字节码，JVM 运行）</td><td>动态类型、解释型</td></tr>
<tr><td>设计哲学</td><td>强规范、显式声明一切</td><td>简洁、"用缩进代替花括号"</td></tr>
<tr><td>典型场景</td><td>大型企业系统、Android</td><td>脚本、数据科学、AI、自动化、后端 Web</td></tr>
</table>

## 2. 语法层面差异

### 2.1 代码块与语句结束

**Java：**
```java
// Java：花括号 + 分号
if (x > 0) {
    System.out.println("positive");
}
```

**Python：**
```python
# Python：冒号 + 缩进，无分号
if x > 0:
    print("positive")
```

- Java 花括号定界代码块，缩进只是风格，不影响语义。
- **Python 缩进是语法的一部分**，缩进错误会直接报 `IndentationError`。同一代码块必须使用一致的缩进（推荐 4 个空格，不要混用 Tab）。

### 2.2 变量与类型

**Java：**
```java
int age = 18;
String name = "Tom";
final double PI = 3.14; // 常量
```

**Python：**
```python
age = 18
name = "Tom"
PI = 3.14  # 没有真正的常量，全大写只是约定，本质仍可被改
```

- Java 必须显式声明类型（`var` 是 Java 10+ 的局部类型推断，仍是静态类型，编译期确定）。
- Python 变量无需声明类型，类型信息挂在**对象**上而不是**变量**上，同一个变量名可以先后指向不同类型的对象。
- Python 类型注解（`age: int = 18`）只是提示，不做强制运行时检查（需要 mypy 等工具才能检查）。

### 2.3 注释

**Java：**
```java
// 单行注释
/* 多行注释 */
/** Javadoc 文档注释 */
```

**Python：**
```python
# 单行注释
"""
多行字符串常被当作注释使用
函数/类下面第一行的字符串会成为 docstring
"""
```

### 2.4 字符串

- Java 字符串用 `"双引号"`，字符用 `'单引号'`（`char` 是单独类型）。
- Python 没有 `char` 类型，单字符就是长度为 1 的字符串；单引号和双引号完全等价。
- Python 有 f-string（`f"{name} is {age}"`），比 Java 的 `String.format` / 字符串拼接更简洁。

### 2.5 数组 / 集合

**Java：**
```java
int[] arr = {1, 2, 3};
List<Integer> list = new ArrayList<>();
list.add(1);
```

**Python：**
```python
arr = [1, 2, 3]      # list：可变、动态长度、可混类型
t = (1, 2, 3)        # tuple：不可变
d = {"a": 1}         # dict，对应 Java 的 Map
s = {1, 2, 3}        # set
```

- Java 数组定长，`List` 才是动态集合，需要显式泛型 `<Integer>`。
- Python 的 `list` 天生动态、可放任意类型的元素，没有类似 Java 数组/`ArrayList` 的区分。

### 2.6 函数 / 方法

**Java：**
```java
public static int add(int a, int b) {
    return a + b;
}
```

**Python：**
```python
def add(a: int, b: int) -> int:
    return a + b
```

- Java 方法必须属于某个类；Python 函数可以独立于类存在（模块级函数）。
- Java 方法签名里的类型是强制的；Python 的类型注解仅为提示。
- Python 支持默认参数、关键字参数、可变参数更灵活：

**Python：**
```python
def greet(name, greeting="Hello", *args, **kwargs):
    print(f"{greeting}, {name}")
```

### 2.7 空值

- Java：`null`
- Python：`None`（首字母大写，是单例对象，用 `is None` 判断而不是 `== None`）

### 2.8 布尔与相等性

- Java：`true` / `false`；`==` 比较对象引用（基本类型除外），比较内容要用 `.equals()`。
- Python：`True` / `False`（首字母大写）；`==` 默认比较内容（依赖 `__eq__`），比较是否为同一对象用 `is`。

## 3. 面向对象差异

### 3.1 类定义

**Java：**
```java
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }
}
```

**Python：**
```python
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def get_name(self) -> str:
        return self.name
```

- Java 构造方法名与类名相同；Python 用固定的 `__init__`。
- Java 实例方法隐式拿到 `this`；Python **必须显式声明 `self`** 作为第一个参数。
- Java 一个文件通常只放一个 `public class`，且**文件名必须和类名一致**；Python 一个 `.py` 文件可以放任意多个类/函数，文件名与类名无关。

### 3.2 访问修饰符

<table>
<tr><th>Java</th><th>Python</th></tr>
<tr><td><code>public</code> / <code>protected</code> / <code>private</code> / (默认包级)</td><td>没有真正的访问控制</td></tr>
<tr><td>编译器强制检查</td><td>全靠<strong>命名约定</strong>：<code>_name</code>（约定内部使用，仍可访问）、<code>__name</code>（触发 name mangling，非严格私有）</td></tr>
</table>

Python 信奉"我们都是成年人"（consenting adults）的哲学：不用语言强制私有，靠约定和文档自律。

### 3.3 接口 / 抽象类 / 多态

- Java：`interface`、`abstract class` 是一等语法，`implements` / `extends` 关键字明确。
- Python：没有 `interface` 关键字，靠 `abc` 模块的 `ABC` + `@abstractmethod` 实现类似效果；更常用**鸭子类型**（duck typing）——不关心类型，只要对象有对应方法就能用。
- Java 是单继承（类）+ 多接口；Python **原生支持多重继承**（`class C(A, B):`），方法解析顺序（MRO）用 C3 线性化算法。

### 3.4 重载

- Java 支持方法重载（同名不同参数列表）。
- Python **不支持重载**，同名方法后定义的会覆盖前面的；一般用默认参数 / `*args` / `**kwargs` / `functools.singledispatch` 代替。

## 4. 包 / 模块系统

<table>
<tr><th></th><th>Java</th><th>Python</th></tr>
<tr><td>组织单位</td><td>package（对应目录结构，需与目录路径严格一致）</td><td>module（<code>.py</code> 文件）/ package（含 <code>__init__.py</code> 的目录）</td></tr>
<tr><td>顶层包</td><td>语言不强制，约定用反向域名（<code>com.example.app</code>）避免冲突</td><td>语言不强制，约定一个项目一个顶层包（详见前文讨论）</td></tr>
<tr><td>引入方式</td><td><code>import com.example.util.Helper;</code></td><td><code>import module</code> / <code>from package import module</code></td></tr>
<tr><td>依赖管理</td><td>Maven / Gradle（<code>pom.xml</code> / <code>build.gradle</code>）</td><td>pip / poetry / uv（<code>requirements.txt</code> / <code>pyproject.toml</code>）</td></tr>
<tr><td>环境隔离</td><td>通常共享 JDK，靠构建工具管理依赖范围</td><td>强调虚拟环境（<code>venv</code>/<code>conda</code>），每个项目物理隔离依赖</td></tr>
</table>

## 5. 异常处理

**Java：**
```java
try {
    doSomething();
} catch (IOException e) {
    log.error(e);
} finally {
    cleanup();
}
```

**Python：**
```python
try:
    do_something()
except IOError as e:
    log.error(e)
finally:
    cleanup()
```

- Java 有**受检异常**（checked exception），方法签名必须用 `throws` 声明，调用方强制处理或继续抛出。
- Python **没有受检异常**，所有异常都类似 Java 的 `RuntimeException`（非受检），不强制捕获。
- Python 额外有 `else` 子句：`try / except / else / finally`，`else` 在没有异常时执行。

## 6. 使用规范对比

### 6.1 命名规范

<table>
<tr><th></th><th>Java</th><th>Python</th></tr>
<tr><td>类名</td><td><code>PascalCase</code>（如 <code>UserService</code>）</td><td><code>PascalCase</code>（如 <code>UserService</code>）</td></tr>
<tr><td>方法/函数名</td><td><code>camelCase</code>（如 <code>getUserName</code>）</td><td><code>snake_case</code>（如 <code>get_user_name</code>，PEP 8）</td></tr>
<tr><td>变量名</td><td><code>camelCase</code></td><td><code>snake_case</code></td></tr>
<tr><td>常量</td><td><code>UPPER_SNAKE_CASE</code></td><td><code>UPPER_SNAKE_CASE</code></td></tr>
<tr><td>包/模块名</td><td>全小写，如 <code>com.example.util</code></td><td>全小写+下划线，如 <code>my_utils</code>（不推荐驼峰）</td></tr>
</table>

### 6.2 官方风格指南

- Java：没有语言级官方规范，业界事实标准是 Google Java Style Guide / 阿里巴巴 Java 开发手册等。
- Python：官方 **PEP 8**（Style Guide for Python Code）事实上是标准规范，工具链（`flake8`、`black`、`ruff`）都以此为基准。

### 6.3 格式化 / Lint 工具

<table>
<tr><th></th><th>Java</th><th>Python</th></tr>
<tr><td>格式化</td><td>Checkstyle、Spotless</td><td><code>black</code>、<code>autopep8</code></td></tr>
<tr><td>静态检查</td><td>SpotBugs、SonarQube</td><td><code>pylint</code>、<code>flake8</code>、<code>mypy</code>（类型检查）</td></tr>
<tr><td>测试框架</td><td>JUnit</td><td><code>pytest</code>、<code>unittest</code></td></tr>
</table>

### 6.4 入口写法

**Java：**
```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

**Python：**
```python
def main():
    print("Hello")

if __name__ == "__main__":
    main()
```

- Java 程序必须有 `public static void main(String[] args)` 作为唯一入口。
- Python 脚本从上到下顺序执行，`if __name__ == "__main__":` 只是约定俗成的写法，用来区分"直接运行"和"被 import"两种场景，并非语言强制。

## 7. 常见"陷阱"提醒（从 Java 转 Python 容易踩的坑）

1. **可变默认参数陷阱**：`def f(items=[])` 中的 `[]` 只会被创建一次，多次调用会共享同一个列表，应写成 `def f(items=None): items = items or []`。
2. **缩进错误**：Tab 和空格混用会报错，IDE 建议统一设置为 4 空格。
3. **`==` vs `is`**：判断值相等用 `==`，判断是否为同一对象（尤其 `None`）用 `is`。
4. **私有变量不是真私有**：`__name` 只是被改写成 `_ClassName__name`，仍可访问，不要以为等同 Java 的 `private`。
5. **没有编译期类型检查**：Java 的很多错误在编译期就能发现，Python 同类错误往往要运行到那一行才报错，因此更依赖单元测试和类型注解（`mypy`）。
6. **一切皆对象、动态类型**：同一个变量可以先赋值为 `int` 再赋值为 `str`，Java 完全不允许这种写法。

## 8. Python 特有、Java 没有对应概念的东西

> 以下是 Java 里完全找不到直接对应物、或者概念上有本质区别的 Python 特性，用红字标出。

### 8.1 <span style="color:red">列表 / 字典 / 集合推导式（Comprehension）</span>

```python
squares = [x * x for x in range(10) if x % 2 == 0]
d = {k: v for k, v in zip(keys, values)}
```
Java 只能用 for 循环 + Stream API 拼凑出类似效果（`stream().filter().map().collect()`），远不如推导式简洁，也不是语言原生语法。

### 8.2 <span style="color:red">生成器（Generator）与 `yield`</span>

```python
def counter(n):
    i = 0
    while i < n:
        yield i
        i += 1
```
函数一旦包含 `yield`，调用它不会立即执行，而是返回一个惰性迭代器，每次 `next()` 才继续执行到下一个 `yield`。Java 没有对应语法（Java 的 `Stream` 是不同的实现方式，`Iterator` 需要手写状态机）。

### 8.3 <span style="color:red">装饰器（Decorator，`@xxx`）</span>

```python
@staticmethod
@property
@functools.lru_cache
def compute(x):
    ...
```
本质是"函数包装函数"的语法糖，可以在不改动原函数代码的前提下增强/修改行为。Java 的注解（`@Override`）只是元数据标记，不会改变方法的实际执行逻辑，两者概念完全不同。

### 8.4 <span style="color:red">切片（Slicing）</span>

```python
a = [0, 1, 2, 3, 4, 5]
a[1:3]     # [1, 2]
a[::-1]    # 反转：[5, 4, 3, 2, 1, 0]
a[::2]     # 步长取值
```
Java 数组/List 没有切片语法，只能手写循环或调用 `subList()`。

### 8.5 <span style="color:red">多重赋值 / 解包（Unpacking）</span>

```python
a, b = 1, 2
a, b = b, a          # 交换变量，无需中间变量
first, *rest = [1, 2, 3, 4]   # rest = [2, 3, 4]
```
Java 交换两个变量必须借助临时变量，也没有类似的解包语法。

### 8.6 <span style="color:red">一切皆对象，函数是一等公民（First-class function）</span>

函数、类本身都可以像普通变量一样被赋值、传参、作为返回值：
```python
def add(a, b): return a + b
op = add
funcs = [add, len, print]
```
Java 8 之后有 Lambda / 方法引用，但仍受"函数式接口"限制，不像 Python 里函数可以直接当对象随意传递。

### 8.7 <span style="color:red">魔术方法 / 运算符重载（Dunder methods）</span>

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __str__(self):
        return f"({self.x}, {self.y})"
```
通过实现 `__add__`、`__eq__`、`__len__`、`__getitem__` 等特殊方法，可以让自定义类支持 `+`、`==`、`len()`、`obj[i]` 等原生运算符。**Java 不支持运算符重载**。

### 8.8 <span style="color:red">上下文管理器 / `with` 语句</span>

```python
with open("a.txt") as f:
    data = f.read()
```
自动调用对象的 `__enter__` / `__exit__` 完成资源获取与释放。Java 的 `try-with-resources` 语法效果类似，但 Python 的 `with` 是通过实现 `__enter__/__exit__` 协议实现的通用机制，能用于任何自定义资源，不仅限于 `Closeable`。

### 8.9 <span style="color:red">鸭子类型（Duck Typing）</span>

不关心对象的具体类型，只要它实现了需要的方法就能用：
```python
def render(shape):
    shape.draw()   # 只要有 draw() 方法就行，不管是不是同一个基类
```
Java 是强类型语言，必须显式实现接口或继承才能这样传参。

### 8.10 <span style="color:red">GIL（全局解释器锁）</span>

CPython 解释器同一时刻只允许一个线程执行 Python 字节码，导致多线程无法利用多核做 CPU 密集型并行计算（需要用多进程 `multiprocessing` 绕过）。Java 线程是真正的操作系统级并行，没有这个限制。

### 8.11 <span style="color:red">海象运算符 `:=`（Python 3.8+）</span>

```python
if (n := len(data)) > 10:
    print(f"数据量过大: {n}")
```
在表达式内部完成赋值并立即使用，Java 没有等价写法。

### 8.12 <span style="color:red">链式比较</span>

```python
if 0 < x < 10:
    ...
```
等价于 `0 < x and x < 10`，Java 必须拆成两个条件用 `&&` 连接。

### 8.13 <span style="color:red">动态添加/删除属性（Monkey Patching）</span>

```python
p = Person("Tom", 18)
p.nickname = "T"     # 运行时给实例动态加属性，Person 类本身没定义过
```
Java 对象的字段结构在编译期就固定死了，运行时不能给实例任意加字段。

### 8.14 <span style="color:red">交互式解释器（REPL）</span>

直接在终端敲 `python` 就能进入交互环境，逐行执行代码、即时看到结果，非常适合探索式调试。Java 没有这种开箱即用的交互模式（`jshell` 是 Java 9 之后才补上的类似功能）。
