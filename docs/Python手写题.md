# Python 手写题 · 面试高频

<!-- NAV:START -->
> **导航**
>
> 📍 **Python** · 第 4/9 步 · [完整路径](./路径-Python.md)
> ← [2.FastAPI·述](./Python异步与FastAPI面渣级口述.md)
> → [4.追问](./追问三连-Python.md)
>
> [首页](./README.md) · [AI路径](./路径-AI工程.md) · [Java路径](./路径-Java后端.md) · [Python路径](./路径-Python.md)
>
<!-- NAV:END -->

> 与 [Java面试追问与手写题.md](./Java面试追问与手写题.md) 互补；追问见 [追问三连-Python.md](./追问三连-Python.md)  
> 临场：先说思路 → 写主路径 → 边界 → 复杂度

---

## P0 清单

| 题 | 考点 |
|----|------|
| 装饰器（日志/计时） | 闭包、wraps |
| 带参装饰器 | 三层嵌套 |
| 生成器读大文件 | yield |
| 上下文管理器 | class 或 contextmanager |
| 简易 LRU | OrderedDict / dict+顺序 |
| 限流 Semaphore 异步 | asyncio |
| 反转链表（可选） | 双指针 |
| 单例 | 模块单例 / 装饰器 / metaclass |

---

## 1. 计时装饰器

```python
import functools
import time

def timed(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            print(fn.__name__, time.perf_counter() - t0)
    return wrapper
```

**口述：** wraps 保留原函数元数据；finally 保证异常也打印耗时。

---

## 2. 带参数重试装饰器

```python
import functools
import time

def retry(times=3, delay=0.1):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last = None
            for i in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last = e
                    time.sleep(delay)
            raise last
        return wrapper
    return deco
```

**追问：** 异步版本要用 async wrapper + await；只捕获特定异常。

---

## 3. 生成器按行读文件

```python
def read_lines(path, encoding="utf-8"):
    with open(path, encoding=encoding) as f:
        for line in f:
            yield line.rstrip("\n")
```

**口述：** 大文件不一次性 read；with 保证关闭。

---

## 4. 上下文管理器计时

```python
from contextlib import contextmanager
import time

@contextmanager
def timer(name="block"):
    t0 = time.perf_counter()
    try:
        yield
    finally:
        print(name, time.perf_counter() - t0)

# with timer("embed"): ...
```

---

## 5. 简易 LRU（OrderedDict）

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.od = OrderedDict()

    def get(self, key):
        if key not in self.od:
            return -1
        self.od.move_to_end(key)
        return self.od[key]

    def put(self, key, value):
        if key in self.od:
            self.od.move_to_end(key)
        self.od[key] = value
        if len(self.od) > self.cap:
            self.od.popitem(last=False)
```

**复杂度：** get/put 均摊 O(1)。线程不安全。

---

## 6. asyncio 并发限流

```python
import asyncio

async def map_limited(coro_fn, items, limit=10):
    sem = asyncio.Semaphore(limit)

    async def one(x):
        async with sem:
            return await coro_fn(x)

    return await asyncio.gather(*(one(x) for x in items))
```

**口述：** 调 LLM/爬虫时限制 in-flight，防打爆配额。

---

## 7. 异步超时包装

```python
import asyncio

async def with_timeout(coro, seconds: float):
    return await asyncio.wait_for(coro, timeout=seconds)
```

---

## 8. 模块级单例（推荐说法）

```python
# config_singleton.py
class Settings:
    def __init__(self):
        self.env = "prod"

settings = Settings()  # 模块只导入一次
```

**口述：** Python 模块天然单例；比纠结 metaclass 更常见。

---

## 9. 两数之和（哈希）

```python
def two_sum(nums, target):
    pos = {}
    for i, x in enumerate(nums):
        if target - x in pos:
            return [pos[target - x], i]
        pos[x] = i
    return []
```

---

## 临场模板

```text
1. 复述输入输出
2. 暴力 → 优化
3. 写代码
4. 空输入/异常
5. 时间空间复杂度
```

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 初版 |
