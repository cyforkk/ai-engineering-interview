# Python · 大白话详解

<!-- NAV:START -->
> 📖 **本文用大白话讲懂** · 🗣️ [练嘴·面渣](./Python面渣级口述.md) · 🃏 [卡片速记](./Python卡片速记.md)
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md) · [路径](./路径-Python.md)
>
<!-- NAV:END -->

> 读不懂术语？先看 **生活例子**。会说了再去面渣练开口。


---

## 1. 默认参数大坑（必考）

### 错法

```python
def add(item, bag=[]):  # 糟糕
    bag.append(item)
    return bag
```

多次调用会共用**同一个 list**，数据串了。

### 为啥？

默认参数在**函数定义时**就创建好了，不是每次调用新建。

### 对法

```python
def add(item, bag=None):
    if bag is None:
        bag = []
    bag.append(item)
    return bag
```

---

## 2. 装饰器 / 生成器 / with（用途向）

| 特性 | 人话 | 干啥用 |
|------|------|--------|
| 装饰器 | 给函数外面套马甲 | 日志、登录检查、重试 |
| 生成器 | 一次吐一点，不一次全造好 | 读大文件省内存 |
| with | 用完自动收拾 | 关文件、放锁 |

---

## 3. GIL：为啥多线程算得不快？

### 先记一句

CPython 里，**同一时刻通常只有一个线程在跑 Python 字节码**（简化理解）。

### 怎么选？

| 你在干啥 | 更合适 |
|----------|--------|
| 狂算 CPU | **多进程**或丢到别的服务 |
| 等网络/磁盘 | 多线程或 **asyncio** 都行 |
| 大量等 LLM 接口 | **asyncio** 很合适 |

### asyncio 大忌

在 async 函数里写 `time.sleep` 或同步 `requests`：  
像单行道上有人停车睡觉——**后面全堵死**。  
要用异步库、`await asyncio.sleep`。

FastAPI 适合做 AI 接口服务，但仍要自己做超时、限流。  
长文： [Python异步与FastAPI面渣级口述.md](./Python异步与FastAPI面渣级口述.md)

**练嘴：** [Python面渣级口述.md](./Python面渣级口述.md) · **卡片：** [Python卡片速记.md](./Python卡片速记.md)
