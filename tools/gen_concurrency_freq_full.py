# -*- coding: utf-8 -*-
"""并发编程：按超高频/高频/中频/低频完整卷 + 专项频率导航。不碰面渣。"""
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def w(name, text):
    p = DOCS / name
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print(name, p.stat().st_size)


NAV = """<!-- NAV:START -->
> 📖 **并发完整卷** · 🗣️ [面渣](./并发面渣级口述.md) · 🃏 [卡片](./并发卡片速记.md) · 🔥 [频率导航](./并发八股频率排序.md)
>
> [四档主线](./Java后端面试频率-四档.md) · [集合CHM](./Java集合框架高频面试题与知识点.md)
>
<!-- NAV:END -->
"""

CONC = f"""# 并发编程 · 高频八股知识点（完整卷）

{NAV}

> 2025–2026 大厂深挖最狠模块之一。**线程池 / 锁 / AQS / CAS 几乎必考。**  
> 建议：源码关键路径 + **画图** + 项目场景。

### 并发专项时间占比

| 优先级 | 模块 | 时间 |
|--------|------|:----:|
| **P0** | 线程池 + synchronized + volatile + CAS + AQS | **50%** |
| **P1** | ThreadLocal + 死锁 + Latch/Barrier/Semaphore | **20%** |
| **P2** | JMM + Happens-Before + 乐观/悲观锁 | **15%** |
| **P3** | BlockingQueue + CompletableFuture + 虚拟线程 | **15%** |

### 高效准备

1. 线程池能讲清 **流程 + 参数设计 + 项目为何这样配**  
2. 锁升级 **能画图**  
3. AQS：模板方法 + CLH 队列 + CAS 改 state（不必抠每一行）  
4. 追问链：参数 → 拒绝策略 → 为何不用 Executors → 监控 → 动态调整  

---

# 一、超高频（几乎必问）

## 1. 线程基础

### 1.1 进程与线程的区别？

| | 进程 | 线程 |
|--|------|------|
| 单位 | 资源分配 | CPU 调度 |
| 内存 | 独立地址空间 | 共享进程堆/方法区 |
| 私有 | — | 计数器、虚拟机栈、本地方法栈 |
| 开销 | 更重 | 相对轻 |

### 1.2 创建线程的方式？本质是什么？

1. 继承 `Thread`  
2. 实现 `Runnable`  
3. `Callable` + `FutureTask`  
4. **线程池**（推荐）  

**本质：** 最终都是创建 `Thread`，由 JVM/OS 调度执行 `run` 中的任务。  
接口方式更好：不占继承、任务与执行解耦。

### 1.3 六种状态及转换？

```text
NEW → RUNNABLE ⇄ BLOCKED / WAITING / TIMED_WAITING → TERMINATED
```

| 状态 | 含义 |
|------|------|
| NEW | new 出未 start |
| RUNNABLE | 可运行（含就绪+运行） |
| BLOCKED | 等 synchronized 锁 |
| WAITING | 无限等（wait/join/park） |
| TIMED_WAITING | 限时等（sleep/wait(t)） |
| TERMINATED | 结束 |

### 1.4 sleep 与 wait 区别？wait 为何在 Object？

| | sleep | wait |
|--|-------|------|
| 归属 | Thread | Object |
| 锁 | **不释放** 监视器锁 | **释放** 锁 |
| 唤醒 | 时间到自动 | notify/notifyAll 或超时 wait |
| 使用 | 任意处 | 必须在同步块内 |

- wait 在 Object：锁是对象级的，任意对象都可作监视器。

### 1.5 start 与 run？

- `start()`：启动**新线程**，线程再调 run  
- 直接 `run()`：当前线程普通方法调用，**不开新线程**

### 1.6 上下文切换？开销？

- CPU 从一个线程切到另一个：保存/恢复寄存器、PC 等。  
- **开销**：耗 CPU、缓存失效、吞吐下降。  
- 线程过多 → 切换频繁 → 要控并发（线程池）。

---

## 2. synchronized

### 2.1 实现原理？

- 语义：互斥 + 可见（解锁 happens-before 后续加锁）。  
- 字节码：`monitorenter` / `monitorexit`（代码块）；方法用 ACC_SYNCHRONIZED。  
- 重量级：对象关联 **Monitor（管程）**，争用时阻塞。  
- 对象头 **Mark Word** 记录锁状态。

### 2.2 锁升级过程？（必画图口述）

```text
无锁 → 偏向锁 → 轻量级锁（自旋/CAS） → 重量级锁（OS 互斥）
```

| 阶段 | 场景 | 手段 |
|------|------|------|
| 偏向 | 无竞争，总同一线程 | Mark 偏向线程 ID |
| 轻量 | 轻度竞争 | CAS 自旋 |
| 重量 | 竞争激烈 | 阻塞挂起 |

- JDK 对偏向默认策略有版本差异，面试说清**动机：从偏到重逐步增加成本**。

### 2.3 修饰方法 vs 代码块？

| | 实例方法 | 静态方法 | 代码块 |
|--|----------|----------|--------|
| 锁对象 | this | Class | 指定对象 |

- 代码块锁粒度更可控。

### 2.4 锁优化：粗化 / 消除 / 自适应自旋？

- **锁粗化**：相邻同步合并，减加解锁次数  
- **锁消除**：逃逸分析证明无共享则去掉同步  
- **自适应自旋**：自旋次数动态调整  

### 2.5 synchronized vs ReentrantLock？

| | synchronized | ReentrantLock |
|--|--------------|---------------|
| 层次 | JVM | API（AQS） |
| 可中断 | 获取时基本否 | lockInterruptibly |
| 公平 | 非公平 | 可公平/非公平 |
| 条件 | 单 wait 集 | 多 Condition |
| 释放 | 自动 | 必须 unlock（finally） |
| 超时 | 不直接支持 | tryLock(timeout) |

---

## 3. volatile

### 3.1 作用？

1. **可见性**  
2. **有序性**（禁部分重排）  
3. **不保证原子性**  

### 3.2 底层？

- 内存屏障（Memory Barrier）  
- 写后读前等屏障保证可见与禁止重排  
- 简化理解：写尽快刷新，读尽量从主存语义可见  

### 3.3 为什么 i++ 不安全？volatile 能解决吗？

- i++ = 读 + 改 + 写，多线程交错丢更新  
- **volatile 不能**让 i++ 原子；用锁或 AtomicInteger  

### 3.4 DCL 单例为何 volatile？

- `new` 可能重排为：分配 → 赋值引用 → 构造  
- 其他线程看到非 null 但未初始化完  
- volatile 禁止重排，保证安全发布  

---

## 4. 线程池（重中之重）

### 4.1 为什么用线程池？new Thread 问题？

- 复用线程，控并发，统一管理  
- 直接 new：创建销毁贵、无线程上限、难监控、易 OOM/打垮系统  

### 4.2 七大参数？

| 参数 | 含义 |
|------|------|
| corePoolSize | 核心线程数 |
| maximumPoolSize | 最大线程数 |
| keepAliveTime + unit | 非核心空闲存活 |
| workQueue | 任务队列 |
| threadFactory | 线程工厂（命名） |
| handler | 拒绝策略 |

### 4.3 完整工作流程？

```text
提交任务
 → 线程数 < core ？ 建核心线程执行
 → 否则 入队
 → 队列满 且 线程数 < max ？ 建非核心线程
 → 否则 拒绝策略
```

### 4.4 四种拒绝策略？

| 策略 | 行为 | 场景直觉 |
|------|------|----------|
| AbortPolicy | 抛异常（默认） | 需感知失败 |
| CallerRunsPolicy | 调用者跑 | 降速、反压 |
| DiscardPolicy | 丢弃 | 可丢的日志类 |
| DiscardOldestPolicy | 丢最老再试 | 新任务优先 |

### 4.5 为何不推荐 Executors？

- Fixed/Single：默认**无界队列** → 堆积 OOM  
- Cached：最大线程过大 → 过多线程  
- **手写 ThreadPoolExecutor** + 有界队列 + 明确拒绝 + 线程命名  

### 4.6 如何设核心线程数？

| 类型 | 方向 |
|------|------|
| CPU 密集 | ≈ CPU 核数 或 核数+1 |
| IO 密集 | 可更大：核数 × (1 + 等待/计算) 作起点 |
| 实际 | **压测**调队列长度、拒绝率、耗时 |

### 4.7 execute vs submit？

| | execute | submit |
|--|---------|--------|
| 返回 | void | Future |
| 异常 | 线程内未捕获处理 | Future.get 可拿到异常 |
| 用途 | 纯跑 | 要结果/异常 |

### 4.8 优雅关闭？

| | shutdown | shutdownNow |
|--|----------|-------------|
| 行为 | 不再接新任务，**执行完队列** | 尝试**中断**，返回未执行列表 |
| 配合 | awaitTermination 等待结束 | 需处理中断语义 |

---

## 5. CAS 与原子类

### 5.1 什么是 CAS？

- Compare-And-Swap：内存 V、期望 A、新值 B；V==A 才写成 B  
- CPU 原语支持；乐观更新  

### 5.2 三大问题？

1. **ABA**  
2. **自旋开销**（一直失败空转）  
3. **只能保证一个变量**原子  

### 5.3 ABA 怎么解？

- `AtomicStampedReference`（版本戳）  
- `AtomicMarkableReference`（标记）  

### 5.4 AtomicInteger 原理？

- volatile value + Unsafe CAS 循环更新  
- 高并发计数可优先 **LongAdder**（分段）  

---

## 6. AQS

### 6.1 核心思想？

- 构建锁/同步器的**框架**  
- **volatile int state** + **CLH 变体等待队列** + CAS  
- **模板方法**：子类实现 tryAcquire/tryRelease（或共享版）  

### 6.2 独占 vs 共享？

| 模式 | 含义 | 例 |
|------|------|-----|
| 独占 | 同一时刻一个线程 | ReentrantLock |
| 共享 | 多个线程可同时 | Semaphore、CountDownLatch |

### 6.3 state 与 CLH 队列？

- state：同步状态（重入次数、许可数等语义由子类定）  
- 队列：获取失败的线程以 Node 形式排队，被唤醒后重试  

### 6.4 基于 AQS 的工具？

ReentrantLock、Semaphore、CountDownLatch、ReentrantReadWriteLock、部分 BlockingQueue 内部同步等。

---

# 二、高频

## 7. ThreadLocal

### 7.1 原理？

- 每个 Thread 有 `ThreadLocalMap`  
- key：ThreadLocal（**弱引用**）；value：强引用存值  

### 7.2 内存泄漏？如何避免？

- key 被回收后 value 仍挂 map，线程池线程长期活着 → 泄漏  
- **用完 remove()**（try/finally）  

### 7.3 InheritableThreadLocal？父子传递？

- InheritableThreadLocal：子线程创建时**拷贝**父线程可继承的值  
- 线程池里子线程复用时可能拿旧值 → 用 TransmittableThreadLocal 等方案（了解）或业务显式传参  

---

## 8. 死锁

### 8.1 四必要条件？

1. 互斥  
2. 请求与保持  
3. 不剥夺  
4. 循环等待  

### 8.2 排查？

- `jstack` 可报告 deadlocks  
- JConsole / VisualVM / Arthas  
- 结合日志与锁顺序  

### 8.3 预防？

- 固定加锁顺序  
- tryLock 超时  
- 缩小锁范围、避免嵌套  
- 破坏四条件之一  

---

## 9. 并发工具类

| 工具 | 作用 | 场景 |
|------|------|------|
| CountDownLatch | 等一组完成（倒数） | 主线程等 N 任务 |
| CyclicBarrier | 一组互等到齐（可重用） | 分阶段计算 |
| Semaphore | 许可证限流 | 接口限流、资源池 |

### Latch vs Barrier

| | Latch | Barrier |
|--|-------|---------|
| 关系 | 一个等多个 | 多个互等 |
| 重用 | 否 | 是 |

### Semaphore 限流直觉

- 许可 N：最多 N 个线程同时进入；`acquire`/`release`。  

---

## 10. JMM

### 10.1 什么是 JMM？

- Java 内存模型：规范线程如何与**主内存**交互（抽象）。  
- 每线程有**工作内存**缓存变量副本；可见性靠同步机制刷新。  

### 10.2 原子 / 可见 / 有序如何保证？

| 特性 | 手段 |
|------|------|
| 原子 | 锁、CAS/原子类 |
| 可见 | volatile、synchronized、final 等 |
| 有序 | volatile、锁、hb 规则 |

### 10.3 Happens-Before 主干？

程序顺序、锁、volatile、start/join、传递性等。  
作用：定义「谁的写对谁可见」。

### 10.4 指令重排与 as-if-serial？

- 编译器/CPU 可重排提性能。  
- **as-if-serial**：单线程语义不变。  
- 多线程靠 volatile/锁禁止非法重排。  

---

## 11. 锁补充

| 概念 | 要点 |
|------|------|
| 悲观锁 | 认为冲突多，先加锁（synchronized） |
| 乐观锁 | 认为冲突少，CAS 更新 |
| 公平锁 | 近似排队；非公平吞吐通常更好 |
| 可重入 | 同线程可再次获得同一锁 |
| 读写锁 | 读多写少：ReadWriteLock |

---

# 三、中频

## 12. BlockingQueue

| 类 | 特点 |
|----|------|
| ArrayBlockingQueue | 有界数组 |
| LinkedBlockingQueue | 链表，可选有界 |
| SynchronousQueue | 不存元素，直接交接 |
| PriorityBlockingQueue | 无界优先级 |
| DelayQueue | 延迟 |

### 生产者-消费者

- 一生产一消费：BlockingQueue `put`/`take` 最简。  
- 线程池工作队列即生产消费模型。  

## 13. CompletableFuture

- 异步编排：`supplyAsync`、`thenApply`、`thenCombine`、`exceptionally`  
- **陷阱**：默认公共 ForkJoinPool，生产应 **自定义线程池**  
- 异常要 exceptionally/handle，否则难察觉  

## 14. Fork/Join

- 分治 + **工作窃取**（空闲线程偷任务）  
- `RecursiveTask` / `RecursiveAction`  
- 适合可拆分 CPU 计算  

## 15. 如何保证线程安全？

- synchronized / Lock  
- CAS / 原子类  
- 并发容器（CHM 等）  
- ThreadLocal（隔离，非共享安全）  
- 不可变对象、限制共享  

## 16. 线程中断

| API | 含义 |
|-----|------|
| interrupt() | 设置中断标志 / 打断阻塞 |
| isInterrupted() | 查标志（不清除） |
| interrupted() | 静态，查并**清除** |

- 阻塞方法响应中断抛 InterruptedException，需恢复中断状态或退出。  

---

# 四、低频 / 进阶加分

## 17. 虚拟线程（Loom）

- JVM 调度轻量线程，适合 **大量阻塞 IO**  
- **不适合**长时间 CPU 密集  
- synchronized 可能钉住载体线程；热点可用 ReentrantLock  

## 18. 其他加分

- Mark Word 锁升级细节  
- AQS acquire 流程：tryAcquire → addWaiter → acquireQueued  
- Condition await/signal  
- LongAdder 分段优于 AtomicLong 高竞争计数  
- 线程池：`setCorePoolSize` 等动态调整（需理解运行中影响）  
- 监控：活跃线程、队列长度、完成任务数、拒绝次数  
- StampedLock 乐观读  

---

# 自测清单

### P0
- [ ] 线程池流程 + 七参数 + 拒绝 + Executors 坑 + 设参  
- [ ] 锁升级四阶段 + vs ReentrantLock  
- [ ] volatile 三性 + DCL + i++  
- [ ] CAS 三问题 + AQS 一句话  

### P1
- [ ] ThreadLocal 泄漏与 remove  
- [ ] 死锁四条件 + jstack  
- [ ] Latch/Barrier/Semaphore  

### P2–P3
- [ ] hb 五条主干  
- [ ] 阻塞队列选型  
- [ ] CF 自定义池  
- [ ] 虚拟线程场景  

**口述：** [并发面渣级口述.md](./并发面渣级口述.md)  
**卡片：** [并发卡片速记.md](./并发卡片速记.md)  
**频率：** [并发八股频率排序.md](./并发八股频率排序.md)  

---

## 点名深挖

- 线程池完整流程 + 参数设计案例  
- synchronized 锁升级画图版  
- AQS 获取释放流程  
- ThreadLocal 泄漏完整分析  

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 按超高/高/中/低频大纲重写并发完整卷 |
"""

RANK = f"""# 并发编程 · 频率导航（2025–2026）

> **完整卷：** [并发高频面试题与知识点.md](./并发高频面试题与知识点.md)  
> **面渣：** [并发面渣级口述.md](./并发面渣级口述.md) · **卡片：** [并发卡片速记.md](./并发卡片速记.md)  
> **全库主线：** [四档 P0](./Java后端面试频率-四档.md)

---

## 专项时间（并发内部）

| 优先级 | 模块 | 时间 |
|--------|------|:----:|
| P0 | 线程池 + synchronized + volatile + CAS + AQS | 50% |
| P1 | ThreadLocal + 死锁 + Latch/Barrier/Semaphore | 20% |
| P2 | JMM + HB + 乐观/悲观锁 | 15% |
| P3 | BlockingQueue + CF + 虚拟线程 | 15% |

---

## 一、超高频

| # | 主题 | 完整卷 |
|---|------|--------|
| 1 | 线程基础（进程线程/状态/sleep wait/start run/切换） | [§1](./并发高频面试题与知识点.md) |
| 2 | synchronized（原理/升级/优化/vs Lock） | [§2](./并发高频面试题与知识点.md) |
| 3 | volatile（屏障/i++/DCL） | [§3](./并发高频面试题与知识点.md) |
| 4 | **线程池**（参数/流程/拒绝/Executors/设参/关闭） | [§4](./并发高频面试题与知识点.md) |
| 5 | CAS + 原子类 | [§5](./并发高频面试题与知识点.md) |
| 6 | AQS | [§6](./并发高频面试题与知识点.md) |

---

## 二、高频

ThreadLocal · 死锁 · 工具类 · JMM · 乐观悲观/公平可重入/读写锁  
→ [完整卷 二](./并发高频面试题与知识点.md)

---

## 三、中频

BlockingQueue · 生产者消费者 · CompletableFuture · ForkJoin · 中断  
→ [完整卷 三](./并发高频面试题与知识点.md)

---

## 四、低频加分

虚拟线程 · Mark Word 细节 · AQS 源码流程 · Condition · LongAdder · 池监控与动态调参 · StampedLock  

---

## 追问链（线程池）

```text
参数怎么设？ → 拒绝策略？ → 为何不用 Executors？
→ 如何监控？ → 能否动态调？ → 项目里怎么配的？
```

---

## 点名

`线程池` · `锁升级` · `AQS` · `ThreadLocal泄漏` · `虚拟线程`

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 并发专项频率导航 |
"""

CARDS = f"""# 并发 · 卡片速记

<!-- NAV:START -->
> [完整卷](./并发高频面试题与知识点.md) · [频率](./并发八股频率排序.md) · [面渣](./并发面渣级口述.md)
<!-- NAV:END -->

> 遮住 A。**先 P0。**

---

## 线程基础

**Q1 进程 vs 线程？** A: 资源分配 vs 调度；共享堆。

**Q2 六状态？** A: NEW/RUNNABLE/BLOCKED/WAITING/TIMED_WAITING/TERMINATED。

**Q3 sleep vs wait？** A: 不释放锁 vs 释放；wait 在 Object。

**Q4 start vs run？** A: 启新线程 vs 普通调用。

**Q5 上下文切换？** A: 保存恢复现场；过多损吞吐。

## synchronized / Lock

**Q6 原理关键字？** A: monitorenter；Mark Word；Monitor。

**Q7 锁升级？** A: 偏向→轻量→重量。

**Q8 vs ReentrantLock？** A: 可中断/公平/多Condition/手动unlock。

**Q9 锁消除粗化？** A: 逃逸消除同步；合并相邻锁。

## volatile

**Q10 三性？** A: 可见+有序；不原子。

**Q11 i++？** A: 读改写三步；volatile 不够。

**Q12 DCL？** A: 防 new 重排；需 volatile。

## 线程池 P0

**Q13 为何用池？** A: 复用、控并发、好管理。

**Q14 七参数？** A: core/max/keepAlive/unit/queue/factory/handler。

**Q15 流程？** A: core→队列→max→拒绝。

**Q16 拒绝4？** A: Abort/CallerRuns/Discard/DiscardOldest。

**Q17 Executors 坑？** A: 无界队列OOM/线程爆炸。

**Q18 设参？** A: CPU≈核数；IO更大；压测。

**Q19 execute vs submit？** A: void vs Future。

**Q20 关闭？** A: shutdown 跑完队列；shutdownNow 中断。

## CAS / AQS

**Q21 CAS？** A: 比较交换；ABA/自旋/单变量。

**Q22 ABA？** A: AtomicStampedReference。

**Q23 AQS？** A: state+CLH队列+模板方法。

**Q24 独占共享？** A: Lock vs Semaphore/Latch。

## 高频

**Q25 ThreadLocal 泄漏？** A: 弱key强value；池化remove。

**Q26 死锁四条件？** A: 互斥、请求保持、不剥夺、环路。

**Q27 Latch vs Barrier？** A: 一个等多个 / 互等可重用。

**Q28 Semaphore？** A: 许可证限流。

**Q29 JMM？** A: 主内存与工作内存；hb 保可见有序。

**Q30 乐观悲观？** A: CAS vs 先加锁。

## 中频 / 加分

**Q31 阻塞队列？** A: Array有界；Linked；Synchronous交接。

**Q32 CF 陷阱？** A: 默认公共池；要自定义池。

**Q33 虚拟线程？** A: 适阻塞IO；不适重CPU。

**Q34 LongAdder？** A: 分段计数，高竞争更优。

---

详解：[并发高频面试题与知识点.md](./并发高频面试题与知识点.md)
"""


def patch():
    # four tier link to concurrency freq
    ft = DOCS / "Java后端面试频率-四档.md"
    if ft.exists():
        t = ft.read_text(encoding="utf-8")
        if "并发八股频率排序" not in t:
            t = t.replace(
                "🗣️ [并发面渣](./并发面渣级口述.md) · 🃏 [并发卡](./并发卡片速记.md)",
                "🗣️ [并发面渣](./并发面渣级口述.md) · 🃏 [并发卡](./并发卡片速记.md) · 🔥 [并发频率](./并发八股频率排序.md)",
            )
            ft.write_text(t, encoding="utf-8")
            print("fourtier")

    sb = DOCS / "_sidebar.md"
    if sb.exists():
        t = sb.read_text(encoding="utf-8")
        if "并发八股频率排序" not in t:
            t = t.replace(
                "  * [并发](并发高频面试题与知识点.md) · [卡片](并发卡片速记.md)\n",
                "  * [并发完整卷](并发高频面试题与知识点.md) · [频率](并发八股频率排序.md) · [卡片](并发卡片速记.md)\n",
            )
            sb.write_text(t, encoding="utf-8")
            print("sidebar")

    ov = DOCS / "Java八股模块总览.md"
    if ov.exists():
        t = ov.read_text(encoding="utf-8")
        if "并发八股频率排序" not in t:
            t = t.replace(
                "| 2 **并发完整卷** | [并发](./并发高频面试题与知识点.md) |",
                "| 2 **并发完整卷** | [并发](./并发高频面试题与知识点.md) · [频率](./并发八股频率排序.md) |",
            )
            ov.write_text(t, encoding="utf-8")
            print("overview")


def main():
    w("并发高频面试题与知识点.md", CONC)
    w("并发八股频率排序.md", RANK)
    w("并发卡片速记.md", CARDS)
    patch()


if __name__ == "__main__":
    main()
