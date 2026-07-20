# Python 异步 · FastAPI · 面渣级长口述（实战向）

<!-- NAV:START -->
> **导航串联**
>
> **系列：Python 主线**（3/10）
> - 上一篇：[Python·面渣](./Python面渣级口述.md)
> - 下一篇：[Python手写题](./Python手写题.md)
>
> **相关专题：** [Python 基础](./Python高频面试题与知识点.md) · [AI 应用](./AI应用工程高频面试题与知识点.md) · [LLMOps](./LLMOps与可观测高频面试题与知识点.md)
>
> **返回：** [总索引](./README.md) · [串联地图](./学习地图-串联.md) · [路线图](./学习路线图-4到8周.md) · [架构图](./架构图集.md)
>
<!-- NAV:END -->

> 配套：[Python高频面试题与知识点.md](./Python高频面试题与知识点.md) · [Python面渣级口述.md](./Python面渣级口述.md)  
> 定位：**AI 服务 / 高并发 IO** 面试深挖；每段 3～5 分钟可拆讲  
> 总索引：[README.md](./README.md)

---

## 一、asyncio 底层叙事（先建立模型）

### 1. 事件循环是什么？协程怎么跑？

**口述：**

> asyncio 是单线程（默认一个事件循环）里做并发：协程遇到 await 可暂停，把控制权交回事件循环，循环去跑别的就绪协程或处理 IO 完成回调。  
> 所以它适合**大量等待**的场景，比如同时挂起几百个 HTTP 调模型、查向量库；不适合在协程里狂算 CPU，那会堵死整个循环，所有请求一起卡。  
> `async def` 定义协程函数，调用它只得到协程对象，要用 `await` 或 `asyncio.run` / `create_task` 才真正调度。  
> `await` 的对象要是 awaitable：协程、Task、Future 等。  
> 和线程比：无线程切换到内核那么重，但一旦有人写了同步阻塞调用，比如 `time.sleep`、同步 `requests.get`，事件循环就停摆——这是面试和线上最常见的坑。

---

### 2. create_task、gather、wait、Semaphore

**口述：**

> `asyncio.create_task` 把协程包装成 Task 丢进循环，可以「先发射再 await」，实现并发。  
> `asyncio.gather(*tasks)` 等一批任务都结束，默认一个失败会取消其它（可 `return_exceptions=True` 收集异常）。  
> 需要限流时用 `asyncio.Semaphore`：例如最多 20 个并发打模型 API，acquire 后再 await 调用，结束 release，避免把配额和连接打爆。  
> 超时用 `asyncio.wait_for(coro, timeout=…)`，超时抛 `TimeoutError`，要在外层决定重试还是降级。  
> 取消：Task.cancel 会在下次 await 点注入 `CancelledError`，要会清理资源（finally）。

---

### 3. 阻塞代码怎么办？

**口述：**

> 三种路：  
> 1. 换成原生 async 库：`httpx.AsyncClient`、`asyncpg`、motor 等；  
> 2. `asyncio.to_thread(fn, …)` 或 loop.run_in_executor，把同步函数丢线程池，别堵事件循环；  
> 3. CPU 重活丢进程池，别占满线程。  
> AI 项目里：embedding 本地模型若同步推理，必须进线程/进程，或独立推理服务用 HTTP 异步调用。

---

### 4. async 与线程安全、共享状态

**口述：**

> 单线程协程里，普通 `await` 切换点之间不会被其它协程打断「字节码中间态」到线程那种程度，但 await 边界仍可能交错，共享 list/dict 仍要设计清楚。  
> 和线程混用时，**不要**假设 dict 随便跨线程改；跨线程通信用队列。  
> 数据库连接、httpx Client 建议按应用生命周期复用，注意线程/任务间是否安全；httpx AsyncClient 应在同事件循环内使用。

---

## 二、FastAPI 实战长口述

### 5. FastAPI 为什么适合 AI 网关 / RAG 服务

**口述：**

> 三点：类型注解驱动校验与 OpenAPI，前后端和测试都省事；原生 async，方便并发调模型和向量库；依赖注入清晰，鉴权、DB session、配置好挂。  
> 部署常用 uvicorn（ASGI），多 worker 时注意：每个进程独立内存，本地缓存不共享，模型若 load 进进程要算内存×worker。  
> 它不自动解决 LLM 慢和贵：还要自己做超时、队列、限流、缓存和降级。

---

### 6. 一次请求生命周期（可画图讲）

**口述：**

> 请求进 ASGI → 中间件（日志 request_id、CORS、计时）→ 路由匹配 → 依赖注入（鉴权解析用户、取配置）→ path/query/body 校验（Pydantic）→ 进入 endpoint 协程 → 调 service 层 → await 外部 IO → 返回 Pydantic 模型或流式响应。  
> 异常：HTTPException 给业务错误；未捕获进 exception handler，统一 JSON 错误体，避免堆栈泄露给客户端。

---

### 7. 依赖注入与鉴权

**口述：**

> `Depends` 把横切逻辑从业务函数拆出去：`get_current_user` 读 Header Token，校验失败直接 401。  
> 可嵌套依赖，可缓存（`use_cache`）避免同请求重复解析。  
> AI 场景常依赖：当前租户、配额检查、向量库 client、LLM client。  
> 密钥从环境变量或密钥服务注入，Settings 用 pydantic-settings，不要写死代码里。

---

### 8. 流式输出 SSE（AI 高频）

**口述：**

> 大模型生成慢，用 StreamingResponse 或 sse-starlette 做 Server-Sent Events，边生成边推，降低首字延迟体感。  
> 实现上 endpoint 返回 async generator，里面 async for chunk in llm_stream。  
> 客户端断开时要取消上游模型请求，避免空跑费钱——在 generator 里注意 CancelledError 和 aclose。  
> 网关/Nginx 要关缓冲，否则流式被攒成一块。  
> 和 WebSocket 比：SSE 单向服务端推，实现简单，适合 token 流；双向对话式 agent 有时用 WS。

---

### 9. 后台任务 vs 消息队列

**口述：**

> FastAPI `BackgroundTasks` 适合请求返回后顺手做轻量事，如记日志、轻量通知；进程挂了任务就没了，不适合扣费、发邮件核心链路。  
> 真正可靠异步：Celery / RQ / Arq / 云队列，或 Kafka/Rabbit；API 只投递任务 ID，客户端轮询或 webhook。  
> LLM 长任务（长文档解析、批量 embedding）应进队列，API 快速返回 job_id，避免占用 worker 数十分钟。

---

### 10. 部署与多 Worker 坑

**口述：**

> uvicorn 多 worker 是多进程，全局变量、内存向量、本地缓存不共享。  
> 模型加载若在 import 时做，每个 worker 各加载一份，内存翻倍。  
> 文件上传落本地磁盘也不共享，应用对象存储。  
> 健康检查要区分 liveness/readiness：模型未加载完不要接流量。  
> 生产前面常加 Nginx/网关做 TLS、限流、路由。

---

## 三、AI 服务端到端口述（综合题）

### 11. 设计一个「RAG 查询 API」（5 分钟版）

**口述：**

> 接口 `POST /v1/chat`，body 含 query、conversation_id。  
> 依赖注入校验 API Key 与租户权限。  
> Service 内：  
> 1）可选查语义缓存；  
> 2）await 向量检索（httpx/async 驱动），metadata 过滤租户；  
> 3）拼 prompt，await 流式或非流式调 LLM，整体 wait_for 超时；  
> 4）写审计日志与 token 用量；  
> 5）失败分类：检索空→拒答；模型 429→退避重试有限次；超时→503 或降级只返回文档片段。  
> 并发用 Semaphore 限制对模型的最大 in-flight。  
> 指标：QPS、TTFT、总延迟、错误码、费用。  
> 这就是 asyncio + FastAPI 在 AI 工程里的典型答法。

---

### 12. 线上事件循环被堵怎么查

**口述：**

> 表现：所有接口一起慢，CPU 不一定高。  
> 查：是否有同步 requests/redis/py 客户端；是否有大 JSON 同步解析；是否在 async 路由里跑了重 CPU。  
> 用日志打阶段耗时；blocking 检测工具或压测对比。  
> 修：换 async 库、to_thread、拆服务。

---

## 四、追问快答

| 追问 | 答 |
|------|-----|
| async def 里能 sleep 吗？ | 用 `asyncio.sleep`，别 `time.sleep` |
| 和多线程同时用？ | 可以，但共享状态要小心；IO 线程池有界 |
| Pydantic v2？ | 校验更快，模型写法略变，知迁移点即可 |
| WebSocket 何时用？ | 双向、长连接 agent；纯生成流 SSE 往往够 |

---

## 五、考前骨架

```text
事件循环：await 让出；禁阻塞
并发：create_task + Semaphore + wait_for
FastAPI：Depends 鉴权、Pydantic 校验、SSE 流式
AI：超时重试限流 + job 队列长任务
多 worker：内存不共享
```

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-20 | 初版：异步 + FastAPI 实战长口述 |
