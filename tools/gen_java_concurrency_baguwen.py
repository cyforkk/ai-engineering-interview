# -*- coding: utf-8 -*-
"""Java 多线程与并发高频八股完整卷。不碰面渣。"""
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def w(name, text):
    p = DOCS / name
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print(name, p.stat().st_size)


NAV = """<!-- NAV:START -->
> 📖 **并发八股** · 🗣️ [面渣](./并发面渣级口述.md) · 🃏 [卡片](./并发卡片速记.md)
>
> [模块总览](./Java八股模块总览.md) · [集合/CHM](./Java集合框架高频面试题与知识点.md) · [JVM](./JVM高频面试题与知识点.md)
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md) · [路径](./路径-Java后端.md)
>
<!-- NAV:END -->
"""

CONC = f"""# Java 多线程与并发 · 高频八股知识点（完整卷）

{NAV}

> 并发是面试 **难度最高、区分度最大** 的模块之一，大厂必深挖。  
> 格式：题目 + 核心知识点；强调原理、对比、场景。

### 面试回答建议

1. **概念 → 原理 → 场景** 三段式  
2. 必须能深挖：`synchronized`、`volatile`、**AQS**、**线程池**  
3. 能画：线程状态图、AQS 队列、线程池提交流程  
4. 结合项目：线程池参数怎么定、死锁怎么查、ThreadLocal 注意点  

---

# 一、基础概念

## 1. 进程与线程的区别？

| | 进程 | 线程 |
|--|------|------|
| 单位 | **资源分配** 基本单位 | **CPU 调度** 基本单位 |
| 地址空间 | 独立 | 同进程共享堆、方法区等 |
| 私有 | — | 程序计数器、虚拟机栈、本地方法栈 |
| 开销 | 创建/切换更重 | 相对轻 |

- Java 里多线程共享堆 → 共享可变数据需要同步。

---

## 2. 并发与并行的区别？

| | 并发 concurrency | 并行 parallelism |
|--|------------------|------------------|
| 含义 | 同一**时间段**多任务交替推进 | 同一**时刻**多任务真正同时执行 |
| 硬件 | 单核也可并发（时间片） | 通常需要多核 |

---

## 3. 创建线程的方式？

1. 继承 `Thread`  
2. 实现 `Runnable`  
3. 实现 `Callable` + `FutureTask`（有返回值、可抛异常）  
4. **线程池**（生产推荐）  

- 实现接口优于继承（不占用唯一继承、更灵活）。

---

## 4. 线程生命周期（状态）？

```text
NEW → RUNNABLE → BLOCKED / WAITING / TIMED_WAITING → TERMINATED
```

| 状态 | 含义 |
|------|------|
| NEW | 已创建未 start |
| RUNNABLE | 可运行（含 OS 的就绪 + 正在运行） |
| BLOCKED | 等 `synchronized` 监视器锁 |
| WAITING | 无限等待（`wait`/`join`/`park` 等） |
| TIMED_WAITING | 限时等待（`sleep`/`wait(timeout)` 等） |
| TERMINATED | 终止 |

---

## 5. start() 与 run() 的区别？

| | start() | run() |
|--|---------|-------|
| 作用 | **启动新线程**，线程再执行 run | 普通方法调用 |
| 线程 | 异步新线程 | 仍在**当前线程**执行 |
| 多次调用 | start 只能一次 | 可当普通方法多次调 |

---

# 二、synchronized 与 Lock

## 6. synchronized 怎么用？锁的是谁？

| 用法 | 锁对象 |
|------|--------|
| 实例方法 | 当前实例 `this` |
| 静态方法 | 当前类的 `Class` 对象 |
| 代码块 | 括号里指定的对象 |

- **可重入**：同一线程可多次获得同一把锁（避免自己堵自己）。  
- 保证：临界区 **互斥（原子性视角）** + 解锁后的 **可见性**（与 happens-before 相关）。

---

## 7. 锁升级过程？（JDK6+ 优化，高频）

```text
无锁 → 偏向锁 → 轻量级锁（自旋/CAS） → 重量级锁（OS 互斥量）
```

- **偏向**：无竞争时，偏向第一个获取锁的线程，减少 CAS。  
- **轻量级**：有竞争但可自旋等待，避免陷入内核。  
- **重量级**：竞争激烈，阻塞挂起，Monitor。  
- 底层：对象头 **Mark Word** 记录锁状态；重量级关联 **Monitor**。  
- （具体默认开关随 JDK 版本有调整，面试说清演进动机即可。）

---

## 8. ReentrantLock vs synchronized？

| 对比 | synchronized | ReentrantLock |
|------|--------------|---------------|
| 实现 | JVM | API（**AQS**） |
| 可中断 | 获取锁过程基本不可中断 | `lockInterruptibly` 可中断 |
| 公平 | 非公平 | 可公平 / 非公平 |
| 条件变量 | 单个 wait/notify 集合 | 多个 **Condition** |
| 释放 | 自动 | **必须 unlock**（`try/finally`） |
| 超时尝试 | 不直接支持 | `tryLock(timeout)` |
| 性能 | JDK6 后接近 | 功能更强 |

- 需要：可中断、公平、多条件、tryLock → **ReentrantLock**  
- 简单同步块 → **synchronized** 足够且不易漏释放  

---

# 三、volatile 与 JMM

## 9. volatile 三大特性？

1. **可见性**：写尽快对其他线程可见（主内存可见性语义）。  
2. **有序性**：禁止部分指令重排序（内存屏障）。  
3. **不保证原子性**：`i++` 仍是读改写三步，会丢更新。  

- 典型场景：**状态标志**、DCL 单例中的实例引用（见下）。

---

## 10. volatile 能保证原子性吗？为什么？

- **不能**。  
- 只保证单次读/写的可见与有序；复合操作需要锁或原子类。

---

## 11. DCL 单例为什么要 volatile？

```text
if (instance == null) {{
  synchronized {{
    if (instance == null)
      instance = new Singleton(); // 可能指令重排
  }}
}}
```
- `new` 可能：**分配内存 → 构造 → 赋值引用** 被重排为 **分配 → 赋值 → 构造**。  
- 其他线程看到非 null 引用但对象未初始化完 → 出错。  
- **`volatile` 禁止重排**，保证发布安全。

---

## 12. Happens-Before（掌握主干）？

若 A happens-before B，则 A 的写对 B 可见且有序。

| 规则 | 大意 |
|------|------|
| 程序顺序 | 单线程内前面 hb 后面 |
| 锁规则 | unlock hb 后续同锁 lock |
| volatile | 写 hb 后续对该变量的读 |
| 线程 start | start 前写 hb 线程内 |
| 线程 join | 线程内写 hb join 后 |
| 传递性 | A hb B 且 B hb C ⇒ A hb C |

- `synchronized`/`volatile`/线程启动结束等工具，本质在建立 hb。

---

# 四、CAS 与原子类

## 13. CAS 是什么？优缺点？

- **Compare-And-Swap**：内存值 V、期望 A、新值 B；仅当 V==A 才写成 B。  
- 乐观锁思想；依赖 CPU 原语。  
- **优点**：无锁竞争时性能好。  
- **缺点**  
  - **ABA**：A→B→A 误判未变 → `AtomicStampedReference` / `AtomicMarkableReference`  
  - 自旋失败重试，竞争极高时空转  
  - 通常只保证**一个变量**原子  

---

## 14. 常用原子类？LongAdder？

- `AtomicInteger` / `AtomicLong` / `AtomicReference` / `AtomicBoolean` 等。  
- **LongAdder**：分段累加（类似 CHM 计数思想），**高并发计数**通常优于频繁 CAS 的 AtomicLong。

---

# 五、AQS（并发基石）

## 15. AQS 核心思想？（必须掌握）

- 全称：`AbstractQueuedSynchronizer`，构建锁与同步器的**框架**。  
- 核心：  
  1. `volatile int state` 表示同步状态  
  2. **CLH 变体队列**（双向）管理获取失败而等待的线程  
- 模式：  
  - **独占**：ReentrantLock  
  - **共享**：Semaphore、CountDownLatch  
- 自定义：重写 `tryAcquire` / `tryRelease`（或共享版），复用队列与阻塞唤醒。  

### 基于 AQS 的工具

ReentrantLock、Semaphore、CountDownLatch、ReentrantReadWriteLock、部分 Queue 等。

---

# 六、线程池（超级高频）

## 16. ThreadPoolExecutor 七大参数？（必背+会解释）

| # | 参数 | 含义 |
|---|------|------|
| 1 | corePoolSize | 核心线程数 |
| 2 | maximumPoolSize | 最大线程数 |
| 3 | keepAliveTime | 非核心空闲存活时间 |
| 4 | unit | 时间单位 |
| 5 | workQueue | 任务队列 |
| 6 | threadFactory | 线程工厂（命名、守护等） |
| 7 | handler | 拒绝策略 |

常用队列：`LinkedBlockingQueue`、`ArrayBlockingQueue`、`SynchronousQueue`。

---

## 17. 任务提交流程？

```text
1. 当前线程数 < core → 创建核心线程执行
2. ≥ core → 任务入队
3. 队列满 且 < max → 创建非核心线程
4. 队列满 且 ≥ max → 执行拒绝策略
```

（细节以源码 `execute` 为准，面试按此四步说即可。）

---

## 18. 四种拒绝策略？

| 策略 | 行为 |
|------|------|
| AbortPolicy | **默认**，抛 `RejectedExecutionException` |
| CallerRunsPolicy | 调用者线程自己跑任务（反向压测/降速） |
| DiscardPolicy | 默默丢弃 |
| DiscardOldestPolicy | 丢队列最老的，再尝试提交 |

---

## 19. 为什么不要用 Executors 创建？

| 方法 | 风险 |
|------|------|
| newFixedThreadPool / newSingleThreadExecutor | 默认 **无界** LinkedBlockingQueue → 堆积 **OOM** |
| newCachedThreadPool | 最大线程很大，可能创建过多线程 |
| newScheduledThreadPool | 同样需注意任务堆积 |

- **生产推荐**：手动 `new ThreadPoolExecutor(...)`，有界队列 + 明确拒绝策略 + 自定义线程名。

---

## 20. 参数如何估？（CPU vs IO）

| 类型 | 经验方向 |
|------|----------|
| CPU 密集 | 线程数 ≈ **CPU 核数 + 1**（或核数） |
| IO 密集 | 可更大：核数 × (1 + 等待/计算) 一类公式作起点，**压测调** |
| 混合 | 拆池或取折中，监控队列与拒绝 |

- 关键：队列长度、拒绝率、任务耗时、超时；没有唯一公式。

---

# 七、常用同步工具

## 21. CountDownLatch / CyclicBarrier / Semaphore 等？

| 工具 | 核心作用 | 典型场景 |
|------|----------|----------|
| CountDownLatch | 一或多个线程等**一组事件**结束（倒数） | 主线程等 N 个子任务 |
| CyclicBarrier | **一组线程互相等**，到齐再走（可重置） | 多线程分阶段计算 |
| Semaphore | 控制同时访问数（许可证） | 限流、连接池 |
| Phaser | 更灵活的多阶段同步 | 动态注册参与者 |
| Exchanger | 两线程交换数据 | 双线程握手交换 |

### CountDownLatch vs CyclicBarrier（常对比）

| | CountDownLatch | CyclicBarrier |
|--|----------------|---------------|
| 关系 | 一个等多个 | 多个互等 |
| 可重用 | 否（计数到 0） | 是（reset/循环） |

---

# 八、ThreadLocal

## 22. ThreadLocal 原理？内存泄漏？

- 每个 `Thread` 有 `ThreadLocalMap`。  
- key：`ThreadLocal` 实例（**弱引用**）；value：存放的值（**强引用**）。  
- **泄漏场景**：线程池线程长期复用；key 被回收后 value 仍挂在 map 上，难释放。  
- **正确用法**：用完 **`remove()`**（`try/finally`）。  
- 场景：用户上下文、简单日期格式隔离（注意别滥用）。

---

# 九、死锁

## 23. 死锁四条件？如何避免与排查？

**四必要条件（同时满足才可能死锁）：**

1. 互斥  
2. 请求与保持  
3. 不剥夺  
4. 循环等待  

**避免/破坏：**

- 固定全局加锁顺序（破循环等待）  
- `tryLock` 超时（破请求保持/不剥夺）  
- 缩小锁范围、避免嵌套锁  
- 一次性申请所需资源  

**排查：** `jstack` 可检测并打印 Java 死锁；结合日志与监控。

---

# 十、虚拟线程（Java 21 / 2026 加分）

## 24. 虚拟线程 vs 平台线程？

| | 平台线程 | 虚拟线程 Virtual Thread |
|--|----------|-------------------------|
| 调度 | OS | **JVM** 调度的轻量线程 |
| 数量 | 受 OS/内存限制，宜少 | 可达很大规模（百万级可能） |
| 场景 | 通用 | **高并发阻塞 IO** 简化模型 |
| 注意 | — | 不适合长时间 **CPU 密集**；`synchronized` 可能 **钉住** 载体线程，热点锁可用 `ReentrantLock` 等 |

- 来自 Project Loom；Java 21 正式。  
- 可大幅减少「为阻塞 IO 堆线程池」的心智负担，但仍要限流与超时。

---

# 十一、JUC 集合与并发结构（衔接）

- **ConcurrentHashMap**：JDK8 CAS + synchronized 锁头（详见 [集合卷](./Java集合框架高频面试题与知识点.md)）。  
- **CopyOnWriteArrayList**：读多写少。  
- **BlockingQueue**：线程池工作队列、生产者消费者。  

---

# 自测清单

- [ ] 进程线程、并发并行、start/run、六种状态  
- [ ] synchronized 锁对象 + 锁升级 + 可重入  
- [ ] ReentrantLock 对比表  
- [ ] volatile 三性 + DCL + hb 主干  
- [ ] CAS / ABA / LongAdder  
- [ ] AQS：state + 队列 + 独占/共享  
- [ ] 线程池 7 参数 + 流程 + 4 拒绝 + Executors 坑  
- [ ] Latch/Barrier/Semaphore  
- [ ] ThreadLocal 泄漏与 remove  
- [ ] 死锁四条件 + jstack  
- [ ] 虚拟线程适用场景  

**口述：** [并发面渣级口述.md](./并发面渣级口述.md)  
**卡片：** [并发卡片速记.md](./并发卡片速记.md)  

---

## 可继续深挖（点名即可）

1. AQS 源码核心流程（acquire/release）  
2. 线程池参数业务压测配置案例  
3. synchronized 锁升级与对象头细节  
4. JMM + Happens-Before 完整规则表  
5. 虚拟线程原理、钉住载体线程与最佳实践  

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 并发完整卷：10 大模块按大厂高频大纲补全 |
"""

CARDS = f"""# 并发 · 卡片速记

<!-- NAV:START -->
> [完整知识点](./并发高频面试题与知识点.md) · [面渣](./并发面渣级口述.md) · [总览](./Java八股模块总览.md)
<!-- NAV:END -->

> 遮住 **A**。

---

## 基础

**Q1 进程 vs 线程？**  
A: 资源分配 vs CPU调度；线程共享堆。

**Q2 并发 vs 并行？**  
A: 时间段交替 vs 同一时刻同时。

**Q3 创建线程 4 种？**  
A: Thread / Runnable / Callable / 线程池。

**Q4 线程状态？**  
A: NEW→RUNNABLE→BLOCKED/WAITING/TIMED_WAITING→TERMINATED。

**Q5 start vs run？**  
A: start 启新线程；run 普通调用。

## synchronized / Lock

**Q6 synchronized 锁谁？**  
A: 实例this / 静态Class / 代码块指定对象。

**Q7 锁升级？**  
A: 偏向→轻量→重量。

**Q8 ReentrantLock 优势？**  
A: 可中断、公平、多Condition、tryLock；需手动unlock。

## volatile / JMM

**Q9 volatile 三性？**  
A: 可见、有序；不保证原子。

**Q10 DCL 为何 volatile？**  
A: 防 new 重排导致未初始化发布。

**Q11 happens-before 举例？**  
A: 解锁hb加锁；volatile写hb读；传递性。

## CAS / AQS

**Q12 CAS？**  
A: 期望值匹配才更新；ABA用版本戳。

**Q13 LongAdder？**  
A: 分段计数，高并发计数更优。

**Q14 AQS 核心？**  
A: state + CLH变体队列；独占/共享。

## 线程池

**Q15 七大参数？**  
A: core/max/keepAlive/unit/queue/factory/handler。

**Q16 提交流程？**  
A: core→入队→max→拒绝。

**Q17 拒绝策略 4？**  
A: Abort/CallerRuns/Discard/DiscardOldest。

**Q18 Executors 坑？**  
A: 无界队列OOM/无线程上限；手写TPE。

**Q19 CPU vs IO 线程数？**  
A: CPU≈核数；IO可更大，压测调。

## 工具 / TL / 死锁 / VT

**Q20 CountDownLatch vs CyclicBarrier？**  
A: 一个等多个 / 多个互等可重用。

**Q21 Semaphore？**  
A: 许可证限流。

**Q22 ThreadLocal 泄漏？**  
A: 弱引用key+强value；池化必remove。

**Q23 死锁四条件？**  
A: 互斥、请求保持、不剥夺、环路。

**Q24 虚拟线程？**  
A: JVM轻量线程，适高并发阻塞IO；不适重CPU。

---

详解：[并发高频面试题与知识点.md](./并发高频面试题与知识点.md)
"""


def patch():
    ov = DOCS / "Java八股模块总览.md"
    if ov.exists():
        t = ov.read_text(encoding="utf-8")
        if "并发完整卷" not in t and "并发八股完整" not in t:
            t = t.replace(
                "| 2 并发 | [并发](./并发高频面试题与知识点.md) |",
                "| 2 **并发完整卷** | [并发](./并发高频面试题与知识点.md) |",
            )
            note = "\n\n> **并发**已按 10 大模块补全：基础、synchronized/Lock、volatile/JMM、CAS、AQS、线程池、工具类、ThreadLocal、死锁、虚拟线程。→ [并发高频面试题与知识点.md](./并发高频面试题与知识点.md)\n"
            if "并发已按 10 大模块" not in t:
                t = t.replace(
                    "原则：**原理 + 对比 + 场景**，不要死背一句话。",
                    "原则：**原理 + 对比 + 场景**，不要死背一句话。" + note,
                    1,
                )
            ov.write_text(t, encoding="utf-8")
            print("overview patched")


def main():
    w("并发高频面试题与知识点.md", CONC)
    w("并发卡片速记.md", CARDS)
    patch()


if __name__ == "__main__":
    main()
