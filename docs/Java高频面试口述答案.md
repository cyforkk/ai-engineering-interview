# Java 高频面试口述答案全集（跨模块 · 归档向）

> ⚠️ **优先使用各专题 `*面渣级口述.md`（更新、按 P0 排序）。**  
> 本文保留作 **Java 多模块合集速查**，与分册内容有重叠时 **以分册为准**。  
> 总索引：[README.md](./README.md) · 路线图：[学习路线图-4到8周.md](./学习路线图-4到8周.md)  
> 用法：每题 1.5～2.5 分钟；模板：**是什么 → 原理 → 对比/坑点**。

### 口述练习优先级（与主库一致）

| 序 | 级 | 章节 | 先练 |
|:--:|:--:|------|------|
| 1 | P0 | 二、集合 HashMap/CHM | ★★★★★ |
| 2 | P0 | 三、并发·线程池/volatile | ★★★★★ |
| 3 | P0 | 五、MySQL·索引/MVCC | ★★★★★ |
| 4 | P0 | 六、Redis·三连/锁 | ★★★★★ |
| 5 | P0 | 四、Spring·事务/三级缓存 | ★★★★★ |
| 6 | P0 | 一、基础 equals/String | ★★★★☆ |
| 7 | P1 | 七、MQ | ★★★☆☆ |

JVM 排查口述路径见 [JVM专题 · 场景速查](./JVM高频面试题与知识点.md)。

---

## 目录

1. [Java 基础](#一java-基础口述)
2. [集合 · HashMap / ConcurrentHashMap](#二集合口述) ← **P0 优先**
3. [并发编程](#三并发编程口述) ← **P0 优先**
4. [Spring / Spring Boot](#四spring-口述)
5. [MySQL](#五mysql-口述)
6. [Redis](#六redis-口述)
7. [MQ 与分布式简答](#七mq-与分布式口述简答)
8. [速记总表](#八考前速记总表)

---

## 一、Java 基础口述

### 1.1 面向对象 / 抽象类 vs 接口

**口述：**  
面向对象核心是封装、继承、多态（有的还加抽象）。封装藏细节；继承复用；多态同一引用不同实现，靠重写和动态绑定。

抽象类和接口：  
- 抽象类可以有成员变量、构造器、普通方法，表达「is-a」的模板；  
- 接口更偏「能做什么」的契约。Java 8 后接口可有 default/static 方法，Java 9 可有 private 方法，但字段仍默认 `public static final`。  
- 类单继承、可多实现接口，所以扩展能力上接口更灵活。

### 1.2 重载 vs 重写

**口述：**  
重载是同一类中方法名相同、参数列表不同，编译期静态分派。  
重写是子类重新实现父类实例方法，运行时动态分派；返回类型可协变，访问权限不能更严，异常不能更宽。  
`static` 方法不能算多态意义上的重写，只能隐藏。

### 1.3 == 与 equals、hashCode

**口述：**  
`==` 比较基本类型的值，或引用类型的地址。  
`equals` 默认也是比地址，但业务类常重写比内容。  
契约：equals 相等则 hashCode 必须相等；反之不然。  
HashMap 先用 hash 定位桶，冲突后再 equals。只重写 equals 不重写 hashCode，会导致「逻辑相等却进不同桶」，集合行为错乱。

### 1.4 String 为什么不可变

**口述：**  
String 内部字符数组 final，且无对外修改 API，类也是 final。  
好处：常量池可共享、hash 可缓存、作 HashMap key 安全、天然线程安全、涉及安全（类名、文件路径不好被改）。  
拼接大量字符串用 StringBuilder；多线程拼接才考虑 StringBuffer（同步，现代代码更少用）。

### 1.5 String / StringBuilder / StringBuffer

| | String | StringBuilder | StringBuffer |
|--|--------|---------------|--------------|
| 可变 | 否 | 是 | 是 |
| 线程安全 | 是（不可变） | 否 | synchronized |
| 场景 | 少量、不可变 | 单线程拼接 | 遗留多线程拼接 |

### 1.6 Integer 缓存与装箱

**口述：**  
`Integer.valueOf` 对 -128～127 走缓存，这个范围 `==` 可能为 true；范围外是新对象，`==` 为 false。业务比较一律用 `equals`。  
装箱拆箱有性能开销，集合里大量包装类型要注意。

### 1.7 异常体系

**口述：**  
`Throwable` 下分 Error 和 Exception。Error 如 OOM、StackOverflow，一般不捕获恢复。  
Exception 分受检（要处理或声明）和运行时（RuntimeException，如 NPE、IllegalArgument）。  
资源关闭用 try-with-resources，实现 AutoCloseable。

### 1.8 值传递

**口述：**  
Java 只有值传递。传基本类型是值副本；传对象是**引用的副本**。方法里改引用指向不影响实参，但通过引用改对象内部字段会反映到外面。

### 1.9 final / static

**口述：**  
`final` 类不可继承，方法不可重写，变量不可重新赋值；引用 final 只保证引用不变，对象内容仍可能变。  
`static` 属类，随类加载初始化，所有实例共享；静态方法不能直接访问实例成员。

### 1.10 泛型擦除

**口述：**  
泛型主要在编译期约束类型，运行时擦除为裸类型（或边界类型），所以不能 `new T()`、不能靠泛型重载仅参数泛型不同。反射可绕过部分检查。`extends` 上界只读适合生产者，`super` 下界只写适合消费者（PECS）。

### 1.11 反射

**口述：**  
运行时通过 Class、Constructor、Method、Field 创建对象、调方法、改字段。Spring、序列化、注解处理大量使用。  
代价：慢、可破坏封装、安全检查开销。热点路径避免反射或做缓存 Method。

---

## 二、集合口述

### 2.1 ArrayList 底层与扩容

**口述：**  
ArrayList 基于动态 Object 数组。默认空数组，第一次 add 扩到 10（JDK 实现细节以版本为准，表述「默认容量 10」即可）。  
不够时大约 **1.5 倍** 扩容，`Arrays.copyOf` 复制。  
随机访问 O(1)，中间插入删除要搬移 O(n)。  
多线程不安全；遍历删除用迭代器 remove，否则易 CME（fail-fast）。  
已知大小要指定初始容量，减少扩容拷贝。

**对比 LinkedList：** 双向链表，头尾插入快，随机访问慢；实现 Deque。一般更常用 ArrayList。

### 2.2 HashMap 底层原理（必背长答）

**口述结构：** 结构 → put 流程 → 树化 → 扩容 → 线程问题 → hash。

> HashMap 在 JDK8 是 **数组 + 链表 + 红黑树**。  
> 默认容量 16，负载因子 0.75，阈值 = 容量 × 0.75。  
>
> **put：**  
> 1. 算 key 的 hash（hashCode 高 16 位异或低 16 位扰动）；  
> 2. `(n-1) & hash` 定位桶；  
> 3. 桶空则放新节点；  
> 4. 不空则遍历：key 相同（equals）则覆盖；  
> 5. 链表长度达到 8，且数组长度 ≥ 64 时转红黑树，否则优先扩容；  
> 6. 树节点 ≤ 6 退回链表；  
> 7. size 超过阈值则 2 倍扩容。  
>
> **为什么 2 的幂：** 可用位运算代替取模，扩容时元素要么在原下标，要么在「原下标 + 旧容量」。  
> **为什么树化阈值 8：** 泊松分布下很长链表概率极低，8 是时间空间折中；退化 6 有滞后避免边界抖动。  
> **key 为 null：** 允许一个，放在桶 0。  
> **线程不安全：** 并发 put 会丢数据；JDK7 还可能扩容死链。并发用 ConcurrentHashMap。

**get：** 同样算 hash 定位，再 equals 比较。

### 2.3 自定义 key 注意点

**口述：**  
key 应不可变、正确重写 equals/hashCode，且 equals 相等时 hash 一致。若 key 放入后改了参与 hash 的字段，会「丢」在错误桶里。

### 2.4 LinkedHashMap 与 LRU

**口述：**  
LinkedHashMap 在 HashMap 上维护插入序或访问序双向链表。  
设 `accessOrder=true`，并重写 `removeEldestEntry`，可在超过容量时移除最老节点，实现简易 LRU 缓存。

### 2.5 ConcurrentHashMap 原理（JDK8）

**口述：**  
JDK7 是 Segment 分段锁；JDK8 改为 **Node 数组 + CAS + synchronized 锁桶头**。  
- 桶为空：CAS 挂头节点；  
- 桶非空：synchronized 锁头节点，再链表/树插入；  
- 扩容时多线程协助 transfer；  
- 不允许 null key/value；  
- size 用 baseCount + CounterCell，类似 LongAdder，是近似值，高并发下统计更高效。  
get 基本无锁，靠 volatile 语义读到最新。

**对比 Hashtable：** 整表 synchronized，并发差。  
**对比 Collections.synchronizedMap：** 也是粗粒度锁。  
**对比 CHM：** 粒度到桶，读多写少性能好。

### 2.6 HashSet

**口述：**  
内部是 HashMap，元素作 key，value 是固定 PRESENT 对象。去重依赖 equals/hashCode。

### 2.7 fail-fast vs fail-safe

**口述：**  
fail-fast：迭代时用 modCount 检测结构性修改，不一致抛 ConcurrentModificationException，如 ArrayList、HashMap。  
fail-safe：常在拷贝上遍历，如 CopyOnWriteArrayList、ConcurrentHashMap 的弱一致迭代，不抛 CME，但不保证强一致快照语义（视实现）。

### 2.8 CopyOnWriteArrayList

**口述：**  
写时复制整个数组，适合 **读多写极少**。写加锁，读无锁。写代价高，且迭代看的是旧快照。

---

## 三、并发编程口述

### 3.1 线程创建与状态

**口述：**  
创建：继承 Thread、实现 Runnable、实现 Callable + FutureTask；**生产用线程池**。  
状态：NEW → RUNNABLE（含就绪与运行）→ BLOCKED（等 monitor）/ WAITING / TIMED_WAITING → TERMINATED。  
注意 RUNNABLE 在 JVM 层面不区分是否在 CPU 上跑。

### 3.2 sleep vs wait vs yield vs join

| 方法 | 所属 | 释放锁 | 说明 |
|------|------|--------|------|
| sleep | Thread | 否 | 定时让出 CPU |
| wait | Object | 是 | 需在同步块，配合 notify |
| yield | Thread | 否 | 提示让出，不保证 |
| join | Thread | - | 等另一线程结束 |

### 3.3 synchronized 原理

**口述：**  
可修饰方法或代码块，锁对象分别是 this/Class 或指定对象。  
JVM 基于对象头 Mark Word 与 monitor：偏向锁、轻量级锁、重量级锁等（具体默认策略随 JDK 变化，JDK15+ 偏向锁默认关闭，面试可提「锁升级/锁膨胀」思想）。  
保证原子性、可见性（解锁前写回）、有序性（happens-before）。可重入。  
块比方法更灵活，锁粒度更小更好。

### 3.4 ReentrantLock vs synchronized

**口述：**  
都能可重入互斥。ReentrantLock 是 API 锁：可公平、可 tryLock、可中断、多 Condition。  
必须在 finally unlock，防泄漏。  
一般 synchronized 够用更简洁；需要高级特性再用 Lock。

### 3.5 volatile

**口述：**  
保证 **可见性**（写立刻对其他线程可见）和 **有序性**（禁止部分重排，插内存屏障）。  
**不保证复合操作原子性**，`i++` 仍要原子类或锁。  
典型：状态开关、DCL 单例的 instance 字段。

### 3.6 CAS 与 ABA

**口述：**  
CAS：Compare And Swap，用期望值比较内存值，相同才更新，失败则重试。AtomicInteger 底层靠它。  
优点：无锁乐观并发。  
问题：ABA（值被 A→B→A，CAS 以为没变）—— 用 AtomicStampedReference 版本号；自旋激烈耗 CPU —— 用 LongAdder 等分段。

### 3.7 JMM 与 happens-before（简答）

**口述：**  
JMM 定义线程工作内存与主内存交互，解决可见性、有序性、原子性抽象。  
happens-before：若 A hb B，则 A 的结果对 B 可见。常见：解锁 hb 加锁、volatile 写 hb 读、线程 start/join、传递性等。  
synchronized/volatile/final 等语义都建立在这套规则上。

### 3.8 AQS 原理

**口述：**  
AbstractQueuedSynchronizer 是很多同步器的基石。核心：  
1. 用 **volatile int state** 表示资源；  
2. 通过 CAS 改 state；  
3. 失败则进入 **CLH 变体双向队列** 排队；  
4. 支持独占（ReentrantLock）与共享（Semaphore、CountDownLatch）。  
子类实现 tryAcquire/tryRelease 等模板方法。  
理解 AQS 就能串起锁、门闩、信号量的实现骨架。

### 3.9 线程池（必背长答）

**口述：**  
核心是 ThreadPoolExecutor，七大参数：  
corePoolSize、maximumPoolSize、keepAliveTime、单位、workQueue、threadFactory、handler。

**提交流程：**  
1. 当前线程数 < core → 建核心线程执行；  
2. 否则入队；  
3. 队列满且 < max → 建非核心线程；  
4. 还满 → 拒绝策略。

**队列：** 有界 ArrayBlockingQueue、无界 LinkedBlockingQueue（易 OOM）、SynchronousQueue（Cached 风格）等。

**拒绝策略：** Abort 抛异常、CallerRuns 调用者跑、Discard、DiscardOldest。

**为什么不用 Executors 默认：** newFixed 默认无界队列可能堆积任务 OOM；newCached 最大线程很大可能创建过多线程。生产 **自建有界队列 + 合适拒绝策略 + 业务隔离池**。

**线程数：** CPU 密集 ≈ Ncpu+1；IO 密集可更大。结合压测。

### 3.10 ThreadLocal

**口述：**  
每个线程有 ThreadLocalMap，key 是 ThreadLocal 弱引用，value 是线程局部值。  
实现线程隔离，如用户上下文、SimpleDateFormat 旧写法。  
**泄漏：** 线程池线程复用，key 被回收后 value 仍挂着 —— **finally 里 remove**。

### 3.11 死锁

**口述：**  
互斥、占有且等待、不可抢占、循环等待。  
预防：固定加锁顺序、tryLock 超时、缩小锁范围。  
排查：`jstack` 看 deadlock 报告，或 Arthas `thread -b`。

### 3.12 单例与并发（DCL）

```text
volatile + 双重检查锁定：防止指令重排导致未初始化完成的对象被看到
枚举单例：简洁、防反射/序列化问题（Effective Java 推荐）
静态内部类：懒加载且类加载保证线程安全
```

### 3.13 CountDownLatch / CyclicBarrier / Semaphore

| 工具 | 一句话 |
|------|--------|
| CountDownLatch | 一次倒数，主线程等 N 个任务完 |
| CyclicBarrier | 多方互相等，可重置再开一局 |
| Semaphore | N 个许可，限流 |

### 3.14 CompletableFuture（简答）

**口述：**  
异步编排：supplyAsync、thenApply、thenCombine、exceptionally 等，替代回调地狱。注意默认 ForkJoinPool 与自定义 Executor，避免阻塞公共池。

---

## 四、Spring 口述

### 4.1 IoC / DI

**口述：**  
IoC 控制反转：对象创建和依赖关系交给容器，而不是自己 new。  
DI 依赖注入：构造器、setter、字段注入把依赖塞进来。  
好处：解耦、易测、统一生命周期管理。

### 4.2 AOP

**口述：**  
面向切面：把日志、事务、鉴权等横切逻辑从业务中剥离。  
运行时用 **动态代理**：有接口走 JDK 代理，无接口走 CGLIB 子类。  
Spring 事务、`@Async` 等都建立在 AOP 上。同类内部自调用不走代理，切面失效。

### 4.3 Bean 生命周期（常考）

**口述顺序：**  
1. 实例化  
2. 属性填充（依赖注入）  
3. Aware 回调（BeanName、BeanFactory…）  
4. BeanPostProcessor 前置  
5. 初始化：`@PostConstruct` → InitializingBean → 自定义 init-method  
6. BeanPostProcessor 后置（AOP 代理常在这里）  
7. 使用  
8. 销毁：`@PreDestroy` → DisposableBean → destroy-method  

单例在容器启动阶段创建（默认），原型每次 get 新建。

### 4.4 三级缓存与循环依赖（必背长答）

**口述：**  
Spring 单例用三级缓存解决 **字段/setter 循环依赖**：  
- 一级：成品 Bean  
- 二级：早期暴露的半成品（引用）  
- 三级：ObjectFactory，用于生成早期引用（涉及代理）  

流程概要：A 创建到半成品放入三级 → 注入 B → 创建 B 需要 A → 从三级/二级拿到 A 的早期引用 → B 完成 → A 完成注入 → 升入一级。  

**构造器循环依赖解决不了**（创建时就要对方完整实例）。  
prototype 循环依赖也不支持。

### 4.5 JDK 动态代理 vs CGLIB

| | JDK | CGLIB |
|--|-----|-------|
| 条件 | 目标实现接口 | 继承目标类 |
| 方式 | 调用处理器 | 写子类拦截 |
| 限制 | 只能代理接口方法 | final 类/方法不行 |

Spring Boot 2.x 起默认常偏向 CGLIB（可配置）。

### 4.6 @Transactional 原理与失效（必背）

**原理口述：**  
AOP 代理在方法前后加事务增强：按传播行为决定开新事务或加入；提交或回滚；底层对接 PlatformTransactionManager（如 DataSourceTransactionManager）。

**失效场景：**  
1. 方法不是 public  
2. **同类内部调用**未走代理  
3. 异常被 catch 吞掉  
4. 抛出受检异常未设 `rollbackFor`  
5. 数据库引擎无事务  
6. 传播行为 `NOT_SUPPORTED` 等配置问题  
7. 多线程：子线程无事务上下文  

**传播行为常考：** REQUIRED（默认）、REQUIRES_NEW、NESTED 等。  
**隔离级别：** 对应 DB 隔离，默认一般用数据库默认。

### 4.7 Spring MVC 一次请求

**口述：**  
请求 → DispatcherServlet → HandlerMapping 找 Handler → HandlerAdapter 执行（Controller）→ 返回 ModelAndView 或 `@ResponseBody` 消息转换 → 视图渲染或写 JSON → 返回响应。  
拦截器 pre/post/after；异常解析器处理异常。

### 4.8 Spring Boot 自动配置

**口述：**  
`@SpringBootApplication` 含组件扫描 + `@EnableAutoConfiguration`。  
通过 `spring.factories` 或 2.7+/3.x 的 `AutoConfiguration.imports` 加载自动配置类；  
`@ConditionalOnClass/Property/Bean` 等条件满足才生效；  
starter 聚合依赖 + 自动配置，做到约定优于配置。

### 4.9 @Autowired vs @Resource

**口述：**  
Autowired 是 Spring 的，默认 byType，可配合 `@Qualifier`；required 默认 true。  
Resource 是 JSR-250，默认 byName。  
构造器注入更推荐（不可变、易测）。

### 4.10 Filter / Interceptor / AOP

| | Filter | Interceptor | AOP |
|--|--------|-------------|-----|
| 规范 | Servlet | Spring MVC | Spring |
| 范围 | 请求进入容器 | Controller 前后 | Bean 方法 |
| 顺序 | 更靠前 | 中间 | 方法级横切 |

---

## 五、MySQL 口述

### 5.1 InnoDB vs MyISAM

**口述：**  
InnoDB 支持事务、行锁、外键、崩溃恢复、MVCC，聚簇索引；现在默认。  
MyISAM 表锁、不支持事务，曾适合只读，基本被替代。

### 5.2 事务 ACID 与隔离级别

**口述：**  
原子性、一致性、隔离性、持久性。  
隔离级别：读未提交、读已提交、可重复读、串行化。  
问题：脏读、不可重复读、幻读。  
MySQL InnoDB **默认可重复读（RR）**，并通过 MVCC + 间隙锁等尽量处理幻读。

### 5.3 MVCC（简答加分）

**口述：**  
多版本并发控制：每行隐藏事务号/回滚指针，undo 构成版本链。  
普通 SELECT 生成 ReadView，判断版本是否可见，实现非阻塞读。  
与当前读（加锁读）不同。

### 5.4 索引与 B+ 树

**口述：**  
InnoDB 用 B+ 树：叶子存数据或主键（聚簇），非叶子存键值与指针，叶子链表有序利于范围查。  
相对 B 树：数据都在叶子、层高更低、范围友好。  
二级索引叶子是主键，需 **回表**；覆盖索引可避免回表。

**最左前缀：** 联合索引 (a,b,c) 用 a、ab、abc 才高效，跳过 a 只 b 一般用不上索引。

### 5.5 索引失效常见情况

**口述：**  
对索引列做函数/运算、隐式类型转换、`LIKE '%x'`、违反最左、or 一侧无索引、优化器判断全表更便宜等。用 explain 验证。

### 5.6 explain 关键字段

**口述：**  
type（system/const/eq_ref/ref/range/index/ALL…越左越好）、  
key（实际索引）、rows、Extra（Using filesort/temporary/Using index 覆盖等）。

### 5.7 锁

**口述：**  
InnoDB 行锁基于索引。  
共享/排他；意向锁；RR 下范围条件可能间隙锁、临键锁防幻读。  
死锁：事务互相等，InnoDB 回滚代价小的一方。业务上缩短事务、固定顺序访问。

### 5.8 redo / undo / binlog

| 日志 | 作用 |
|------|------|
| redo | 崩溃恢复，保证持久性 |
| undo | 回滚、MVCC 版本 |
| binlog | 主从复制、归档（Server 层） |

两阶段提交保证 redo 与 binlog 一致（面试提「内部 XA/2PC 思想」即可）。

### 5.9 慢 SQL 优化思路

**口述：**  
慢查询日志定位 → explain → 加合适索引/改写 SQL → 避免 select * → 分页优化（延迟关联）→ 拆大事务 → 冷热数据、缓存。  
不能只加索引，要看选择性与写入代价。

### 5.10 深分页

**口述：**  
`LIMIT 1000000,10` 扫描大量行。优化：记住上次最大 id 用 `WHERE id > ? LIMIT 10`，或延迟关联先查主键再 join。

---

## 六、Redis 口述

### 6.1 为什么快

**口述：**  
1. 内存操作；  
2. 高效数据结构；  
3. 单线程执行命令避免上下文切换与锁（IO 多线程是后续版本读 socket 优化，命令执行仍偏单线程模型）；  
4. IO 多路复用。

### 6.2 五大数据类型与场景

| 类型 | 场景 |
|------|------|
| String | 缓存、计数、分布式锁、Session |
| Hash | 对象字段存储 |
| List | 队列、最新列表 |
| Set | 去重、共同关注 |
| ZSet | 排行榜（跳表+字典） |

扩展：Bitmap 签到、HyperLogLog 基数、Stream 消息。

### 6.3 持久化 RDB vs AOF

**口述：**  
RDB 快照，恢复快、文件小，可能丢最后一次快照后数据。  
AOF 记写命令，数据更全，文件大，有重写。  
可混合持久化。按业务容忍度选，生产常开。

### 6.4 过期与淘汰

**口述：**  
过期：惰性删除 + 定期抽样删除。  
内存满：按 maxmemory-policy，如 allkeys-lru、volatile-lru、lfu 等。

### 6.5 缓存穿透 / 击穿 / 雪崩（必背）

| 问题 | 定义 | 方案 |
|------|------|------|
| 穿透 | 查不存在的数据，打到 DB | 布隆过滤、缓存空值 |
| 击穿 | 热点 key 过期瞬间 | 互斥锁重建、逻辑过期、永不过期+异步更 |
| 雪崩 | 大量 key 同时过期或 Redis 挂 | 过期时间打散、集群高可用、限流降级、多级缓存 |

### 6.6 分布式锁

**口述：**  
`SET key value NX EX seconds` 保证原子加锁+过期。  
value 用唯一 ID，释放用 Lua 校验身份防误删。  
问题：业务超时锁过期 —— Redisson 看门狗续期；主从切换锁丢失 —— 可讨论 RedLock（有争议）或可接受风险 + fencing token。  
生产常用 Redisson。

### 6.7 缓存与 DB 一致性

**口述：**  
强一致难且贵，一般最终一致。  
常见：先更新 DB，再删缓存；失败重试或消息队列补偿；延迟双删防并发读旧；订阅 binlog 异步删缓存（Canal 等）。  
读多写少用缓存，不能假设双写绝对一致。

### 6.8 主从 / 哨兵 / Cluster

**口述：**  
主从复制扩展读、持久化备份。  
哨兵负责监控与故障转移选主。  
Cluster 分槽 16384，水平扩展；注意跨 slot 与数据倾斜、大 key。

### 6.9 大 key / 热 key

**口述：**  
大 key：拆分、压缩、避免大 value 阻塞。  
热 key：本地缓存、副本打散、读写分离、限流。

### 6.10 Pipeline / 事务 / Lua

**口述：**  
Pipeline 批量减少 RTT，非原子。  
事务 MULTI/EXEC 不回滚单条失败（与关系库事务不同）。  
Lua 脚本原子执行，适合锁释放、库存扣减等。

---

## 七、MQ 与分布式口述简答

### 7.1 为什么用 MQ

**口述：**  
解耦、异步提速、削峰填谷。代价：一致性变复杂、延迟、运维成本、排查链路变长。

### 7.2 可靠性与幂等

**口述：**  
生产端：确认机制、失败重试。  
Broker：持久化、副本。  
消费端：手动 ack，业务幂等（唯一键、状态机）。  
至少一次投递下必须幂等；恰好一次很难，常用至少一次 + 幂等。

### 7.3 消息积压

**口述：**  
消费者扩容、优化消费逻辑、临时增加分区/队列、非关键可丢弃或旁路存储后处理。根因常是消费慢或下游故障。

### 7.4 顺序消息

**口述：**  
同一业务键发到同一分区/队列，单线程消费；吞吐与顺序权衡。

### 7.5 分布式事务（简答）

**口述：**  
强一致 2PC 性能差；业务多用最终一致：本地消息表、事务消息、TCC、Saga、Seata AT 等。按一致性要求与复杂度选型。

### 7.6 限流

**口述：**  
计数器、滑动窗口、漏桶、令牌桶（Guava/RateLimiter、Sentinel、网关层）。保护自身与下游。

---

## 八、考前速记总表

### 8.1 一句话命中

| 考点 | 一句话 |
|------|--------|
| HashMap | 数组+链+红黑树，0.75，2 倍扩容，非线程安全 |
| CHM | CAS+同步桶头，无 null，JDK8 无 Segment |
| volatile | 可见+有序，不保证 i++ 原子 |
| CAS | 乐观比较交换，防 ABA 用版本号 |
| AQS | state+队列，锁和同步器基石 |
| 线程池 | 先核心再排队再最大再拒绝；自建有界 |
| ThreadLocal | 线程隔离，finally remove |
| 三级缓存 | 解字段循环依赖，解不了构造器循环 |
| 事务失效 | 非 public、自调用、吞异常、无 rollbackFor |
| B+ 索引 | 最左前缀、少回表、explain |
| MVCC | 版本链+ReadView 非阻塞读 |
| 穿透击穿雪崩 | 空值/布隆、互斥/逻辑过期、打散/高可用 |
| 分布式锁 | SET NX EX + 唯一 value + Lua 删 |
| MQ | 解耦异步削峰 + 可靠 + 幂等 |

### 8.2 建议背诵优先级（时间紧）

```text
P0：HashMap、线程池、volatile、CHM、事务失效、索引、缓存三连、分布式锁
P1：AQS 轮廓、循环依赖三级缓存、MVCC、Bean 生命周期、死锁排查
P2：Boot 自动配置、redo/undo/binlog、Cluster、MQ 积压
```

### 8.3 与 JVM 场景题配合

线上排查口述见：  
[JVM高频面试题与知识点.md](./JVM高频面试题与知识点.md) **第十一章 TOP15**。

---

## 九、分模块自测清单（勾选）

### 基础

- [ ] equals/hashCode  
- [ ] String 不可变  
- [ ] 值传递  
- [ ] 异常与 try-with-resources  

### 集合

- [ ] ArrayList 扩容  
- [ ] HashMap put/扩容/树化  
- [ ] ConcurrentHashMap  
- [ ] LRU  

### 并发

- [ ] synchronized / Lock  
- [ ] volatile / CAS  
- [ ] 线程池七参数  
- [ ] ThreadLocal  
- [ ] AQS 一分钟版  
- [ ] 死锁  

### Spring

- [ ] IoC/AOP  
- [ ] Bean 生命周期  
- [ ] 三级缓存  
- [ ] 事务失效  
- [ ] MVC 流程  
- [ ] Boot 自动配置  

### MySQL

- [ ] 隔离级别 + MVCC  
- [ ] B+ 与最左前缀  
- [ ] 索引失效  
- [ ] 慢 SQL  

### Redis

- [ ] 为什么快 + 五类型  
- [ ] 穿透击穿雪崩  
- [ ] 分布式锁  
- [ ] 一致性  

### MQ

- [ ] 为何用 / 可靠 / 幂等 / 积压  

---

## 十、文档修订记录

| 日期 | 说明 |
|------|------|
| 2026-07-20 | 初版全集：基础、集合、并发、Spring、MySQL、Redis、MQ 口述参考答案 + 速记总表 |
| 2026-07-20 | 关联《追问与手写题》文档 |
