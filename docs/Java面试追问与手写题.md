# Java 面试 · 追问三连（合集）+ 手写题

> 总序：[README.md](./README.md)。  
> **追问已拆分（推荐按轨打开）：**  
> - [追问三连-Java.md](./追问三连-Java.md)  
> - [追问三连-Python.md](./追问三连-Python.md)  
> - [追问三连-AI.md](./追问三连-AI.md)  
>
> 本文保留 **Java 轨详细追问 + 手写代码**（LRU/单例等）。Python/AI 追问请用分册。

### 追问练习优先级（Java）

| 级 | 模块 | 必练 |
|----|------|------|
| **P0** | HashMap、线程池、volatile、事务、三级缓存、索引、缓存三连、分布式锁 | 是 |
| **P1** | CHM、AQS、ThreadLocal、MVCC、慢 SQL、MQ | 社招 |
| **P2** | 其余 | 有空 |

**手写 P0：** 单例 DCL → LRU → 生产者消费者  

---

## 一、使用方法

| 场景 | 做法 |
|------|------|
| 自测 | 遮住「答」，只看「追问」，限时 30～45 秒 |
| 对练 | 主问题 + 连问 3 个追问 |
| 手写 | 先结构图 → 核心方法 → 复杂度与坑 |

**原则：** 结论 → 原理一句 → 实践/对比。

---

## 二、高频追问三连（按面试频率大致排序）

### 2.1 HashMap（P0）

**主问：** HashMap 底层原理？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | 为什么链表转红黑树阈值是 8，退化是 6？ | 泊松分布下很长链概率低；8 折中查找成本；6 与 8 留间隙防边界反复树化/退化 |
| 2 | 扩容时元素如何迁移？为什么容量是 2 的幂？ | 新下标=原下标或 原+oldCap；位运算代替取模，高效且分布均匀 |
| 3 | 多线程 put 会怎样？JDK7/8 差异？ | 丢数据、数据覆盖；JDK7 扩容可能死链；JDK8 改善死链但仍不安全 → 用 CHM |

**再追可选：** hash 扰动为什么 `^ (h>>>16)`？→ 让高位参与低位运算，减少碰撞。

---

### 2.2 ConcurrentHashMap

**主问：** ConcurrentHashMap 怎么保证线程安全？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | get 要加锁吗？为什么？ | 一般不加；Node 的 val/next 等 volatile，读可见 |
| 2 | size() 准确吗？怎么实现？ | 高并发下是近似统计；baseCount + CounterCell 分段累加，类似 LongAdder |
| 3 | 为什么不允许 null？和 HashMap 不同？ | 并发下无法区分「key 不存在」和「值就是 null」；HashMap 单线程可约定 |

**再追可选：** 扩容怎么多线程协助？→ transfer 推进 stride，线程认领区间迁移。

---

### 2.3 线程池

**主问：** 讲一下线程池参数和执行流程。

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | 核心线程会超时回收吗？ | 默认不；允许 `allowCoreThreadTimeOut(true)` 后可回收 |
| 2 | 队列选有界还是无界？ | 生产优先有界，防 OOM；无界时 maximumPoolSize 往往形同虚设（队不满不建非核心） |
| 3 | 如何设置线程数？ | CPU 密 ≈ N+1；IO 密更大；最终压测；按业务隔离池，监控队列与拒绝 |

**再追可选：** 关闭线程池 shutdown 与 shutdownNow？→ 前者不接新任务等执行完；后者尝试中断。

---

### 2.4 volatile / CAS / 单例

**主问：** volatile 有什么用？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | 能保证 i++ 原子吗？ | 不能；要 AtomicInteger 或锁 |
| 2 | 和 synchronized 区别？ | volatile 无互斥无原子复合操作；sync 三者都可保证但更重 |
| 3 | DCL 单例为什么要 volatile？ | 防指令重排，避免看到「半初始化」对象 |

**CAS 追问：** ABA 怎么解？→ 版本号 StampedReference；自旋太久怎么办？→ 分段 LongAdder / 阻塞锁。

---

### 2.5 AQS

**主问：** 说一下 AQS。

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | state 是什么？ | 同步状态；锁重入次数、许可数等语义由子类定义 |
| 2 | 独占和共享区别？ | 独占仅一线程（Lock）；共享可多线程（Semaphore/Latch） |
| 3 | 条件队列 Condition 和同步队列关系？ | await 进条件队列；signal 转移到 AQS 同步队列再竞争 |

---

### 2.6 ThreadLocal

**主问：** ThreadLocal 原理？泄漏吗？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | key 为什么弱引用？ | 方便 ThreadLocal 本身被回收；但 value 仍强引用 → 要 remove |
| 2 | 线程池里为什么更危险？ | 线程复用不销毁，value 长期挂着 |
| 3 | InheritableThreadLocal / 透传？ | 子线程可继承；线程池透传用阿里 TransmittableThreadLocal 等 |

---

### 2.7 synchronized vs Lock

**主问：** 两者区别？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | 什么时候必须用 Lock？ | tryLock 超时、可中断、多 Cond、公平锁 |
| 2 | 锁升级了解吗？ | 偏向→轻量→重量（JDK 版本差异可提 15+ 偏向默认关） |
| 3 | 锁粗化、锁消除？ | JIT 优化：合并循环锁、逃逸分析消除无竞争锁 |

---

### 2.8 Spring 循环依赖

**主问：** 三级缓存怎么解决循环依赖？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | 为什么要三级不只二级？ | 可能需要提前暴露「代理对象」，三级放 ObjectFactory 延迟生成 |
| 2 | 构造器注入循环行不行？ | 不行；创建阶段就需要对方实例 |
| 3 | 怎么从设计上避免？ | 拆分职责、事件驱动、`@Lazy`、改构造依赖方向 |

---

### 2.9 Spring 事务

**主问：** @Transactional 失效场景？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | 同类自调用怎么修？ | 注入自己/AopContext、拆 Bean、TransactionTemplate |
| 2 | REQUIRED 与 REQUIRES_NEW？ | 前者加入已有事务；后者挂起旧事务开新事务 |
| 3 | 只读事务有用吗？ | 可提示优化、某些场景防脏写；不是银弹 |

---

### 2.10 Bean 生命周期 / AOP

**主问：** Bean 生命周期？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | AOP 代理在哪一步？ | 常在 BeanPostProcessor 后置处理 |
| 2 | Filter 和 Interceptor 顺序？ | Filter（Servlet）更靠前，再 DispatcherServlet/Interceptor |
| 3 | @Async 失效？ | 同类自调用、没 @EnableAsync、返回值/异常处理不当 |

---

### 2.11 MySQL 索引

**主问：** 索引为什么用 B+ 树？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | 和哈希索引比？ | 哈希等值快，不支持范围/排序；InnoDB 主选 B+ |
| 2 | 联合索引 (a,b,c) 查 b 能用吗？ | 一般不能有效用最左；除非跳过扫描等特殊优化，别默认能用 |
| 3 | 索引是不是越多越好？ | 否；占空间、拖慢写；按查询构建 |

---

### 2.12 事务隔离 / MVCC

**主问：** RR 下如何避免幻读？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | MVCC 能解决所有幻读吗？ | 快照读靠 MVCC；当前读靠间隙锁/临键锁 |
| 2 | RC 和 RR ReadView 差异？ | RC 每条语句新 ReadView；RR 事务开始（首次读）创建沿用 |
| 3 | 长事务危害？ | 版本链过长、锁久、purge 慢、主从延迟 |

---

### 2.13 慢 SQL

**主问：** 如何优化慢 SQL？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | explain 看哪些？ | type、key、rows、Extra |
| 2 | Using filesort 怎么办？ | 排序字段契合索引，避免额外排序 |
| 3 | 深分页？ | 延迟关联 / 基于上次 id 翻页 |

---

### 2.14 Redis 缓存三连

**主问：** 穿透、击穿、雪崩？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | 空值缓存会不会爆内存？ | 设短 TTL；布隆过滤减少无效 key |
| 2 | 互斥锁重建会不会打死 DB？ | 锁粒度按 key；失败快速返回或排队；热点本地缓存 |
| 3 | 双写一致性最终方案？ | 先更 DB 再删缓存 + 重试/订阅 binlog；接受最终一致 |

---

### 2.15 Redis 分布式锁

**主问：** 怎么实现分布式锁？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | 为什么用 Lua 删锁？ | 校验 value 与 del 原子，防误删别人锁 |
| 2 | 业务超时锁过期？ | 看门狗续期（Redisson）；或评估超时时间 |
| 3 | 主从切换锁丢？ | 存在风险；业务可接受 or  fencing token / 讨论 RedLock 争议 |

---

### 2.16 MQ

**主问：** 如何保证消息不被丢？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | 重复消费怎么办？ | 幂等：唯一键、状态机、Token |
| 2 | 顺序消息？ | 同 key 同分区 + 单线程消费 |
| 3 | 事务消息？ | 半消息/本地消息表，保证本地事务与发消息最终一致 |

---

### 2.17 JVM 场景（与专篇互补）

**主问：** 线上 Full GC 频繁？

| # | 追问 | 参考答要点 |
|---|------|------------|
| 1 | 怎么区分泄漏还是堆小？ | Full GC 后 Old 是否降下来 |
| 2 | dump 会有什么副作用？ | STW/IO；高峰慎用 live dump |
| 3 | 容器 OOMKilled 但无 Java OOM？ | RSS 超 cgroup；非堆+堆外未计入 -Xmx |

更全见 JVM 专篇第十一章。

---

### 2.18 项目深挖通用追问

**主问：** 介绍一个项目难点。

| # | 追问 | 应答策略 |
|---|------|----------|
| 1 | 为什么选 A 不选 B？ | 给 2 个对比维度（性能/复杂度/一致性） |
| 2 | 数据量、QPS、RT 多少？ | 准备真实或合理数量级 |
| 3 | 出过线上问题吗？ | STAR：现象→排查→根因→结果→预防 |

---

## 三、手写题清单（高频）

### 3.1 出现频率分级

| 频率 | 题目 |
|------|------|
| ★★★★★ | 单例（DCL/静态内部类/枚举）、LRU Cache、生产者消费者 |
| ★★★★☆ | 阻塞队列、交替打印、倒序/链表/栈相关算法、手写锁粗粒度 demo |
| ★★★☆☆ | 简易线程池思路、限流器、发布订阅、深拷贝 |
| 算法交叉 | 二分、快排/堆排思路、二叉树遍历、滑动窗口（按公司另备） |

### 3.2 单例 · DCL

```java
public class Singleton {
    private static volatile Singleton INSTANCE;

    private Singleton() {}

    public static Singleton getInstance() {
        if (INSTANCE == null) {
            synchronized (Singleton.class) {
                if (INSTANCE == null) {
                    INSTANCE = new Singleton();
                }
            }
        }
        return INSTANCE;
    }
}
```

**口述要点：** 双检减少同步；volatile 防重排；私有构造。

**枚举版（加分）：**

```java
public enum SingletonEnum {
    INSTANCE;
    public void doSomething() {}
}
```

### 3.3 静态内部类单例

```java
public class SingletonHolder {
    private SingletonHolder() {}
    private static class Holder {
        private static final SingletonHolder I = new SingletonHolder();
    }
    public static SingletonHolder getInstance() {
        return Holder.I;
    }
}
```

**要点：** 类加载延迟初始化 + 线程安全。

---

### 3.4 LRU Cache（LinkedHashMap 版 · 面试最快）

```java
public class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;

    public LRUCache(int capacity) {
        super(capacity, 0.75f, true); // accessOrder = true
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}
```

**要点：** accessOrder 访问排序；超容删最老。  
**追问：** 线程安全？→ Collections.synchronizedMap 或自己加锁；或用 ConcurrentHashMap + 并发链表（复杂）。

### 3.5 LRU · HashMap + 双向链表（手写完整）

**结构：**

```text
HashMap<K, Node>  // O(1) 查找
双向链表：头=最新，尾=最旧（或相反，统一即可）
get：移到头
put：存在则更新并移头；不存在则加头，超容删尾
```

```java
public class LRUCacheManual {
    private static class Node {
        int key, val;
        Node prev, next;
        Node(int k, int v) { key = k; val = v; }
    }

    private final int capacity;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0); // dummy
    private final Node tail = new Node(0, 0);

    public LRUCacheManual(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        Node n = map.get(key);
        if (n == null) return -1;
        moveToHead(n);
        return n.val;
    }

    public void put(int key, int value) {
        Node n = map.get(key);
        if (n != null) {
            n.val = value;
            moveToHead(n);
            return;
        }
        Node node = new Node(key, value);
        map.put(key, node);
        addToHead(node);
        if (map.size() > capacity) {
            Node last = tail.prev;
            remove(last);
            map.remove(last.key);
        }
    }

    private void moveToHead(Node n) {
        remove(n);
        addToHead(n);
    }

    private void addToHead(Node n) {
        n.next = head.next;
        n.prev = head;
        head.next.prev = n;
        head.next = n;
    }

    private void remove(Node n) {
        n.prev.next = n.next;
        n.next.prev = n.prev;
    }
}
```

**复杂度：** get/put O(1) 均摊。

---

### 3.6 生产者消费者 · BlockingQueue

```java
public class ProducerConsumer {
    private final BlockingQueue<Integer> queue = new ArrayBlockingQueue<>(100);

    public void start() {
        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < 1000; i++) {
                    queue.put(i); // 满则阻塞
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        Thread consumer = new Thread(() -> {
            try {
                while (true) {
                    Integer v = queue.take(); // 空则阻塞
                    // process v
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });

        producer.start();
        consumer.start();
    }
}
```

**口述：** 有界队列解耦与削峰；put/take 阻塞；也可用 wait/notify 手写。

### 3.7 生产者消费者 · wait/notify

```java
public class WaitNotifyQueue<T> {
    private final Queue<T> q = new LinkedList<>();
    private final int max;

    public WaitNotifyQueue(int max) { this.max = max; }

    public synchronized void put(T t) throws InterruptedException {
        while (q.size() == max) wait();
        q.offer(t);
        notifyAll();
    }

    public synchronized T take() throws InterruptedException {
        while (q.isEmpty()) wait();
        T t = q.poll();
        notifyAll();
        return t;
    }
}
```

**坑：** 用 **while** 不 if（防虚假唤醒）；notifyAll 更稳妥。

---

### 3.8 交替打印 A/B

```java
public class AlternatePrint {
    private final Object lock = new Object();
    private boolean aTurn = true;

    public void printA() {
        for (int i = 0; i < 10; i++) {
            synchronized (lock) {
                while (!aTurn) {
                    try { lock.wait(); } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
                System.out.print("A");
                aTurn = false;
                lock.notifyAll();
            }
        }
    }

    public void printB() {
        for (int i = 0; i < 10; i++) {
            synchronized (lock) {
                while (aTurn) {
                    try { lock.wait(); } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
                System.out.print("B");
                aTurn = true;
                lock.notifyAll();
            }
        }
    }
}
```

**加分：** Lock + Condition、或 Semaphore(1) 两个信号量。

---

### 3.9 有界阻塞队列（口述 + 骨架）

```java
// 数组 + putIndex/takeIndex/count
// put: while full wait; 写入; count++; notifyAll
// take: while empty wait; 读出; count--; notifyAll
// 注意取模环形缓冲区
```

---

### 3.10 简易限流 · 令牌桶思路（口述）

```text
桶容量 capacity，速率 rate 令牌/秒
每个请求 take(1)：
  先根据时间差补充令牌（不超过 capacity）
  若 tokens >= 1 则减一并放行，否则拒绝
```

**面试点：** 与漏桶区别（令牌允许突发到桶容量）；分布式用 Redis + Lua。

---

### 3.11 手写同步工具语义（不必完整 AQS）

**面试常说即可：**

| 手写语义 | 要点 |
|----------|------|
| 不可重入锁 | state 0/1 + 队列 |
| 可重入锁 | state 重入计数 + owner 线程 |
| 门闩 CountDown | state=N，await 直到 0，countDown CAS 减 |

---

### 3.12 常见算法手写（Java 岗交叉）

按目标公司准备，下列为「Java 岗也常默写」：

| 题 | 要点 |
|----|------|
| 反转链表 | 迭代三指针 / 递归 |
| 合并两有序链表 | 哑头节点 |
| 二分查找 | 边界 mid |
| 快排 | partition |
| 堆排序 / TopK | 小顶堆 |
| 两数之和 | HashMap |
| 最长无重复子串 | 滑动窗口 |
| 二叉树层序 | 队列 |
| 有效括号 | 栈 |
| 生产者消费者 | 见上 |

---

## 四、手写题临场模板

```text
1. 确认题意：输入输出、线程安全、容量、是否阻塞
2. 说思路：数据结构 + 主流程（30 秒）
3. 写代码：先主干后边界
4. 自测：空、满、单线程、两线程交错
5. 复杂度：时间/空间
6. 改进：线程安全、性能、Java 标准库对应类
```

**印象分：**

- 用 `while` 等条件而非 `if`  
- `interrupt` 正确处理  
- 锁在 finally 释放  
- 变量命名清晰  

---

## 五、模拟面试脚本（60 分钟）

| 时间 | 内容 |
|------|------|
| 0–5 | 自我介绍 + 项目一句话 |
| 5–20 | 项目深挖 + 3 个追问 |
| 20–35 | 八股：HashMap → 线程池 → 事务失效（各带追问） |
| 35–45 | 场景：Full GC 或 OOM 或缓存三连 |
| 45–55 | 手写：LRU 或生产者消费者 |
| 55–60 | 反问 |

**每日训练：** 1 个主问题 + 3 追问 + 1 个手写骨架（30 分钟）。

---

## 六、P0 追问速记卡（考前）

| 主点 | 三连关键词 |
|------|------------|
| HashMap | 8/6、2 幂扩容、并发丢数据 |
| CHM | get 无锁、size 近似、禁 null |
| 线程池 | 核心超时、有界队列、压测设参 |
| volatile | 非原子、vs sync、DCL |
| 三级缓存 | 代理、构造器不行、设计解耦 |
| 事务 | 自调用、REQUIRES_NEW、rollbackFor |
| 索引 | 范围查、最左、不是越多越好 |
| MVCC | 快照读/当前读、RC vs RR ReadView |
| 缓存三连 | 空值TTL、互斥、删缓存 |
| 分布式锁 | Lua、续期、主从风险 |
| 单例 | volatile、枚举、静态内部类 |
| LRU | accessOrder / 哈希+双向链表 |

---

## 七、文档修订记录

| 日期 | 说明 |
|------|------|
| 2026-07-20 | 初版：18 组高频追问三连 + 手写题（单例/LRU/生产者消费者/交替打印等）+ 模拟面试脚本 |
