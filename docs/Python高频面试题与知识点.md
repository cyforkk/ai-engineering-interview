# Python · 知识点

<!-- NAV:START -->
> 📖 **知识点（笔记体）** · 🗣️ [面渣练嘴](./Python面渣级口述.md) · 🃏 [卡片](./Python卡片速记.md)
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md) · [路径](./路径-Python.md)
>
<!-- NAV:END -->


---

## 1. 可变 / 不可变？默认参数陷阱？

- 可变：list、dict、set；不可变：int、str、tuple 等。
- **坑**：`def f(a=[])` 的默认 list 在**定义时创建一次**，多次调用共享。
- **改法**：`def f(a=None):`，函数内 `if a is None: a = []`。

---

## 2. 装饰器 / 生成器 / with？

- **装饰器**：函数增强（日志、鉴权、重试）；`@wraps` 保留元数据。
- **生成器**：`yield` 惰性产出，省内存。
- **with**：上下文管理，保证资源释放。

---

## 3. GIL？线程 / 进程 / asyncio 怎么选？

- CPython：**同一时刻通常一个线程执行 Python 字节码**（简化理解）。
- **CPU 密集**：多进程 / 外部计算。
- **IO 密集**：多线程或 asyncio。
- **高并发等网络（调 LLM）**：asyncio + 异步客户端。
- **禁忌**：async 里 `time.sleep` / 同步 `requests` 会堵事件循环。

---

## 4. 浅拷贝 / 深拷贝？

- 浅：只复制外层；深：递归复制内部对象。

---

## 自测

- [ ] 默认参数陷阱  
- [ ] GIL 选型三句话  
- [ ] async 不能阻塞  

**口述：** [Python面渣级口述.md](./Python面渣级口述.md) · [FastAPI](./Python异步与FastAPI面渣级口述.md) · **卡片：** [Python卡片速记.md](./Python卡片速记.md)
