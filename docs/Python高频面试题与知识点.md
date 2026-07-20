# Python · 高频面试

> **专题序：语言轨 / 权重 P0（Python 岗）· P1（AI 应用岗）**  
> **面渣级长口述：** [Python面渣级口述.md](./Python面渣级口述.md)  
> **异步/FastAPI 实战长口述：** [Python异步与FastAPI面渣级口述.md](./Python异步与FastAPI面渣级口述.md)  
> **追问三连：** [追问三连-Python.md](./追问三连-Python.md)  
> 主线：基础语法与类型 → 迭代/生成器 → **GIL 与并发** → 装饰器/上下文 → Web·工程  
> 总索引：[README.md](./README.md)

---

## 一、优先级总览

| 级 | 模块 | 频率 |
|----|------|------|
| **P0** | 可变/不可变、浅深拷贝、`*args/**kwargs`、推导式 | 极高 |
| **P0** | 迭代器/生成器、装饰器、上下文管理器 | 极高 |
| **P0** | GIL、多线程/多进程/asyncio 选型 | 极高 |
| **P1** | 面向对象、MRO、描述符、`__slots__` | 高 |
| **P1** | 包管理、虚拟环境、类型注解、异常 | 高 |
| **P1** | FastAPI/Flask、WSGI/ASGI 概念 | AI/Web 岗 |
| **P2** | 元类、GC 细节、C 扩展、性能分析 | 中 |

---

## 二、P0 必会

### 2.1 类型与拷贝

| 点 | 结论 |
|----|------|
| 可变 | list/dict/set |
| 不可变 | int/str/tuple/frozenset |
| 浅拷贝 | 外层新、内层共享（`copy` / 切片） |
| 深拷贝 | `copy.deepcopy` 递归复制 |
| 默认参数 | **别用可变对象当默认参数** |

### 2.2 函数

| 点 | 结论 |
|----|------|
| `*args/**kwargs` | 可变位置/关键字 |
| 闭包 | 内函数引用外函数变量 |
| LEGB | 局部→嵌套→全局→内建 |
| `global/nonlocal` | 改全局 / 改外层非全局 |

### 2.3 迭代器与生成器

| 点 | 结论 |
|----|------|
| 可迭代 | `__iter__` |
| 迭代器 | `__iter__` + `__next__` |
| 生成器 | `yield`，惰性、省内存 |
| 生成器表达式 | `(x for x in …)` |

### 2.4 装饰器

```text
@decorator
def f(): ...
# 等价 f = decorator(f)
```

- 带参数装饰器：三层嵌套  
- `functools.wraps` 保留元信息  
- 常见：日志、计时、权限、缓存 `@lru_cache`

### 2.5 上下文管理器

- `with`：`__enter__` / `__exit__`  
- `@contextmanager` + yield  
- 场景：文件、锁、数据库连接  

### 2.6 GIL 与并发（核心）

| 点 | 结论 |
|----|------|
| GIL | CPython 同一时刻一线程执行字节码 |
| CPU 密集 | **多进程** 或 C 扩展/换实现 |
| IO 密集 | 多线程仍有用；或 **asyncio** |
| asyncio | 单线程协程，适合高并发 IO |
| 选型 | CPU→process；IO 阻塞→thread；海量连接→async |

---

## 三、P1 常考

### 3.1 OOP

| 点 | 结论 |
|----|------|
| 新式类 | 默认 object 子类 |
| MRO | C3，`Class.__mro__` |
| 多继承 | 菱形靠 MRO |
| `@property` | 属性化访问 |
| 魔术方法 | `__init__/__str__/__repr__/__eq__` 等 |

### 3.2 异常与资源

- `try/except/else/finally`  
- 自定义异常继承 `Exception`  
- `raise ... from`  
- 优先 `with` 管资源  

### 3.3 工程实践

| 点 | 结论 |
|----|------|
| venv/uv/poetry | 依赖隔离 |
| `requirements.txt` / lock | 可复现 |
| 类型注解 | `list[int]`、`Optional`、Protocol |
| 测试 | pytest |
| 日志 | logging，别滥 print 生产 |

### 3.4 Web（AI 服务常见）

| 点 | 结论 |
|----|------|
| Flask | 轻量 WSGI |
| FastAPI | ASGI、类型、自动 OpenAPI，AI 服务常用 |
| WSGI vs ASGI | 同步网关 vs 异步 |
| uvicorn/gunicorn | 部署 |

### 3.5 与 AI 应用交界

- 调用 LLM API：超时、重试、限流、幂等  
- 流式输出：SSE/WebSocket  
- 依赖：`httpx`/`openai` SDK、向量库客户端  
- 详见 [AI应用工程](./AI应用工程高频面试题与知识点.md)、[Agent](./Agent高频面试题与知识点.md)

---

## 四、P2 加分

| 点 | 一句话 |
|----|--------|
| 描述符 | `__get__/__set__`，property 底层 |
| 元类 | 创建类的类，框架向 |
| GC | 引用计数+分代，循环用 GC |
| `__slots__` | 减 `__dict__` 省内存 |
| 性能 | cProfile、生成器、pypy/C 扩展 |

---

## 五、高频题 TOP 25

1. 可变 vs 不可变  
2. 浅拷贝深拷贝  
3. 默认参数陷阱  
4. `*args/**kwargs`  
5. 装饰器原理  
6. 生成器与 yield  
7. 迭代器协议  
8. with 原理  
9. GIL 是什么  
10. 多线程 vs 多进程 vs asyncio  
11. 闭包  
12. 列表/字典推导式  
13. 新式类与 MRO  
14. `@staticmethod` vs `classmethod`  
15. 异常处理最佳实践  
16. 虚拟环境为何需要  
17. 类型注解有什么用  
18. FastAPI 为何适合 AI 服务  
19. 如何做接口超时重试  
20. 全局解释器锁下如何充分利用多核  
21. `is` vs `==`  
22. 字符串拼接性能  
23. 内存泄漏可能原因（循环引用、全局缓存）  
24. 协程与线程区别  
25. 项目里 Python 怎么分层  

---

## 六、自测清单

### P0

- [ ] 默认参数不用 list  
- [ ] 装饰器能手写无参版本  
- [ ] yield 省内存场景  
- [ ] GIL + 三种并发选型  
- [ ] with 干什么  

### P1

- [ ] MRO 一句话  
- [ ] FastAPI/Flask 区别  
- [ ] pytest 基本用法  

---

## 七、关联

[AI应用工程](./AI应用工程高频面试题与知识点.md) · [Agent](./Agent高频面试题与知识点.md) · [算法](./算法高频面试题与知识点.md) · [README](./README.md)

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-20 | 初版：Python 高频地图 |
