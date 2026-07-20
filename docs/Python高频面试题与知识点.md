# Python · 知识点（精讲版）

<!-- NAV:START -->
> **导航** → [Python·面渣](./Python面渣级口述.md) · [异步FastAPI长口述](./Python异步与FastAPI面渣级口述.md)
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md) · [Python路径](./路径-Python.md)
>
<!-- NAV:END -->

---

## 一、要搞定什么

1. 可变/不可变、默认参数陷阱（很爱考）  
2. 装饰器、生成器、with **能讲清用途**  
3. **GIL** 下多线程/多进程/asyncio 怎么选（AI 服务核心）  

**主教材：** [Python面渣级口述.md](./Python面渣级口述.md)  
**服务深挖：** [Python异步与FastAPI面渣级口述.md](./Python异步与FastAPI面渣级口述.md)

---

## 二、可变与默认参数（P0）

### 白话

list/dict 可变；str/int/tuple 不可变。  
`def f(a=[])` 的 `[]` 在**定义时创建一次**，多次调用共享同一个 list，会「脏数据」——改用 `None`，函数里再 `a = []`。

浅拷贝只复制外层，内层对象仍共享；深拷贝递归复制。

### 面试怎么答

> 可变不可变举例；默认参数陷阱与改法；浅深拷贝区别。

---

## 三、装饰器 / 生成器 / with（P0）

### 白话

**装饰器：** 函数包函数，`@` 语法糖。用于日志、鉴权、重试、计时。用 `functools.wraps` 保留原函数名。  

**生成器：** `yield` 惰性产出，适合大文件逐行读，省内存。  

**with：** 保证进入退出成对（关文件、放锁），异常也会走清理。

### 面试怎么答

> 装饰器=高阶函数；生成器省内存场景；with 协议 enter/exit。

**手写：** [Python手写题.md](./Python手写题.md)

---

## 四、GIL 与并发（P0 最重要）

### 白话

CPython 有 **GIL**：同一进程里同一时刻通常只有一个线程在执行 Python 字节码。  
所以**纯算 CPU** 多线程跑不满多核 → 用**多进程**，或把计算放到 C 扩展/别的服务。  

**IO 等待**时（网络、磁盘）会释放 GIL，多线程仍有用。  
**asyncio：** 单线程协程，适合高并发等网络（调 LLM、向量库），但协程里不能写阻塞代码（`time.sleep`、同步 requests），否则堵死事件循环。

### 面试怎么答

> GIL 含义；CPU→进程；IO→线程或 asyncio；asyncio 禁阻塞。  
> FastAPI 适合 AI 网关：类型+async+OpenAPI，但仍要自己做超时限流。

**完整稿：** [Python面渣 · GIL](./Python面渣级口述.md) · [FastAPI 实战](./Python异步与FastAPI面渣级口述.md)

---

## 五、自测

- [ ] 默认参数陷阱能举反例  
- [ ] 装饰器用途 + wraps  
- [ ] GIL 选型三句话  
- [ ] 能说为何 async 里不能 requests  

**使用说明：** [如何使用本仓库.md](./如何使用本仓库.md)
