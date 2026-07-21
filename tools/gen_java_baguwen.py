# -*- coding: utf-8 -*-
"""
按大厂 Java 高频八股大纲分模块补全知识点（笔记体：题 + 要点）。
不碰面渣。
"""
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def w(name, text):
    p = DOCS / name
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print("W", name, p.stat().st_size)


def nav(oral, card, path="路径-Java后端.md"):
    return f"""<!-- NAV:START -->
> 📖 **八股知识点** · 🗣️ [面渣](./{oral}) · 🃏 [卡片](./{card})
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md) · [Java路径](./{path}) · [模块总览](./Java八股模块总览.md)
>
<!-- NAV:END -->
"""


# =============================================================================
JAVA = f"""# Java 基础 + 集合 · 高频八股知识点

{nav('Java面渣级口述.md', 'Java卡片速记.md')}

> 覆盖 P5–P7 基础与集合主考点。风格：**题目 + 核心要点**。完整口语 → 面渣。

---

# 一、Java 基础（必考）

## 1. == 与 equals 的区别？

| | == | equals |
|--|-----|--------|
| 基本类型 | 比较**值** | — |
| 引用类型 | 比较**内存地址** | 默认（Object）也比地址；重写后可比**内容**（String/Integer） |

---

## 2. 为什么重写 equals 必须重写 hashCode？（必考）

- **约定**：equals 为 true ⇒ hashCode **必须**相同。
- **原因**：HashMap/HashSet 先 hash 定位桶，再 equals 比 key。
- **后果**：hash 不同 → 进不同桶 → **存进去取不出**。
- hash 相同 **不** ⇒ equals 一定 true（允许碰撞）。

---

## 3. String / StringBuilder / StringBuffer？

| | 可变 | 线程安全 | 场景 |
|--|------|----------|------|
| String | 否 | 是（不可变） | 常量、少量拼接 |
| StringBuilder | 是 | 否 | 单线程拼接（首选） |
| StringBuffer | 是 | 是（synchronized） | 历史多线程拼接，现代少用 |

---

## 4. String 为什么不可变？

- 类 final；底层 `char[]`（JDK9+ 多为 `byte[]` + coder）；无对外修改内容的 API。
- **好处**
  - 常量池共享安全。
  - hashCode 可缓存（适合做 HashMap key）。
  - 天然线程安全、防篡改（类名、路径、密钥参数等）。

---

## 5. final / finally / finalize？

- **final**：类不可继承；方法不可重写；变量不可重新赋值（引用 final ≠ 对象内容不可变）。
- **finally**：try 后通常必执行（释放资源）；`System.exit` 等极端情况除外。
- **finalize**：GC 前调用，**已不推荐/废弃**，别依赖。

---

## 6. 面向对象三大特性？（+ 抽象）

- **封装**：隐藏细节，暴露接口。
- **继承**：复用、is-a。
- **多态**：同一引用不同实现（编译看父，运行看子——虚方法）。
- 常把 **抽象** 并列为第四特性。

---

## 7. 重载 vs 重写？

| | 重载 overload | 重写 override |
|--|---------------|---------------|
| 范围 | 同类（或继承可见） | 子类覆盖父类 |
| 规则 | 同名，**参数列表不同** | 方法签名相同（返回值协变等规则） |
| 绑定 | **编译期** | **运行时**多态 |

---

## 8. 抽象类 vs 接口？

| | 抽象类 | 接口 |
|--|--------|------|
| 构造 | 可有 | 无实例构造（不能 new 接口） |
| 成员变量 | 可有普通成员 | 多为常量（public static final） |
| 方法 | 可抽象可实现 | JDK8+：default / static / private 方法 |
| 多继承 | 单继承类 | 可实现多接口 |
| 设计 | is-a 模板 | can-do 能力 |

---

## 9. Integer 缓存？装箱拆箱？

- **装箱**：基本 → 包装（`Integer.valueOf`）。
- **拆箱**：包装 → 基本（`intValue`）。
- **缓存**：默认 **-128～127**；区间内 `==` 可能 true；区间外 false。
- 比内容用 `equals`；`new Integer(100)` 不走缓存。

---

## 10. 异常体系？

```text
Throwable
├── Error          （严重，一般不捕获：OOM、StackOverflow）
└── Exception
    ├── RuntimeException 及子类  → 非检查异常（可不声明）
    └── 其他 Exception           → 检查异常（需处理或声明）
```

- 检查异常：编译期强制处理（IOException 等）。
- 运行时异常：NPE、IllegalArgument 等。

---

## 11. Java 是值传递还是引用传递？

- **只有值传递**。
- 传引用类型时：传递的是**引用的副本**（地址值的拷贝）。
- 方法内改「副本指向」不影响外部引用；通过副本调用方法改对象内部状态，外部可见。

---

## 12. 常见补充（加分）

- **== 与 equals 对包装类**：缓存区间内外表现不同。
- **String intern**：尝试返回池中引用。
- **深拷贝 / 浅拷贝**：浅拷贝共享内部引用；深拷贝递归复制。

---

# 二、集合框架（超级高频）

## 13. HashMap 底层？（必考，分版本）

### JDK 1.7

- 数组 + 链表。
- 头插法；多线程扩容可能**死循环**（历史考点）。

### JDK 1.8+

- 数组 + 链表 + **红黑树**。
- **尾插**；树化条件：链长 **≥8** 且数组长度 **≥64**；树节点过少（≤6）退化链表。
- 默认容量 **16**，负载因子 **0.75**，扩容 **2 倍**。
- hash 扰动：高低位异或，减少碰撞。
- 容量 **2 的幂**：`(n-1) & hash` 代替取模。

### put 要点

1. hash → 下标  
2. 空桶直接放 / 相等覆盖 / 链或树插入  
3. 可能树化、扩容  

### get 要点

hash → 下标 → 链/树用 equals 找 key。

### 线程安全

- HashMap **否**。
- 并发用 ConcurrentHashMap。

---

## 14. ArrayList vs LinkedList？

| | ArrayList | LinkedList |
|--|-----------|------------|
| 结构 | 动态数组 | 双向链表 |
| 随机访问 | O(1) | O(n) |
| 头尾插删 | 尾部均摊 O(1)；中间要搬移 | 头尾 O(1) |
| 实践 | **默认首选** | 特定链表算法场景 |

---

## 15. HashMap vs Hashtable vs ConcurrentHashMap？

| | 线程安全 | 锁粒度 | null |
|--|----------|--------|------|
| HashMap | 否 | — | key/value 可 null（一个 null key） |
| Hashtable | 是 | 基本全表 synchronized | 不允许 null |
| ConcurrentHashMap | 是 | JDK7 分段锁；**JDK8 CAS + synchronized 锁桶头节点** | 不允许 null |

### ConcurrentHashMap 为何相对高效？

- 不锁整表；JDK8 按节点/桶同步 + CAS 初始化。
- 读多写少场景吞吐通常优于 Hashtable。

---

## 16. HashSet / TreeMap？

- **HashSet**：底层 HashMap，value 为固定 PRESENT 对象；靠 key 去重。
- **TreeMap**：红黑树，**有序**（Comparable / Comparator）；操作 O(log n)。

---

## 17. fail-fast / fail-safe？

- fail-fast：迭代时结构被改可能 CME（ArrayList 等）。
- 并发容器迭代多为弱一致，不保证强 fail-fast。

---

## 18. 集合选用速记

| 需求 | 选择 |
|------|------|
| 列表随机访问 | ArrayList |
| KV 缓存（单线程） | HashMap |
| KV 并发 | ConcurrentHashMap |
| 去重无序 | HashSet |
| 有序 KV | TreeMap / LinkedHashMap |

---

# 自测清单

- [ ] equals/hashCode + Integer 缓存  
- [ ] String 三兄弟 + 不可变原因  
- [ ] 值传递一句话  
- [ ] HashMap 7/8 差异 + 树化 + 2 的幂  
- [ ] CHM 与 Hashtable 区别  

**口述：** [Java面渣级口述.md](./Java面渣级口述.md) · **卡片：** [Java卡片速记.md](./Java卡片速记.md)  
**下一模块：** [并发](./并发高频面试题与知识点.md)
"""

# =============================================================================
CONC = f"""# 多线程与并发 · 高频八股知识点

{nav('并发面渣级口述.md', '并发卡片速记.md')}

> 大厂必深挖：原理 + 对比 + 场景。口语 → [面渣](./并发面渣级口述.md)。

---

## 1. 创建线程的方式？

1. 继承 `Thread`  
2. 实现 `Runnable`  
3. 实现 `Callable` + `FutureTask`（可返回值/异常）  
4. **线程池**（生产推荐）  

---

## 2. 线程生命周期？

```text
New → Runnable ↔ Running → Blocked / Waiting / Timed Waiting → Terminated
```

- Blocked：等 synchronized 锁。  
- Waiting：`wait`/`join`/`LockSupport.park` 等。  
- Timed Waiting：带超时的等待。  

---

## 3. synchronized 原理？

- 监视器锁；可修饰方法/代码块；**可重入**。
- 对象头 **Mark Word** 记录锁状态。
- 锁升级（HotSpot）：**偏向锁 → 轻量级锁 → 重量级锁**（竞争加剧时膨胀；细节版本有演进）。
- 保证：**原子性 + 可见性**（解锁 happens-before 后续加锁）。

---

## 4. volatile？

- **可见性**：写对其他线程尽快可见。  
- **有序性**：禁止部分指令重排序（内存屏障）。  
- **不保证原子性**（`i++` 仍要锁或 Atomic）。  
- 场景：开关标志、双检锁中的安全发布（配合正确写法）。

---

## 5. CAS？ABA？Atomic？

- **CAS**：Compare-And-Swap，无锁更新；失败重试（自旋）。
- **ABA**：A→B→A 被误判未变 → 版本戳 / `AtomicStampedReference`。
- `AtomicInteger` 等基于 CAS；高竞争计数可考虑 `LongAdder`。

---

## 6. AQS 原理？（高频）

- `AbstractQueuedSynchronizer`：同步器框架。
- 核心：`state` + **CLH 变体等待队列**。
- 模式：独占（ReentrantLock）/ 共享（Semaphore、CountDownLatch）。
- 子类实现 tryAcquire / tryRelease 等，队列阻塞唤醒复用。

---

## 7. ReentrantLock vs synchronized？

| | synchronized | ReentrantLock |
|--|--------------|---------------|
| 实现 | JVM | API（AQS） |
| 可中断/超时 | 弱 | 支持 |
| 公平 | 非公平 | 可公平/非公平 |
| 条件队列 | 单个 wait/notify | 多个 Condition |
| 释放 | 自动 | 必须 unlock（finally） |

---

## 8. 死锁？

- **四条件**：互斥、占有且等待、不可抢占、循环等待。
- **避免**：固定加锁顺序、超时锁、减小锁粒度、避免嵌套锁。
- **排查**：`jstack` 看死锁报告；DB 侧 InnoDB 会检测回滚一方。

---

## 9. ThreadLocal？

- 每线程一份副本（`ThreadLocalMap` 挂在 Thread 上）。
- **泄漏**：线程池线程复用 + 不 `remove` → 脏数据/对象难回收。
- **规范**：`try/finally remove`。

---

## 10. 线程池七大参数 + 拒绝策略？（必考）

| 参数 | 含义 |
|------|------|
| corePoolSize | 核心线程数 |
| maximumPoolSize | 最大线程数 |
| keepAliveTime + unit | 非核心空闲存活 |
| workQueue | 任务队列 |
| threadFactory | 线程工厂 |
| handler | 拒绝策略 |

**提交流程**：<core 建线程 → 入队 → <max 建非核心 → 拒绝。

**四种拒绝策略**

1. AbortPolicy：抛异常（默认）  
2. CallerRunsPolicy：调用者线程执行  
3. DiscardPolicy：丢弃  
4. DiscardOldestPolicy：丢最老再试  

**Executors 坑**：`Fixed/Single` 默认无界队列易 OOM；`Cached` 最大线程过大。**推荐 `ThreadPoolExecutor` 手动创建**。

---

## 11. JUC 三件套？

| 工具 | 作用 |
|------|------|
| CountDownLatch | 一或多个线程等一组事件结束（倒数） |
| CyclicBarrier | 一组线程互相等，到齐再走（可循环） |
| Semaphore | 限流/许可证 |

---

## 12. ConcurrentHashMap / CopyOnWriteArrayList？

- **CHM**：见集合篇；JDK8 CAS + synchronized 节点。
- **COW ArrayList**：写时复制；读多写少；迭代弱一致。写贵。

---

## 13. Java 21 虚拟线程（加分）

- **平台线程**：1:1 操作系统线程，重。
- **虚拟线程**：JVM 调度的轻量线程，适合**大量阻塞 IO** 并发。
- 不适合：长时间占 CPU 的重计算（仍要控制并行度）。
- 与线程池模型：可为每任务一个虚拟线程（场景依赖）。

---

# 自测

- [ ] volatile 三性边界  
- [ ] 线程池参数 + 拒绝 + Executors 坑  
- [ ] AQS 一句话  
- [ ] ThreadLocal 泄漏  
- [ ] 虚拟线程适用场景  

**口述：** [并发面渣级口述.md](./并发面渣级口述.md) · **卡片：** [并发卡片速记.md](./并发卡片速记.md)  
**相关：** [JVM](./JVM高频面试题与知识点.md) · [Java集合](./Java高频面试题与知识点.md)
"""

# =============================================================================
JVM = f"""# JVM · 高频八股知识点

{nav('JVM面渣级口述.md', 'JVM卡片速记.md')}

> 阿里、美团等高频：内存 + GC + 类加载 + 排查。口语 → [面渣](./JVM面渣级口述.md)。

---

## 1. 运行时数据区？

| 区域 | 私有/共享 | 作用 |
|------|-----------|------|
| 程序计数器 | 私有 | 当前字节码行号 |
| 虚拟机栈 | 私有 | 栈帧：局部变量、操作数栈等 |
| 本地方法栈 | 私有 | native |
| 堆 | 共享 | 对象实例，GC 主战场 |
| 方法区/元空间 | 共享 | 类元数据等（JDK8+ 元空间用本地内存） |
| 直接内存 | 堆外 | NIO 等，受本机/容器限制 |

### 堆分代

- **新生代**：Eden + Survivor0 + Survivor1（复制算法常见）。  
- **老年代**：长期存活对象。  

---

## 2. 如何判断对象存活？

- **引用计数**：循环引用问题；Java 不用作主方案。  
- **可达性分析**：从 GC Roots 不可达 → 可回收。  
- Roots：栈引用、静态变量、常量、JNI、锁对象等。

---

## 3. 垃圾回收算法？

| 算法 | 特点 | 典型 |
|------|------|------|
| 标记-清除 | 碎片 | 老年代历史 |
| 复制 | 活对象少时高效 | 新生代 |
| 标记-整理 | 无碎片、移动成本 | 老年代 |
| 分代收集 | 不同代不同策略 | 现代基础 |

---

## 4. 常见垃圾收集器？

| 收集器 | 特点 |
|--------|------|
| Serial | 单线程，简单 |
| ParNew | 新生代并行 |
| CMS | 并发标记清除，低停顿（碎片、浮动垃圾） |
| **G1** | Region、可预测停顿、JDK9+ 常见默认 |
| **ZGC** | 超低延迟（大堆场景加分） |

### G1 特点（常考）

- 堆拆 **Region**（可跨代逻辑）。  
- **Remembered Set** 等维护跨 Region 引用。  
- 优先回收收益高的 Region；可设停顿目标。  
- 过程直觉：初始标记 → 并发标记 → 最终标记 → 筛选回收（可记主干）。

---

## 5. Minor GC / Full GC？

- Minor：主要收新生代，较频繁。  
- Full：老年代或整堆等大范围回收，停顿通常更长；要少触发。  
- 频繁 Full：分配过快、泄漏、晋升失败、元空间等要分情况。

---

## 6. 类加载过程？双亲委派？

```text
加载 → 验证 → 准备 → 解析 → 初始化
```

- **双亲委派**：先委派父加载器，父没有再自己加载。  
- **目的**：核心类唯一、安全（防自定义 `java.lang.String`）。  

### 破坏双亲委派场景

- **SPI**（JDBC 驱动等）  
- **Tomcat** 等 Web 容器隔离  
- **OSGi** 模块热插拔  
- 自定义 ClassLoader 打破委派  

---

## 7. 常见 OOM 与排查？

| 类型 | 方向 |
|------|------|
| 堆 OOM | dump + MAT 看占用与引用链 |
| 元空间 OOM | 类太多/泄漏，查动态生成类 |
| 栈溢出 | 递归过深 StackOverflowError |
| 直接内存 | NIO/堆外，容器 limit |

### 工具

- `jmap` / `jstack` / `jstat`  
- **MAT** 分析 dump  
- **Arthas** 在线诊断（加分）  

### 排查顺序（口述）

```text
现象时间线 → GC/CPU/内存指标 → jstack/jmap → 根因 → 止血+根治
```

---

# 自测

- [ ] 五区 + 堆分代  
- [ ] 可达性 vs 引用计数  
- [ ] G1 三个关键词  
- [ ] 双亲委派 + 破坏场景  
- [ ] OOM 工具链  

**口述：** [JVM面渣级口述.md](./JVM面渣级口述.md) · **卡片：** [JVM卡片速记.md](./JVM卡片速记.md)
"""

# =============================================================================
SPRING = f"""# Spring / Spring Boot · 高频八股知识点

{nav('Spring面渣级口述.md', 'Spring卡片速记.md')}

> 中小厂高频，大厂也问原理。口语 → [面渣](./Spring面渣级口述.md)。

---

## 1. IoC / DI？BeanFactory vs ApplicationContext？

- **IoC**：控制反转，创建装配交给容器。  
- **DI**：依赖注入（构造器推荐 / setter / 字段）。  
- **BeanFactory**：容器基础接口，偏懒加载。  
- **ApplicationContext**：更完整（事件、国际、AOP 等），企业开发常用。

---

## 2. Bean 生命周期？（要能串）

主干（口述顺序）：

1. 实例化  
2. 属性填充（依赖注入）  
3. Aware 回调（BeanName/BeanFactory/ApplicationContext…）  
4. BeanPostProcessor **前置**  
5. InitializingBean / `@PostConstruct` / init-method  
6. BeanPostProcessor **后置**（AOP 代理常在此阶段完成）  
7. 使用中  
8. `@PreDestroy` / DisposableBean / destroy-method  

---

## 3. AOP 原理？JDK 动态代理 vs CGLIB？

- 横切：事务、日志、鉴权。  
- **JDK 动态代理**：基于接口。  
- **CGLIB**：基于子类（无接口时）。  
- Spring Boot 2.x 起常默认偏向 CGLIB（可配置）。  
- **自调用**不走代理 → 事务/AOP 失效。

---

## 4. 事务传播行为？失效场景？

### 常用传播

| 传播 | 含义 |
|------|------|
| REQUIRED（默认） | 有事务加入，无则新建 |
| REQUIRES_NEW | 挂起当前，新建事务 |
| NESTED | 嵌套（保存点） |
| SUPPORTS / NOT_SUPPORTED / MANDATORY / NEVER | 了解 |

### 失效常见原因

- 同类内部调用（无代理）  
- 方法非 public  
- 异常被吞未抛出  
- 抛检查异常默认不回滚（需 `rollbackFor`）  
- 传播/只读配置理解错误  

---

## 5. Spring Boot 自动配置原理？

- `@SpringBootApplication` 含 `@EnableAutoConfiguration`。  
- 加载自动配置类：  
  - 旧：`META-INF/spring.factories`  
  - 新：`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`  
- **条件注解**（`@ConditionalOnClass` 等）决定是否生效。  
- starter 聚合依赖 + 自动配置。

---

## 6. @Autowired vs @Resource？

| | @Autowired | @Resource |
|--|------------|-----------|
| 来源 | Spring | JSR-250 |
| 默认 | 按类型 | 按名称 |
| 必填 | required 可调 | — |

---

## 7. 循环依赖？三级缓存？（高频）

- 单例 **字段/setter** 注入：三级缓存可解决。  
  - 提前暴露「早期引用」，打断环。  
- **构造器循环依赖**：创建都完不成，**通常无法解决**。  
- 原型 bean 循环依赖也不支持同样机制。  
- 面试：说清「为何能解 / 不能解」比背字段名更重要。

---

## 8. 过滤器 vs 拦截器？

- Filter：Servlet 规范，更靠前。  
- Interceptor：Spring MVC，可访问 Handler 信息。

---

# 自测

- [ ] Bean 生命周期主干  
- [ ] 事务失效 4 条  
- [ ] 自动配置加载位置  
- [ ] 循环依赖边界  

**口述：** [Spring面渣级口述.md](./Spring面渣级口述.md) · **卡片：** [Spring卡片速记.md](./Spring卡片速记.md)
"""

# =============================================================================
MYSQL = f"""# MySQL · 高频八股知识点

{nav('MySQL面渣级口述.md', 'MySQL卡片速记.md')}

---

## 1. 索引原理？为什么用 B+ 树？

- 索引降低扫描成本，避免全表扫。  
- **B+ 树**：矮胖、适合磁盘 IO；叶子链表利于**范围查询**；内部节点不存行数据（更利于分支）。  
- 哈希索引点查快，范围弱。

---

## 2. 聚簇索引 vs 二级（非聚簇）？

- **聚簇（主键）**：叶子 = **整行**。  
- **二级索引**：叶子 = **主键值** → 常 **回表**。  
- **覆盖索引**：二级索引已含查询列，免回表。  
- **索引下推（ICP）**：在存储引擎层用索引条件过滤，减少回表（了解加分）。

---

## 3. 最左前缀？

- 联合索引 `(a,b,c)`：从左连续使用 a / a,b / a,b,c。  
- 仅 b 或仅 c 通常用不好该索引。

---

## 4. 索引失效常见？

- 函数/运算包列、左模糊 `LIKE '%x'`、隐式类型转换、违背最左、选择性太差优化器弃用。  
- **以 EXPLAIN 为准**。

---

## 5. 事务 ACID？隔离级别？读问题？

- A 原子 / C 一致 / I 隔离 / D 持久。  
- 脏读 / 不可重复读 / 幻读。  
- 级别：RU → RC → **RR（InnoDB 默认）** → Serializable。  

---

## 6. MVCC 原理？

- **undo log** 版本链 + **ReadView**。  
- 快照读：普通 SELECT。  
- 当前读：`FOR UPDATE` / 更新删除等。  
- 提高读写并发。

---

## 7. 锁？

- 行锁依赖索引；无索引可能锁更多。  
- **间隙锁 / 临键锁**（RR 下）与防幻读相关。  
- 死锁：InnoDB 检测并回滚一方；`SHOW ENGINE INNODB STATUS` 等排查。

---

## 8. 慢查询与 EXPLAIN？

1. 慢日志定位  
2. EXPLAIN：`type`、`key`、`rows`、`Extra`（Using filesort/temporary 等）  
3. 加索引/改 SQL  
4. 验证  

深分页：`LIMIT 大偏移` → `id > last` / 延迟关联。

---

## 9. InnoDB vs MyISAM？

| | InnoDB | MyISAM |
|--|--------|--------|
| 事务 | 支持 | 否 |
| 行锁 | 支持 | 表锁为主 |
| 外键 | 支持 | 否 |
| 崩溃恢复 | 更好 | 较弱 |
| 现代默认 | **InnoDB** | 历史场景 |

---

## 10. redo / undo / binlog？

- redo：崩溃恢复（WAL）。  
- undo：回滚 + MVCC。  
- binlog：复制与恢复。  

---

# 自测

- [ ] B+ / 回表 / 覆盖 / 最左 / ICP  
- [ ] MVCC 一句话  
- [ ] EXPLAIN 关键字段  
- [ ] InnoDB vs MyISAM  

**口述：** [MySQL面渣级口述.md](./MySQL面渣级口述.md) · **卡片：** [MySQL卡片速记.md](./MySQL卡片速记.md)
"""

# =============================================================================
REDIS = f"""# Redis · 高频八股知识点

{nav('Redis面渣级口述.md', 'Redis卡片速记.md')}

---

## 1. 为什么快？

- 纯内存。  
- 命令执行**单线程**（无锁竞争）。  
- 高效编码/数据结构。  
- **IO 多路复用**。  
- Redis6+ 多线程主要加速网络 IO，别说成命令随意并行。

---

## 2. 五种类型 + 底层（加分）？

| 类型 | 场景 | 底层（了解） |
|------|------|----------------|
| String | 缓存、计数、锁 | SDS |
| Hash | 对象字段 | hashtable / listpack 等 |
| List | 列表/队列 | quicklist 等 |
| Set | 去重 | intset / hashtable |
| ZSet | 排行榜 | **skiplist** + dict 等 |

历史常考：ziplist/listpack 压缩、skiplist 为何适合 ZSet。

---

## 3. 持久化 RDB vs AOF vs 混合？

| | RDB | AOF |
|--|-----|-----|
| 内容 | 快照 | 写命令日志 |
| 恢复 | 快 | 可更完整 |
| 体积 | 相对小 | 可能大（可重写） |
| 丢数据 | 最近间隔 | 看 fsync 策略 |

- **混合持久化**：兼顾。  

---

## 4. 穿透 / 击穿 / 雪崩？（必考）

| 问题 | 定义 | 方案方向 |
|------|------|----------|
| 穿透 | 查不存在 | 空值缓存、布隆、校验 |
| 击穿 | 热点过期 | 互斥重建、逻辑过期 |
| 雪崩 | 大量同时过期或 Redis 挂 | TTL 抖动、HA、限流、多级缓存 |

---

## 5. 分布式锁？

- `SET key val NX EX`  
- 唯一 value + **Lua** 校验删除  
- 续期：Redisson **看门狗**  
- 主从极端丢锁风险要会说  

---

## 6. 过期删除 + 内存淘汰？

- **过期删除**：惰性删除 + 定期删除（不是定时全扫）。  
- **淘汰策略**（内存满）：noeviction、allkeys-lru、volatile-lru、lfu 等（会说 LRU/LFU 即可）。

---

## 7. Cache Aside？

- 读：缓存 → DB → 回填。  
- 写：**先 DB 再删缓存**。  

---

# 自测

- [ ] 三连不混  
- [ ] 锁四要素  
- [ ] RDB/AOF  
- [ ] 淘汰策略举例  

**口述：** [Redis面渣级口述.md](./Redis面渣级口述.md) · **卡片：** [Redis卡片速记.md](./Redis卡片速记.md)
"""

# =============================================================================
DP = f"""# 设计模式 · 高频八股知识点

{nav('设计模式面渣级口述.md', '设计模式卡片速记.md')}

---

## 1. 为什么要设计模式？

- 在**变化点**上解耦：创建、算法、增强、通知等。  
- 面试讲：**场景 + 结构 + 权衡**，不背 UML。

---

## 2. 单例（双重检查锁）

```text
volatile 实例
getInstance:
  if null:
    synchronized:
      if null: new
```

- volatile 防指令重排（发布安全）。  
- 枚举单例更简单安全（Effective Java）。  
- 注意：反射、序列化可破普通单例。

---

## 3. 工厂

- 封装创建，调用方依赖抽象。  
- 简单工厂 / 工厂方法 / 抽象工厂（说清差异即可）。

---

## 4. 代理

- 控制访问、增强（日志、事务）。  
- 静态代理 / JDK 动态代理 / CGLIB。  
- **Spring AOP** 同源思想。

---

## 5. 策略

- 算法可替换，消灭巨型 if-else。  
- 例：支付渠道、优惠计算。

---

## 6. 模板方法

- 父类定骨架，子类覆写步骤。  
- 例：同一流程不同明细。

---

## 7. 观察者

- 发布-订阅；事件驱动。  
- Spring `ApplicationEvent` 大量使用。

---

## 8. Spring 中常见模式

| 模式 | 体现 |
|------|------|
| 工厂 | BeanFactory |
| 单例 | 默认 Bean 作用域 |
| 代理 | AOP |
| 模板方法 | JdbcTemplate 等 |
| 观察者 | 事件 |

---

# 自测

- [ ] DCL 单例要点  
- [ ] 策略 vs 模板  
- [ ] 代理与 AOP  

**口述：** [设计模式面渣级口述.md](./设计模式面渣级口述.md) · **卡片：** [设计模式卡片速记.md](./设计模式卡片速记.md)
"""

# =============================================================================
MS = f"""# 分布式 · 高频八股知识点（加分）

{nav('微服务与分布式面渣级口述.md', '微服务与分布式卡片速记.md')}

---

## 1. CAP / BASE？

- **CAP**：分区时在 C（强一致）与 A（可用）间权衡。  
- **BASE**：基本可用、软状态、最终一致（互联网常见）。  

---

## 2. 分布式事务常见方案？

| 方案 | 要点 |
|------|------|
| 2PC | 协调者两阶段；阻塞、单点问题 |
| TCC | Try-Confirm-Cancel；业务侵入 |
| Saga | 长事务 + 补偿 |
| 本地消息表 / 事务消息 | 最终一致，工程常用 |

选型：能简单不复杂；优先业务可接受的最终一致。

---

## 3. 分布式 ID？

- UUID：简单，无序/长。  
- 号段 / DB 自增：简单有瓶颈。  
- 雪花算法：趋势有序，要处理时钟回拨。  
- 美团 Leaf 等方案了解。

---

## 4. 幂等？

- 同一请求多次 = 一次效果。  
- 手段：唯一键、token、状态机。  

---

## 5. 微服务基础

- 拆分按业务边界。  
- 超时、重试、熔断、限流、链路追踪。  

---

# 自测

- [ ] CAP 一句话  
- [ ] 事务方案对比一句  
- [ ] 幂等手段  

**口述：** [微服务与分布式面渣级口述.md](./微服务与分布式面渣级口述.md) · **卡片：** [微服务与分布式卡片速记.md](./微服务与分布式卡片速记.md)  
**MQ：** [MQ知识点](./MQ高频面试题与知识点.md)
"""

# =============================================================================
MQ = f"""# 消息队列 · 高频八股知识点

{nav('MQ面渣级口述.md', 'MQ卡片速记.md')}

---

## 1. 为什么用 MQ？

- **解耦、削峰、异步**。  
- 代价：最终一致、重复、顺序、积压、运维。

---

## 2. 如何保证消息不丢？

| 环节 | 手段 |
|------|------|
| 生产 | 确认机制（ack）、失败重试 |
| Broker | 持久化、多副本 |
| 消费 | 处理成功再提交 offset/ack |

---

## 3. 如何保证顺序？

- 同业务键进**同一分区/队列**。  
- 单线程消费该分区；并行与顺序矛盾要权衡。

---

## 4. 如何保证幂等？

- 至少一次投递 ⇒ 消费端幂等。  
- 唯一键去重、状态机、业务侧防重表。

---

## 5. Kafka 要点？

- Topic / Partition / Consumer Group / offset。  
- ISR、ack（0/1/all）。  
- 高吞吐日志型存储。

---

## 6. RocketMQ / RabbitMQ 对比直觉？

- RocketMQ：国内业务特性、事务消息、延时消息友好。  
- RabbitMQ：路由灵活、传统企业多。  
- Kafka：日志流、大数据、高吞吐。  
（选型看场景，勿绝对化。）

---

# 自测

- [ ] 不丢三环节  
- [ ] 顺序与幂等  
- [ ] Kafka 分区作用  

**口述：** [MQ面渣级口述.md](./MQ面渣级口述.md) · Kafka/RMQ 面渣见路径  
**卡片：** [MQ卡片速记.md](./MQ卡片速记.md)
"""

# =============================================================================
JAVA8 = f"""# Java 8+ 与常见加分项 · 知识点

{nav('Java面渣级口述.md', 'Java卡片速记.md')}

> 基础模块的补充页：Lambda / Stream / 异步 / 日期。完整口语仍可并入 Java/并发面渣。

---

## 1. Lambda / 函数式接口？

- 匿名函数写法；目标类型为函数式接口（单一抽象方法）。  
- 例：`Runnable`、`Comparator`、自定义 `@FunctionalInterface`。

---

## 2. Stream？

- 声明式处理集合：`filter/map/reduce/collect`。  
- 惰性求值；可 parallel（注意线程安全与场景）。  
- 不要为炫技滥用难读链式。

---

## 3. Optional？

- 显式表达「可能为空」，减少 NPE。  
- `of/ofNullable/map/orElse/orElseGet`。  
- 不要滥用 Optional 做字段类型（看团队规范）。

---

## 4. CompletableFuture？

- 异步编排：`supplyAsync`、`thenApply`、`thenCombine`、`exceptionally`。  
- 自定义线程池，避免共用公共 ForkJoinPool 踩坑。

---

## 5. 新日期 API？

- `LocalDate/LocalDateTime/Instant/ZoneId`。  
- 不可变、线程安全；替代 `Date/Calendar` 老坑。

---

## 6. 其他加分

- 接口 default 方法。  
- 方法引用。  
- Java 11/17/21 LTS：var、Records、模式匹配、**虚拟线程**（见并发篇）。

---

**返回：** [Java 基础+集合](./Java高频面试题与知识点.md) · [并发](./并发高频面试题与知识点.md)
"""

# =============================================================================
OVERVIEW = f"""# Java 八股模块总览（P5–P7）

> 按大厂/中厂高频整理。知识点 = **题目 + 核心要点**；面渣 = 练嘴；卡片 = 速记。

---

## 学习优先级（2026）

```text
项目用到的 > 集合/并发/JVM > MySQL/Redis > Spring > 分布式/MQ
```

原则：**原理 + 对比 + 场景**，不要死背一句话。

---

## 模块索引

| 模块 | 知识点（笔记） | 面渣 | 卡片 |
|------|----------------|------|------|
| 1 基础+集合 | [Java](./Java高频面试题与知识点.md) | [面渣](./Java面渣级口述.md) | [卡](./Java卡片速记.md) |
| 1b Java8+ | [Java8+](./Java8加分项知识点.md) | 同上 | 同上 |
| 2 并发 | [并发](./并发高频面试题与知识点.md) | [面渣](./并发面渣级口述.md) | [卡](./并发卡片速记.md) |
| 3 JVM | [JVM](./JVM高频面试题与知识点.md) | [面渣](./JVM面渣级口述.md) | [卡](./JVM卡片速记.md) |
| 4 Spring | [Spring](./Spring高频面试题与知识点.md) | [面渣](./Spring面渣级口述.md) | [卡](./Spring卡片速记.md) |
| 5 MySQL | [MySQL](./MySQL高频面试题与知识点.md) | [面渣](./MySQL面渣级口述.md) | [卡](./MySQL卡片速记.md) |
| 6 Redis | [Redis](./Redis高频面试题与知识点.md) | [面渣](./Redis面渣级口述.md) | [卡](./Redis卡片速记.md) |
| 7 设计模式 | [模式](./设计模式高频面试题与知识点.md) | [面渣](./设计模式面渣级口述.md) | [卡](./设计模式卡片速记.md) |
| 8 分布式 | [分布式](./微服务与分布式高频面试题与知识点.md) | [面渣](./微服务与分布式面渣级口述.md) | [卡](./微服务与分布式卡片速记.md) |
| 9 MQ | [MQ](./MQ高频面试题与知识点.md) | [面渣](./MQ面渣级口述.md) | [卡](./MQ卡片速记.md) |

---

## 各模块你要能答到什么程度

| 模块 | 达标 |
|------|------|
| 基础 | equals/hashCode、String、值传递、异常体系 |
| 集合 | HashMap 7/8、树化、CHM vs Hashtable |
| 并发 | volatile、线程池参数、AQS 直觉、死锁 |
| JVM | 内存区、可达性、G1、双亲委派、OOM 工具 |
| Spring | 生命周期、AOP 代理、事务失效、循环依赖 |
| MySQL | B+、最左、MVCC、EXPLAIN |
| Redis | 三连、锁、持久化、为什么快 |
| 加分 | 模式场景、CAP、消息不丢/幂等/顺序 |

---

## 可继续深挖（你点名即可）

- HashMap 源码级 put/扩容  
- 线程池完整参数与实战配置  
- G1 回收过程细讲  
- Spring 三级缓存细节  
- 初级 / 中级 / 高级分层卷  

---

## 推荐资料（大纲原列）

- JavaGuide  
- 二哥的 Java 进阶之路（javabetter.cn）  
- 《深入理解 Java 虚拟机》《Java 并发编程的艺术》  

[路径 B · Java 后端](./路径-Java后端.md) · [如何使用](./如何使用本仓库.md) · [首页](./README.md)
"""

PATH_JAVA = f"""# 路径 B · Java 后端

适合：**Java 后端（P5–P7 八股主线）**

**读法：** 知识点过题 → 面渣练说 → 卡片回忆。面渣文件不改。  
**模块总览：** [Java八股模块总览.md](./Java八股模块总览.md)  
[如何使用本仓库.md](./如何使用本仓库.md)

---

## 按顺序学

| 步 | 面渣（怎么说） | 知识点（笔记体） | 卡片 |
|:--:|----------------|------------------|------|
| 1 | [Java](./Java面渣级口述.md) | [基础+集合](./Java高频面试题与知识点.md) · [Java8+](./Java8加分项知识点.md) | [卡](./Java卡片速记.md) |
| 2 | [并发](./并发面渣级口述.md) | [并发八股](./并发高频面试题与知识点.md) | [卡](./并发卡片速记.md) |
| 3 | [JVM](./JVM面渣级口述.md) | [JVM八股](./JVM高频面试题与知识点.md) | [卡](./JVM卡片速记.md) |
| 4 | [MySQL](./MySQL面渣级口述.md) | [MySQL八股](./MySQL高频面试题与知识点.md) | [卡](./MySQL卡片速记.md) |
| 5 | [Redis](./Redis面渣级口述.md) | [Redis八股](./Redis高频面试题与知识点.md) | [卡](./Redis卡片速记.md) |
| 6 | [Spring](./Spring面渣级口述.md) | [Spring八股](./Spring高频面试题与知识点.md) | [卡](./Spring卡片速记.md) |
| 7 | [设计模式](./设计模式面渣级口述.md) | [模式](./设计模式高频面试题与知识点.md) | [卡](./设计模式卡片速记.md) |
| 8 | [MQ](./MQ面渣级口述.md) 等 | [MQ](./MQ高频面试题与知识点.md) · [分布式](./微服务与分布式高频面试题与知识点.md) | 各卡片 |
| 9 | [网络](./计算机网络面渣级口述.md) · [OS](./操作系统面渣级口述.md) | 各知识点 | 各卡片 |
| 10 | [算法](./算法面渣级口述.md) + [30题](./算法高频30题代码册.md) | [算法](./算法高频面试题与知识点.md) | [卡](./算法卡片速记.md) |
| 11 | 系统设计场景口述 | [设计](./后端系统设计高频面试题与知识点.md) | [卡](./后端系统设计卡片速记.md) |
| 12 | [K8s](./Docker与K8s面渣级口述.md) · [STAR](./项目STAR范例-Java.md) · [行为](./行为面试面渣级口述.md) | — | — |

加练：[追问·Java](./追问三连-Java.md) · [手写](./Java面试追问与手写题.md)

```text
基础集合 → 并发 → JVM → MySQL → Redis → Spring → 模式/MQ/分布式 → 网络OS → 算法 → 项目
```

[首页](./README.md) · [AI](./路径-AI工程.md) · [Python](./路径-Python.md)
"""


def main():
    w("Java高频面试题与知识点.md", JAVA)
    w("并发高频面试题与知识点.md", CONC)
    w("JVM高频面试题与知识点.md", JVM)
    w("Spring高频面试题与知识点.md", SPRING)
    w("MySQL高频面试题与知识点.md", MYSQL)
    w("Redis高频面试题与知识点.md", REDIS)
    w("设计模式高频面试题与知识点.md", DP)
    w("微服务与分布式高频面试题与知识点.md", MS)
    w("MQ高频面试题与知识点.md", MQ)
    w("Java8加分项知识点.md", JAVA8)
    w("Java八股模块总览.md", OVERVIEW)
    w("路径-Java后端.md", PATH_JAVA)


if __name__ == "__main__":
    main()
