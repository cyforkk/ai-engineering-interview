# -*- coding: utf-8 -*-
"""Python：按超高/高/中/低频完整卷 + 频率导航。不碰面渣。"""
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def w(name, text):
    p = DOCS / name
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print(name, p.stat().st_size)


NAV = """<!-- NAV:START -->
> 📖 **Python 完整卷** · 🗣️ [面渣](./Python面渣级口述.md) · [异步FastAPI](./Python异步与FastAPI面渣级口述.md) · 🃏 [卡片](./Python卡片速记.md) · 🔥 [频率](./Python八股频率排序.md)
>
> [路径 C](./路径-Python.md) · [手写题](./Python手写题.md) · [四档主线](./Java后端面试频率-四档.md)
>
<!-- NAV:END -->
"""

MAIN = f"""# Python · 高频八股知识点（完整卷）

{NAV}

> 2025–2026 大厂 + AI/后端岗：重 **语言特性、底层原理、实际使用**。  
> 能结合代码讲清；手写见 [Python手写题.md](./Python手写题.md)。

### 专项时间占比

| 优先级 | 模块 | 时间 |
|--------|------|:----:|
| **P0** | 数据类型底层 + 装饰器 + 生成器/迭代器 + GIL + 深浅拷贝 | **45%** |
| **P1** | OOP（魔法方法、classmethod）+ GC + 闭包 | **25%** |
| **P2** | 并发模型 + with + 标准库 | **15%** |
| **P3** | 元类、描述符、异步、性能 | **15%** |

### 高效准备

1. **能手写**：装饰器、生成器、深浅拷贝、单例、上下文管理器  
2. **讲原理**：GIL 为何存在、dict 为何快、生成器如何省内存  
3. **结合项目**：装饰器做日志/鉴权、生成器读大文件、多进程 CPU 任务  
4. AI/数据岗：生成器、装饰器、类型注解、asyncio、numpy/pandas 差异  
5. 后端岗：GIL、多进程、协程、性能、与 Java/Go 对比  

---

# 一、超高频（几乎必问）

## 1. 数据类型与底层

### 1.1 list / tuple / dict / set？

| 类型 | 可变 | 有序* | 底层直觉 | 场景 |
|------|------|-------|----------|------|
| list | ✓ | 有序 | 动态数组 | 序列、可变列表 |
| tuple | ✗ | 有序 | 定长数组 | 不可变、作 dict 键（元素可哈希时） |
| dict | ✓ | 3.7+ 插入有序 | **哈希表** | KV 映射 |
| set | ✓ | 无序 | 哈希集合 | 去重、成员检测 |

\\*有序指元素顺序；set 无序。

### 1.2 可变 vs 不可变？

| 不可变 | 可变 |
|--------|------|
| int、float、str、tuple、frozenset | list、dict、set、自定义对象（默认可变） |

- **影响**：不可变可哈希（一般）→ 可作 dict 键；可变作键会错乱  
- 默认参数陷阱：`def f(a=[])` 共享同一 list  

### 1.3 深拷贝 vs 浅拷贝？

| | 浅 copy.copy | 深 copy.deepcopy |
|--|--------------|------------------|
| 外层 | 新对象 | 新对象 |
| 内层可变 | **共享引用** | **递归复制** |

```python
import copy
a = [[1], 2]
b = copy.copy(a)      # b[0] is a[0]
c = copy.deepcopy(a)  # 完全独立
```

### 1.4 dict 底层？键为何可哈希？

- 开放寻址法 / 哈希表（CPython 实现细节随版本演进）  
- 键 → hash → 定位桶；冲突再探测  
- **可哈希**：`__hash__` 稳定且与 `__eq__` 一致；可变对象 hash 会变 → 不能作键  

### 1.5 list vs tuple 场景？

- list：要增删改  
- tuple：固定结构、作字典键、函数多返回值、更轻量不可变约定  

---

## 2. 函数与高级特性

### 2.1 *args / **kwargs？

- `*args`：多余位置参数 → 元组  
- `**kwargs`：多余关键字参数 → 字典  
- 用于通用包装、转发参数  

### 2.2 装饰器原理？带参数装饰器？

- 装饰器 = 接收函数、返回函数的高阶函数  
- `@dec` ≡ `f = dec(f)`  
- **带参数**：三层嵌套 `decorator(args)(func)(*a,**k)`  
- 用 `functools.wraps` 保留元数据  

```python
from functools import wraps
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper
```

### 2.3 闭包？

- 内层函数引用外层变量，外层返回内层 → 闭包  
- 场景：装饰器、工厂函数、数据隐藏  
- 注意循环变量绑定（用默认参数绑当前值）  

### 2.4 生成器 vs 迭代器？yield？

| | 迭代器 | 生成器 |
|--|--------|--------|
| 协议 | `__iter__` + `__next__` | 用 yield 写的迭代器 |
| 内存 | 可一次持有 | **惰性**，逐个产出 |

- `yield`：暂停函数，产出值，保留状态  
- 大文件、流式数据 → 生成器  

### 2.5 推导式 vs 生成器表达式？

| 写法 | 结果 | 内存 |
|------|------|------|
| `[x for x in it]` | list | 全量 |
| `(x for x in it)` | generator | 惰性 |
| `{{k:v for ...}}` | dict | 全量 |
| `{{x for ...}}` | set | 全量 |

---

## 3. 面向对象

### 3.1 新式类 vs 旧式类？

- Py2：旧式/新式；**Py3 全是新式类**（默认继承 object）  

### 3.2 __new__ vs __init__？

| | __new__ | __init__ |
|--|---------|----------|
| 时机 | **创建**实例 | 初始化实例 |
| 返回 | 实例（或其它） | None |
| 用途 | 单例、不可变定制 | 常规初始化 |

### 3.3 staticmethod / classmethod / 实例方法？

| | 第一个参数 | 用途 |
|--|------------|------|
| 实例方法 | self | 访问实例 |
| classmethod | cls | 工厂方法、替代构造 |
| staticmethod | 无 | 工具函数挂在类上 |

### 3.4 类变量 vs 实例变量？

- 类变量：类共享  
- 实例变量：`self.x` 每实例一份  
- 可变类变量（list）被共享 → 易踩坑  

### 3.5 MRO？

- 多继承方法查找顺序  
- C3 线性化；`ClassName.__mro__` / `mro()`  
- 保证单调、本地优先  

### 3.6 常用魔法方法？

| 方法 | 作用 |
|------|------|
| __str__ / __repr__ | 可读/调试字符串 |
| __call__ | 实例可调用 |
| __enter__ / __exit__ | with 协议 |
| __len__ / __getitem__ | 容器 |
| __eq__ / __hash__ | 相等与哈希 |

---

## 4. 并发与内存

### 4.1 GIL？

- **Global Interpreter Lock**：CPython 同一时刻通常只有一个线程执行 Python 字节码  
- **为何**：简化内存管理与 C 扩展安全（历史设计）  
- **规避**：  
  - CPU 密集 → **多进程** / 推 C 扩展 / 外部服务  
  - IO 密集 → 多线程仍有用（等 IO 释 GIL）  
  - 高并发网络 → **asyncio**  

### 4.2 多线程 / 多进程 / 协程？

| | 适合 | 注意 |
|--|------|------|
| 线程 | IO 密集 | 受 GIL；要锁 |
| 进程 | CPU 密集 | 内存与通信贵 |
| 协程 | 高并发 IO | 不能阻塞事件循环 |

### 4.3 垃圾回收？

- **引用计数**主机制  
- **标记-清除**解决容器循环引用  
- **分代回收**优化  
- `gc` 模块可调、可调试  

### 4.4 循环引用？

- 两对象互相引用，计数不归零  
- 由 **循环 GC** 处理；也可用 `weakref`  

---

## 5. 其他超高频

### 5.1 值传递还是引用传递？

- 对象引用的 **赋值传递**（传的是引用的值）  
- 不可变“改绑”不影响外部；可变原地改影响外部  

### 5.2 is vs ==？

| is | == |
|----|-----|
| 同一对象（id） | 值相等（__eq__） |
| 小整数/短字符串可能驻留 | 业务比内容用 == |

### 5.3 上下文管理器 with？

```python
with open(path) as f:
    ...
# 等价 __enter__ / __exit__，异常也清理
```

- 自定义：类实现协议，或 `@contextmanager`  

### 5.4 异常最佳实践？

- 捕具体异常，勿裸 `except:`  
- `else` / `finally`；`raise ... from`  
- 自定义：`class AppError(Exception): ...`  

---

# 二、高频

## 6. 语言特性

### LEGB 作用域

```text
Local → Enclosing → Global → Built-in
```

### global / nonlocal

| global | nonlocal |
|--------|----------|
| 改模块全局 | 改外层非全局闭包变量 |

### lambda

- 单表达式匿名函数；场景：排序 key、简短回调  
- 限制：不能语句块；可读性差时别滥用  

### 函数式

- `map` / `filter` / `functools.reduce` / `partial`  
- 现代更常用推导式与生成器  

### 元类 metaclass

- 创建类的类；`type` 是默认元类  
- 场景：ORM、API 注册、框架约束  

### __slots__

- 限制实例属性集合，减 `__dict__`，省内存  
- 继承与动态属性受限  

---

## 7. 模块与包

### if __name__ == '__main__'

- 直接运行时为 `'__main__'`；被 import 时是模块名  
- 放脚本入口，避免 import 副作用  

### 导入

- 绝对导入推荐；相对 `from . import x`  
- 注意循环导入  

### 常用标准库

| 库 | 用途 |
|----|------|
| collections | defaultdict、Counter、deque… |
| itertools | 迭代工具 |
| functools | wraps、lru_cache、partial |
| os / sys / pathlib | 系统与路径 |
| json / re / datetime | 数据与时间 |
| concurrent.futures | 线程/进程池 |
| asyncio | 异步 |

---

## 8. 性能与优化

| 手段 | 说明 |
|------|------|
| 算法与数据结构 | 第一位 |
| 生成器/流式 | 大文件省内存 |
| 字符串 join | 避免循环 `+` |
| 多进程/C 扩展 | CPU 密集 |
| pypy / 向量化 | 场景可选 |

### 分析工具

- `cProfile`、`line_profiler`、`memory_profiler`、`py-spy`  

### Py2 vs Py3（若问）

- print 函数、默认 Unicode、range、整数除法等  

### 鸭子类型

- 不看类型名，看有没有所需方法/行为  

### 迭代器协议

- `__iter__` 返回 self 或新迭代器；`__next__` 产出或 StopIteration  

### 描述符 Descriptor

- `__get__` / `__set__` / `__delete__`  
- property、classmethod 底层相关  

---

# 三、中频

## 9. 异步 asyncio

- `async def` + `await`；事件循环调度协程  
- **禁忌**：协程里同步阻塞（`time.sleep`、同步 requests）  
- 用 `asyncio.sleep`、httpx/aiohttp  
- 详见：[Python异步与FastAPI面渣](./Python异步与FastAPI面渣级口述.md)  

## 10. 类型注解

- `def f(x: int) -> str`；`list[int]`、`Optional`、`Protocol`  
- 静态检查（mypy）；运行时不强制（除非用工具）  

## 11. 单例

| 方式 | 注意 |
|------|------|
| 模块级 | 最简单常用 |
| __new__ | 注意并发 |
| 装饰器/元类 | 灵活 |

## 12. 装饰器场景

- 日志、鉴权、缓存（`lru_cache`）、计时、重试  

## 13. collections / itertools

| 类型 | 用途 |
|------|------|
| defaultdict | 默认工厂 |
| Counter | 计数 |
| deque | 双端队列 |
| namedtuple / dataclass | 轻量结构 |
| OrderedDict | 历史有序（3.7+ dict 已有序） |

## 14. 测试

- unittest / **pytest**  
- fixture、mock  

---

# 四、低频 / 进阶

- gc 分代细节、`gc.get_referrers`  
- 协程 = 生成器演进 + 事件循环  
- CPython vs PyPy（JIT）vs Jython  
- Cython / ctypes / cffi  
- 元编程、async + 线程池混合  
- mypy 与运行时校验  

---

# 岗位侧重

| 方向 | 加分 |
|------|------|
| AI/数据 | 生成器、装饰器、typing、asyncio、numpy 内存视图直觉 |
| 后端 | GIL、进程、协程、FastAPI、性能、与 Java 对比 |

---

# 自测清单

### P0
- [ ] list/dict/set 底层与场景  
- [ ] 可变不可变 + 默认参数坑  
- [ ] 浅深拷贝代码  
- [ ] 装饰器（含 wraps）  
- [ ] yield 生成器  
- [ ] GIL 选型三句话  

### P1
- [ ] new/init、classmethod  
- [ ] MRO 一句  
- [ ] GC 引用计数+循环  
- [ ] 闭包  

### P2–P3
- [ ] with 协议  
- [ ] 线程/进程/协程  
- [ ] asyncio 禁阻塞  
- [ ] join vs +  

**口述：** [Python面渣级口述.md](./Python面渣级口述.md) · [异步FastAPI](./Python异步与FastAPI面渣级口述.md)  
**手写：** [Python手写题.md](./Python手写题.md)  
**卡片：** [Python卡片速记.md](./Python卡片速记.md)  
**频率：** [Python八股频率排序.md](./Python八股频率排序.md)  

---

## 点名深挖

- 装饰器完整 + 带参数  
- GIL 详解与规避  
- 生成器 vs 迭代器 + 代码  
- 深浅拷贝完整对比  
- 垃圾回收机制  

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 按超高/高/中/低频大纲写 Python 完整卷 |
"""

RANK = f"""# Python · 频率导航（2025–2026）

> **完整卷：** [Python高频面试题与知识点.md](./Python高频面试题与知识点.md)  
> **面渣：** [Python面渣级口述.md](./Python面渣级口述.md) · [异步FastAPI](./Python异步与FastAPI面渣级口述.md)  
> **卡片：** [Python卡片速记.md](./Python卡片速记.md) · **手写：** [Python手写题.md](./Python手写题.md)  
> **路径：** [路径-Python.md](./路径-Python.md)

---

## 专项时间

| 优先级 | 模块 | 时间 |
|--------|------|:----:|
| P0 | 数据类型 + 装饰器 + 生成器 + GIL + 拷贝 | **45%** |
| P1 | OOP + GC + 闭包 | 25% |
| P2 | 并发模型 + with + 标准库 | 15% |
| P3 | 元类/描述符/异步/性能 | 15% |

---

## 一、超高频

| # | 主题 | 入口 |
|---|------|------|
| 1 | list/dict/set 底层、可变不可变、深浅拷贝 | [§1](./Python高频面试题与知识点.md) |
| 2 | args/kwargs、装饰器、闭包、生成器 | [§2](./Python高频面试题与知识点.md) |
| 3 | OOP：new/init、classmethod、MRO、魔法方法 | [§3](./Python高频面试题与知识点.md) |
| 4 | GIL、多线程/进程/协程、GC | [§4](./Python高频面试题与知识点.md) |
| 5 | 传参、is/==、with、异常 | [§5](./Python高频面试题与知识点.md) |

---

## 二、高频

LEGB · global/nonlocal · lambda · 元类 · slots · 模块导入 · 性能 · 鸭子类型 · 描述符  

---

## 三、中频

asyncio · typing · 单例 · collections · pytest  

---

## 四、低频

gc 细节 · PyPy · Cython · mypy  

---

## 必须能手写

```text
装饰器（wraps）· 生成器 · 深浅拷贝 · 单例 · 上下文管理器
```

---

## 点名

`装饰器` · `GIL` · `生成器` · `深浅拷贝` · `垃圾回收`

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | Python 专项频率导航 |
"""

CARDS = f"""# Python · 卡片速记

<!-- NAV:START -->
> [完整卷](./Python高频面试题与知识点.md) · [频率](./Python八股频率排序.md) · [面渣](./Python面渣级口述.md)
<!-- NAV:END -->

> 遮住 A。**先 P0。**

---

## 数据类型

**Q1 list vs tuple？** A: 可变序列 vs 不可变；tuple 可作键（元素可哈希）。

**Q2 dict 底层？** A: 哈希表；键须可哈希。

**Q3 可变不可变？** A: list/dict/set vs int/str/tuple。

**Q4 默认参数坑？** A: 可变默认只创建一次；用 None。

**Q5 浅拷贝深拷贝？** A: 内层共享 vs 递归复制。

## 函数

**Q6 *args **kwargs？** A: 位置元组 / 关键字字典。

**Q7 装饰器？** A: 函数包函数；@ 语法糖；wraps。

**Q8 闭包？** A: 内函数引用外变量并返回。

**Q9 yield？** A: 生成器惰性产出。

**Q10 列表推导 vs 生成器表达式？** A: 全量 list vs 惰性。

## OOP / 并发

**Q11 __new__ vs __init__？** A: 创建 vs 初始化。

**Q12 classmethod vs staticmethod？** A: 收 cls / 无强制实例。

**Q13 GIL？** A: 同进程同时一线程跑字节码；CPU用进程。

**Q14 线程进程协程？** A: IO / CPU / 高并发IO。

**Q15 GC？** A: 引用计数+循环检测+分代。

## 其他

**Q16 is vs ==？** A: 同一对象 vs 相等。

**Q17 with？** A: enter/exit 保证清理。

**Q18 LEGB？** A: Local Enclosing Global Builtin。

**Q19 字符串拼接？** A: join 优于循环 +。

**Q20 asyncio 禁忌？** A: 协程里阻塞调用。

---

详解：[Python高频面试题与知识点.md](./Python高频面试题与知识点.md) · 手写：[Python手写题.md](./Python手写题.md)
"""


def patch():
    path = DOCS / "路径-Python.md"
    if path.exists():
        t = path.read_text(encoding="utf-8")
        if "Python八股频率排序" not in t:
            t = t.replace(
                "[详解](./Python高频面试题与知识点.md)",
                "[**完整卷**](./Python高频面试题与知识点.md)·[频率](./Python八股频率排序.md)",
            )
            t = t.replace(
                "[知](./Python高频面试题与知识点.md)",
                "[完整卷](./Python高频面试题与知识点.md)·[频率](./Python八股频率排序.md)",
            )
            if "Python八股频率排序" not in t:
                t = t.replace(
                    "**读法：**",
                    "**Python 完整卷：** [知识点](./Python高频面试题与知识点.md) · [频率](./Python八股频率排序.md) · [卡片](./Python卡片速记.md)\n\n**读法：**",
                )
            path.write_text(t, encoding="utf-8")
            print("path")

    sb = DOCS / "_sidebar.md"
    if sb.exists():
        t = sb.read_text(encoding="utf-8")
        if "Python八股频率排序" not in t:
            t = t.replace(
                "  * [Python 详解](Python高频面试题与知识点.md)\n"
                "  * [异步 FastAPI 口述](Python异步与FastAPI面渣级口述.md)\n",
                "  * [Python 完整卷](Python高频面试题与知识点.md)\n"
                "  * [Python 频率](Python八股频率排序.md)\n"
                "  * [异步 FastAPI 口述](Python异步与FastAPI面渣级口述.md)\n",
            )
            sb.write_text(t, encoding="utf-8")
            print("sidebar")

    readme = DOCS / "README.md"
    if readme.exists():
        t = readme.read_text(encoding="utf-8")
        if "Python完整卷" not in t and "Python 完整卷" not in t:
            t = t.replace(
                "| Python / AI 服务 | **[路径 C · Python](./路径-Python.md)** |",
                "| Python / AI 服务 | **[路径 C · Python](./路径-Python.md)** · [**Python完整卷**](./Python高频面试题与知识点.md) |",
            )
            readme.write_text(t, encoding="utf-8")
            print("readme")


def main():
    w("Python高频面试题与知识点.md", MAIN)
    w("Python八股频率排序.md", RANK)
    w("Python卡片速记.md", CARDS)
    patch()


if __name__ == "__main__":
    main()
