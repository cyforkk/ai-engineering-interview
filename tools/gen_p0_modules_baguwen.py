# -*- coding: utf-8 -*-
"""
以「超高频/高频/中频/低频 + P0-P4」为主线：
- 重写四档导航为大纲权威版
- JVM / MySQL / Redis 超高频完整卷
- MyBatis 中频短页
不碰面渣。
"""
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def w(name, text):
    p = DOCS / name
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print("W", name, p.stat().st_size)


# =============================================================================
MASTER = r'''# Java 后端高频八股 · 权威导航（按频率）

> **本页 = 复习主线。** 按 2025–2026 大厂/中厂面经整理：先超高频，再高频。  
> 每个点：原理 + 核心流程 + 场景 +「为什么」。  
> 姊妹（纯 Java 序号）：[SABC](./Java八股频率排序-SABC.md) · [Spring 专项](./Spring八股频率排序-SABC.md)

---

## 高效背八股

1. 先懂 **为什么**，再记怎么做  
2. 每点准备 **1～2 个项目场景**  
3. **画图**：HashMap、线程池、JVM 内存、三级缓存  
4. 关注：Java 17/21、虚拟线程、G1/ZGC  

```text
知识点过题 → 面渣练说 2 分钟 → 卡片遮挡 → 追问
```

---

## P0～P4 时间占比（2026）

| 优先级 | 模块 | 时间 | 入口 |
|--------|------|:----:|------|
| **P0** | 集合 + 并发 + MySQL + Redis | **40%** | [集合](./Java集合框架高频面试题与知识点.md) · [并发](./并发高频面试题与知识点.md) · [MySQL](./MySQL高频面试题与知识点.md) · [Redis](./Redis高频面试题与知识点.md) |
| **P1** | JVM + Spring | **25%** | [JVM](./JVM高频面试题与知识点.md) · [Spring](./Spring高频面试题与知识点.md) |
| **P2** | Java 基础 + 设计模式 | **15%** | [基础](./Java高频面试题与知识点.md) · [模式](./设计模式高频面试题与知识点.md) |
| **P3** | MQ + 分布式 | **10%** | [MQ](./MQ高频面试题与知识点.md) · [分布式](./微服务与分布式高频面试题与知识点.md) |
| **P4** | NIO / 反射等 | **10%** | [网络](./计算机网络高频面试题与知识点.md) · [Java8+](./Java8加分项知识点.md) |

**路径：** [路径-Java后端.md](./路径-Java后端.md)

---

# 一、超高频（几乎必问 · 优先）

## 1. 集合框架

| 必考点 | 文档 |
|--------|------|
| HashMap 结构 / put / 扩容 / 冲突 | [集合完整卷](./Java集合框架高频面试题与知识点.md) |
| ConcurrentHashMap 1.7 vs 1.8 | 同上 |
| ArrayList vs LinkedList / 扩容 | 同上 |
| HashSet / TreeMap / LinkedHashMap | 同上 |
| fail-fast / fail-safe | 同上 |

🗣️ [Java面渣](./Java面渣级口述.md) · 🃏 [集合卡](./Java集合卡片速记.md)

## 2. 并发编程

| 必考点 | 文档 |
|--------|------|
| synchronized vs ReentrantLock、锁升级 | [并发完整卷](./并发高频面试题与知识点.md) |
| volatile | 同上 |
| 线程池参数 / 流程 / 拒绝 / 设参 | 同上 |
| CAS / ABA | 同上 |
| AQS 独占/共享 | 同上 |
| 创建线程、状态流转 | 同上 |
| Latch / Barrier / Semaphore | 同上 |

🗣️ [并发面渣](./并发面渣级口述.md) · 🃏 [并发卡](./并发卡片速记.md)

## 3. JVM

| 必考点 | 文档 |
|--------|------|
| 内存区域 | [JVM完整卷](./JVM高频面试题与知识点.md) |
| GC 算法 + CMS/G1/ZGC | 同上 |
| 类加载 + 双亲委派 | 同上 |
| 对象创建与内存布局 | 同上 |
| GC 调优参数与排查 | 同上 + [面渣场景](./JVM面渣级口述.md) |

🗣️ [JVM面渣](./JVM面渣级口述.md) · 🃏 [JVM卡](./JVM卡片速记.md)

## 4. Spring / Spring Boot

| 必考点 | 文档 |
|--------|------|
| IoC / AOP | [Spring完整卷](./Spring高频面试题与知识点.md) |
| 循环依赖三级缓存 | 同上 |
| Bean 生命周期 | 同上 |
| Boot 自动装配 | 同上 |
| MVC 流程 | 同上 |

🗣️ [Spring面渣](./Spring面渣级口述.md) · 🔥 [Spring频率](./Spring八股频率排序-SABC.md) · 🃏 [Spring卡](./Spring卡片速记.md)

## 5. MySQL

| 必考点 | 文档 |
|--------|------|
| B+ 索引 / 最左 / 失效 | [MySQL完整卷](./MySQL高频面试题与知识点.md) |
| 隔离级别 + MVCC | 同上 |
| 行锁 / 间隙锁 / 临键锁 | 同上 |
| 慢查询 / Explain | 同上 |

🗣️ [MySQL面渣](./MySQL面渣级口述.md) · 🃏 [MySQL卡](./MySQL卡片速记.md)

## 6. Redis

| 必考点 | 文档 |
|--------|------|
| 数据结构与场景 | [Redis完整卷](./Redis高频面试题与知识点.md) |
| RDB / AOF | 同上 |
| 穿透击穿雪崩 | 同上 |
| 分布式锁 / Redisson | 同上 |
| 过期删除 + 淘汰策略 | 同上 |

🗣️ [Redis面渣](./Redis面渣级口述.md) · 🃏 [Redis卡](./Redis卡片速记.md)

---

# 二、高频（大概率）

### Java 基础
[Java基础完整卷](./Java高频面试题与知识点.md) · [卡片](./Java卡片速记.md)  
equals/hashCode、String、OOP、final/finally/finalize、深浅拷贝、异常体系

### 并发进阶
[并发完整卷](./并发高频面试题与知识点.md)  
死锁、ThreadLocal、悲观/乐观锁、Happens-Before、阻塞队列（[集合 Queue](./Java集合框架高频面试题与知识点.md)）

### JVM 进阶
[JVM完整卷](./JVM高频面试题与知识点.md)  
四类引用、Full GC、打破双亲委派

### Spring 进阶
[Spring完整卷](./Spring高频面试题与知识点.md) · [设计模式](./设计模式高频面试题与知识点.md)  
事务传播、@Transactional 失效、Spring 中的模式

### 中间件
[MQ](./MQ高频面试题与知识点.md) · [分布式](./微服务与分布式高频面试题与知识点.md)  
可靠性/顺序/幂等；2PC/TCC/本地消息表/Seata

---

# 三、中频

| 点 | 入口 |
|----|------|
| Java 8 | [Java8+](./Java8加分项知识点.md) |
| 反射 / 泛型 / 序列化 | [Java基础](./Java高频面试题与知识点.md) |
| 动态代理 | [Spring AOP](./Spring高频面试题与知识点.md) |
| BIO/NIO/AIO | [网络](./计算机网络高频面试题与知识点.md) · [OS](./操作系统高频面试题与知识点.md) |
| 设计模式 | [设计模式](./设计模式高频面试题与知识点.md) |
| DCL 单例 | [并发](./并发高频面试题与知识点.md) · [模式](./设计模式高频面试题与知识点.md) |
| **MyBatis** | [MyBatis知识点](./MyBatis高频面试题与知识点.md) |

---

# 四、低频深挖

字节码/JIT、ZGC/Shenandoah、虚拟线程、JMM 细节、自定义 ClassLoader、Spring 源码细节、限流熔断一致性哈希、TCP/HTTP、Redis 集群  
→ 见各完整卷末「可继续深挖」+ 面渣场景

---

## 两周冲刺（对齐 P0–P1）

| 周 | 内容 |
|----|------|
| 第 1 周 | 集合 HashMap/CHM → 并发锁/池/AQS → MySQL 索引事务锁 → Redis 三连+锁 |
| 第 2 周 | JVM 内存 GC 排查 → Spring 自动装配/生命周期/三级缓存 → 面渣录音 + 项目 STAR |

---

## 点名深挖

HashMap 连环问 / 线程池调优 / 循环依赖 / MVCC / Redis 三连 / G1 … 直接发模块名。

[首页](./README.md) · [如何使用](./如何使用本仓库.md)

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 定为权威主线导航；P0 六大超高频全链完整卷 |
'''

# =============================================================================
JVM = r'''# JVM · 高频八股知识点（完整卷 · 超高频）

<!-- NAV:START -->
> 📖 **JVM 八股** · 🗣️ [面渣](./JVM面渣级口述.md) · 🃏 [卡片](./JVM卡片速记.md)
>
> [权威导航·四档](./Java后端面试频率-四档.md) · [模块总览](./Java八股模块总览.md)
>
<!-- NAV:END -->

> 超高频：内存区、GC、类加载、对象布局、排查调优。

---

# 一、运行时数据区（必考）

## 1. JVM 内存区域有哪些？

| 区域 | 线程 | 作用 |
|------|------|------|
| 程序计数器 | 私有 | 当前字节码行号；唯一不会 OOM 的区（规范层面） |
| 虚拟机栈 | 私有 | 栈帧：局部变量表、操作数栈、动态链接、返回地址 |
| 本地方法栈 | 私有 | native 方法 |
| **堆** | 共享 | 对象实例；GC 主战场 |
| 方法区 / **元空间** | 共享 | 类元数据、常量等（JDK8+ 元空间用本地内存） |
| **直接内存** | 堆外 | NIO DirectByteBuffer 等，受本机/容器限制 |

### 堆分代（常见模型）

```text
堆
├── 新生代 Young
│    ├── Eden
│    ├── Survivor0
│    └── Survivor1
└── 老年代 Old
```

- 多数对象朝生夕死 → 新生代频繁回收。  
- 长期存活 / 大对象可进老年代。

---

## 2. 栈溢出 vs 堆溢出？

| 现象 | 常见原因 |
|------|----------|
| StackOverflowError | 递归过深、栈帧过大 |
| OutOfMemoryError: Java heap space | 堆不够 / 泄漏 |
| Metaspace | 类太多或类加载泄漏 |
| Direct buffer memory | 堆外分配过多 |

---

# 二、垃圾回收（必考）

## 3. 如何判断对象可回收？

- **引用计数**：循环引用问题；Java 不用作主方案。  
- **可达性分析**：从 GC Roots 不可达 → 可回收。  
- Roots：栈引用、静态变量、常量、JNI、同步锁持有对象等。

---

## 4. 垃圾回收算法？

| 算法 | 要点 | 典型 |
|------|------|------|
| 标记-清除 | 碎片 | 老年代历史/CMS 类 |
| 复制 | 活对象少高效 | 新生代 |
| 标记-整理 | 无碎片、移动成本 | 老年代 |
| 分代收集 | 不同代不同策略 | 现代基础 |

---

## 5. 常见收集器？CMS / G1 / ZGC？

| 收集器 | 特点 |
|--------|------|
| Serial / ParNew | 简单 / 新生代并行 |
| Parallel | 吞吐优先 |
| **CMS** | 并发标记清除，低停顿；碎片、浮动垃圾；已淘汰趋势 |
| **G1** | Region、可预测停顿、JDK9+ 常见默认 |
| **ZGC** | 超低延迟（大堆），大厂加分 |
| Shenandoah | 低延迟另一选择（了解） |

### G1 要点

- 堆拆 Region；优先回收「收益高」的 Region。  
- 可设停顿目标（如 `-XX:MaxGCPauseMillis`）。  
- Remembered Set 维护跨 Region 引用。

### Minor / Mixed / Full GC（直觉）

- Young/Minor：收新生代。  
- Mixed（G1）：年轻代 + 部分老年代 Region。  
- **Full GC**：整堆等大范围，停顿通常更重，要少触发。

---

## 6. Full GC 常见触发？（高频进阶）

- 老年代空间不足  
- 元空间不足  
- `System.gc()`（不推荐依赖）  
- 大对象直接进老年代失败  
- 统计/晋升失败等（与收集器有关）  

---

# 三、对象创建与内存布局（超高频补齐）

## 7. 对象创建过程？（简化）

1. **类加载检查**（类是否已加载）  
2. **分配内存**（指针碰撞 / 空闲列表；TLAB 优化）  
3. **零值初始化**  
4. **设置对象头**  
5. **执行构造** `<init>`  

## 8. 对象内存布局？

```text
对象头 Object Header
  ├── Mark Word（hash、锁、GC 年龄等）
  └── 类型指针（指向类元数据；压缩指针时有差异）
实例数据
对齐填充（8 字节对齐）
```

- 数组多一段数组长度。  
- 与 **synchronized 锁升级**（Mark Word）呼应。

---

# 四、引用类型

## 9. 强 / 软 / 弱 / 虚引用？

| 类型 | 回收时机 | 场景 |
|------|----------|------|
| 强 Strong | 不达则不收 | 普通引用 |
| 软 Soft | 内存不足易收 | 缓存 |
| 弱 Weak | GC 时发现即收 | ThreadLocal key、WeakHashMap |
| 虚 Phantom | 形同无引用，用于回收跟踪 | 堆外释放等 |

---

# 五、类加载与双亲委派

## 10. 类加载过程？

```text
加载 → 验证 → 准备 → 解析 → 初始化
```

- 准备：静态变量默认零值。  
- 初始化：执行 `<clinit>`（静态赋值与静态块）。

## 11. 双亲委派？为什么需要？可破坏吗？

- 先委派父加载器，父没有再自己加载。  
- **为什么**：保证核心类唯一、安全（防伪造 `java.lang.String`）。  
- **破坏场景**：SPI（JDBC）、Tomcat 隔离、热部署、OSGi、自定义 ClassLoader。  

---

# 六、排查与调优

## 12. 常见 GC / 内存问题排查思路？

```text
现象（FullGC频繁 / OOM / CPU高）
 → 对齐时间线与监控（GC 日志、heap）
 → jstat / jmap / jstack / dump
 → MAT 看占用与引用链 / 栈看热点
 → 根因：泄漏、分配过快、参数不当、元空间
 → 止血 + 根治 + 回归
```

### 常用参数（会说含义即可）

| 参数 | 含义 |
|------|------|
| -Xms / -Xmx | 堆初始/最大（常设相同减抖动） |
| -Xmn | 年轻代大小（慎用，G1 常不靠它） |
| -XX:+UseG1GC | 使用 G1 |
| -XX:MaxGCPauseMillis | G1 停顿目标 |
| -XX:MetaspaceSize | 元空间 |
| -XX:+HeapDumpOnOutOfMemoryError | OOM 时 dump |

### 工具

jps、jstat、jmap、jstack、MAT、Arthas（加分）、GC 日志。

---

# 自测

- [ ] 五区 + 堆分代  
- [ ] 可达性 + 三种算法  
- [ ] G1 vs CMS vs ZGC 各一句  
- [ ] 对象头含什么  
- [ ] 双亲委派为什么 + 破坏场景  
- [ ] OOM 排查四步  

**口述（含场景）：** [JVM面渣级口述.md](./JVM面渣级口述.md)  
**卡片：** [JVM卡片速记.md](./JVM卡片速记.md)  
**导航：** [四档主线](./Java后端面试频率-四档.md)

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 超高频完整卷：补对象布局、引用、FullGC、参数 |
'''

# =============================================================================
MYSQL = r'''# MySQL · 高频八股知识点（完整卷 · 超高频）

<!-- NAV:START -->
> 📖 **MySQL 八股** · 🗣️ [面渣](./MySQL面渣级口述.md) · 🃏 [卡片](./MySQL卡片速记.md)
>
> [权威导航·四档](./Java后端面试频率-四档.md) · [路径](./路径-Java后端.md)
>
<!-- NAV:END -->

---

# 一、索引（必考）

## 1. 为什么用 B+ 树？

- 矮胖，减少磁盘 IO。  
- 叶子存数据/主键并有序链表，**范围查询**友好。  
- 对比：哈希点查快但范围弱；二叉树太高。

## 2. 聚簇索引 vs 二级索引？

- **聚簇（主键）**：叶子 = **整行**。  
- **二级**：叶子 = **主键值** → 常 **回表**。  
- **覆盖索引**：二级已含查询列，免回表。  
- **索引下推 ICP**：引擎层过滤，减回表（了解加分）。

## 3. 最左前缀？

- 联合索引 `(a,b,c)`：从左连续用 a / a,b / a,b,c。  
- 只有 b 或 c 通常用不好。

## 4. 索引失效常见场景？

- 对索引列套函数/运算  
- `LIKE '%x'` 左模糊  
- 类型隐式转换  
- 违背最左  
- or 一侧无索引、优化器认为全表更便宜  
- **以 EXPLAIN 为准**

---

# 二、事务与 MVCC（必考）

## 5. ACID？隔离级别？读问题？

- 原子 / 一致 / 隔离 / 持久。  
- 脏读 / 不可重复读 / 幻读。  
- 级别：RU → RC → **RR（InnoDB 默认）** → Serializable。

## 6. MVCC 如何实现？

- **undo log** 版本链 + **ReadView**。  
- **快照读**：普通 SELECT。  
- **当前读**：`FOR UPDATE` / 更新删除。  
- 提高读写并发。

---

# 三、锁（必考）

## 7. 行锁、间隙锁、临键锁？

| 锁 | 含义 |
|----|------|
| 行锁 | 锁索引记录 |
| 间隙锁 | 锁索引记录之间的间隙，防幻读插入 |
| 临键锁 | 行锁 + 间隙锁（RR 下常见） |

- 锁加在索引上；无索引可能锁更多甚至表级倾向。  
- 死锁：InnoDB 检测回滚一方；`SHOW ENGINE INNODB STATUS`。

---

# 四、慢查询与 Explain（必考）

## 8. 慢 SQL 优化步骤？

1. 慢日志 / 监控定位  
2. **EXPLAIN**  
3. 加索引 / 改写 SQL / 避免 select *  
4. 验证  

### EXPLAIN 关键字段

| 字段 | 看什么 |
|------|--------|
| type | 访问类型（const/ref/range/index/ALL…） |
| key | 实际用的索引 |
| rows | 估计扫描行 |
| Extra | Using filesort / temporary / Using index（覆盖）等 |

### 深分页

`LIMIT 大偏移` 差 → `id > last` 或延迟关联。

---

# 五、引擎与日志

## 9. InnoDB vs MyISAM？

| | InnoDB | MyISAM |
|--|--------|--------|
| 事务 | ✓ | ✗ |
| 行锁 | ✓ | 表锁为主 |
| 外键 | ✓ | ✗ |
| 现代默认 | **是** | 历史 |

## 10. redo / undo / binlog？

- redo：崩溃恢复（WAL）  
- undo：回滚 + MVCC  
- binlog：复制与归档  

---

# 自测

- [ ] B+ / 回表 / 覆盖 / 最左 / 失效  
- [ ] MVCC 一句话  
- [ ] 三种锁  
- [ ] EXPLAIN 四字段  
- [ ] 慢 SQL 四步  

**口述：** [MySQL面渣级口述.md](./MySQL面渣级口述.md) · **卡片：** [MySQL卡片速记.md](./MySQL卡片速记.md)

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 超高频完整卷对齐四档大纲 |
'''

# =============================================================================
REDIS = r'''# Redis · 高频八股知识点（完整卷 · 超高频）

<!-- NAV:START -->
> 📖 **Redis 八股** · 🗣️ [面渣](./Redis面渣级口述.md) · 🃏 [卡片](./Redis卡片速记.md)
>
> [权威导航·四档](./Java后端面试频率-四档.md) · [路径](./路径-Java后端.md)
>
<!-- NAV:END -->

---

# 一、为什么快 + 数据结构

## 1. Redis 为什么快？

- 内存  
- 命令执行**单线程**（无锁竞争）  
- 高效结构  
- IO 多路复用  
- Redis6+ 多线程主要加速网络，非命令随意并行  

## 2. 五种类型与场景？

| 类型 | 场景 | 底层（加分） |
|------|------|----------------|
| String | 缓存、计数、锁 | SDS |
| Hash | 对象字段 | hashtable/listpack |
| List | 列表/队列 | quicklist |
| Set | 去重、关系 | intset/hashtable |
| ZSet | 排行榜 | **skiplist** + dict |

---

# 二、持久化

## 3. RDB vs AOF vs 混合？

| | RDB | AOF |
|--|-----|-----|
| 内容 | 快照 | 写命令日志 |
| 恢复 | 快 | 更完整（视 fsync） |
| 体积 | 相对小 | 可重写压缩 |
| 丢数据 | 最近间隔 | 看策略 |

- **混合持久化**：兼顾。  

---

# 三、缓存三连（必考）

## 4. 穿透 / 击穿 / 雪崩？

| 问题 | 定义 | 方案 |
|------|------|------|
| **穿透** | 查不存在 | 空值缓存、布隆、校验 |
| **击穿** | 热点过期 | 互斥重建、逻辑过期 |
| **雪崩** | 大量同时过期或 Redis 挂 | TTL 抖动、HA、限流、多级缓存 |

---

# 四、分布式锁

## 5. 如何实现？Redisson？

```text
SET key unique_value NX EX seconds
```

- NX 互斥；EX 防死锁；unique 防误删；**Lua** 校验删除。  
- **Redisson**：看门狗自动续期；API 封装。  
- 风险：主从切换极端丢锁；业务评估。  

---

# 五、过期与淘汰

## 6. 过期删除策略？

- **惰性删除**：访问时发现过期再删。  
- **定期删除**：抽样清理。  
- 不是对每个 key 精确定时器全扫。  

## 7. 内存淘汰策略？

内存达到 maxmemory 时：

| 策略 | 含义 |
|------|------|
| noeviction | 不淘汰，写报错 |
| allkeys-lru | 所有 key 里 LRU |
| volatile-lru | 有过期时间的 key 里 LRU |
| allkeys-lfu / volatile-lfu | LFU |
| volatile-ttl | 优先更短 TTL |
| random 等 | 了解 |

---

# 六、一致性

## 8. Cache Aside？

- 读：缓存 → DB → 回填  
- 写：**先 DB 再删缓存**  
- 删失败重试/补偿；多最终一致  

---

# 自测

- [ ] 为什么快四点  
- [ ] 五类型场景  
- [ ] 三连不混  
- [ ] 锁四要素 + Redisson  
- [ ] 过期 + 淘汰举例  

**口述：** [Redis面渣级口述.md](./Redis面渣级口述.md) · **卡片：** [Redis卡片速记.md](./Redis卡片速记.md)

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 超高频完整卷对齐四档大纲 |
'''

# =============================================================================
MYBATIS = r'''# MyBatis · 高频知识点（中频）

<!-- NAV:START -->
> 📖 **MyBatis** · [四档导航](./Java后端面试频率-四档.md) · [路径](./路径-Java后端.md)
>
<!-- NAV:END -->

---

## 1. #{} 与 ${} 区别？（必考）

| | `#{}` | `${}` |
|--|-------|-------|
| 方式 | 预编译占位 `?` | 字符串拼接 |
| SQL 注入 | **安全** | **有风险** |
| 用途 | 参数值 | 表名/列名等动态标识（需白名单） |

**结论：能用 #{} 绝不用 ${}。**

---

## 2. 一级缓存？二级缓存？

| | 一级 | 二级 |
|--|------|------|
| 范围 | **SqlSession** | **Mapper 命名空间**（跨 Session，需配置） |
| 默认 | 开启 | 默认关，需显式开 |
| 注意 | Session 关闭/提交等会清 | 分布式下本地二级缓存易脏，慎用 |

---

## 3. 其他常问

- `#{}` 与 `PreparedStatement`  
- 动态 SQL：`if/where/foreach`  
- 延迟加载（关联查询）  
- 与 Spring 整合：SqlSession 线程安全由模板/代理管理  

---

## 自测

- [ ] #{} vs ${}  
- [ ] 一级 vs 二级范围  
- [ ] 为何生产慎用二级缓存  

[四档主线](./Java后端面试频率-四档.md)
'''


def patch_nav():
    # README
    r = DOCS / "README.md"
    if r.exists():
        t = r.read_text(encoding="utf-8")
        if "权威导航" not in t:
            t = t.replace(
                "| Java 后端 | **[路径 B](./路径-Java后端.md)** · [总览](./Java八股模块总览.md) · [SABC](./Java八股频率排序-SABC.md) · [**四档P0**](./Java后端面试频率-四档.md) |",
                "| Java 后端 | **[路径 B](./路径-Java后端.md)** · [**四档主线P0**](./Java后端面试频率-四档.md) · [总览](./Java八股模块总览.md) · [SABC](./Java八股频率排序-SABC.md) |",
            )
            r.write_text(t, encoding="utf-8")
            print("readme")

    # path
    p = DOCS / "路径-Java后端.md"
    if p.exists():
        t = p.read_text(encoding="utf-8")
        if "权威导航" not in t and "四档主线" not in t:
            t = t.replace(
                "**读法：** 知识点过题 → 面渣练说 → 卡片回忆。面渣文件不改。",
                "**读法：** 先按 [**四档主线（P0 超高频）**](./Java后端面试频率-四档.md) → 知识点过题 → 面渣练说 → 卡片。面渣不改。",
            )
            p.write_text(t, encoding="utf-8")
            print("path")

    # sidebar - put 四档 first in java section
    sb = DOCS / "_sidebar.md"
    if sb.exists():
        t = sb.read_text(encoding="utf-8")
        if "四档主线" not in t:
            t = t.replace(
                "  * [🔥 四档+P0时间表](Java后端面试频率-四档.md)\n",
                "  * [🔥 **四档主线 P0**](Java后端面试频率-四档.md)\n",
            )
            sb.write_text(t, encoding="utf-8")
            print("sidebar")

    # overview
    ov = DOCS / "Java八股模块总览.md"
    if ov.exists():
        t = ov.read_text(encoding="utf-8")
        if "四档主线" not in t:
            t = t.replace(
                "> **按面试频率复习：** [SABC 排序](./Java八股频率排序-SABC.md) · [**四档+P0时间表**](./Java后端面试频率-四档.md)",
                "> **复习主线：** [**四档 P0 超高频**](./Java后端面试频率-四档.md) · [SABC](./Java八股频率排序-SABC.md)",
            )
            ov.write_text(t, encoding="utf-8")
            print("overview")

    # jvm cards light update
    jvm_card = DOCS / "JVM卡片速记.md"
    if jvm_card.exists():
        c = '''# JVM · 卡片速记

<!-- NAV:START -->
> [完整卷](./JVM高频面试题与知识点.md) · [面渣](./JVM面渣级口述.md) · [四档](./Java后端面试频率-四档.md)
<!-- NAV:END -->

**Q1 内存区？** A: 计数器/栈/本地栈私有；堆与方法区(元空间)共享；直接内存堆外。

**Q2 堆分代？** A: 新生代Eden+S0/S1 + 老年代。

**Q3 如何判垃圾？** A: 可达性分析；非引用计数。

**Q4 GC算法？** A: 标记清除、复制、标记整理、分代。

**Q5 G1？** A: Region；可控停顿；优先收收益高区。

**Q6 ZGC？** A: 超低延迟收集器（加分）。

**Q7 双亲委派？** A: 先父后子；核心类唯一安全。

**Q8 破坏场景？** A: SPI、Tomcat、热部署。

**Q9 对象布局？** A: 对象头(Mark+类型指针)+实例数据+对齐。

**Q10 四引用？** A: 强软弱虚。

**Q11 Full GC？** A: 老年代/元空间不足等；停顿重。

**Q12 OOM排查？** A: 日志→jmap dump→MAT引用链→根治。

详解：[JVM高频面试题与知识点.md](./JVM高频面试题与知识点.md)
'''
        jvm_card.write_text(c, encoding="utf-8")
        print("jvm card")

    # mysql/redis cards brief refresh
    (DOCS / "MySQL卡片速记.md").write_text('''# MySQL · 卡片速记

> [完整卷](./MySQL高频面试题与知识点.md) · [面渣](./MySQL面渣级口述.md) · [四档](./Java后端面试频率-四档.md)

**Q1 B+？** A: 矮胖适合磁盘；范围查询友好。

**Q2 回表？** A: 二级索引找到主键再查聚簇。

**Q3 最左？** A: (a,b,c) 从左连续用。

**Q4 失效？** A: 函数、左模糊、隐式转换、违背最左。

**Q5 默认隔离？** A: RR。

**Q6 MVCC？** A: undo版本链+ReadView；快照读。

**Q7 临键锁？** A: 行锁+间隙锁。

**Q8 EXPLAIN？** A: type/key/rows/Extra。

**Q9 慢SQL？** A: 慢日志→EXPLAIN→改→验证。

**Q10 InnoDB？** A: 事务+行锁；现代默认。

详解：[MySQL高频面试题与知识点.md](./MySQL高频面试题与知识点.md)
''', encoding="utf-8")
    print("mysql card")

    (DOCS / "Redis卡片速记.md").write_text('''# Redis · 卡片速记

> [完整卷](./Redis高频面试题与知识点.md) · [面渣](./Redis面渣级口述.md) · [四档](./Java后端面试频率-四档.md)

**Q1 为何快？** A: 内存、单线程命令、高效结构、多路复用。

**Q2 五类型？** A: String/Hash/List/Set/ZSet 各一场景。

**Q3 穿透？** A: 不存在→空值/布隆。

**Q4 击穿？** A: 热点过期→互斥/逻辑过期。

**Q5 雪崩？** A: 大量过期或挂→TTL抖动+HA。

**Q6 锁？** A: SET NX EX + 唯一值 + Lua；Redisson续期。

**Q7 RDB/AOF？** A: 快照 vs 命令日志。

**Q8 过期？** A: 惰性+定期。

**Q9 淘汰？** A: allkeys-lru 等。

**Q10 Cache Aside写？** A: 先DB再删缓存。

详解：[Redis高频面试题与知识点.md](./Redis高频面试题与知识点.md)
''', encoding="utf-8")
    print("redis card")


def main():
    w("Java后端面试频率-四档.md", MASTER)
    w("JVM高频面试题与知识点.md", JVM)
    w("MySQL高频面试题与知识点.md", MYSQL)
    w("Redis高频面试题与知识点.md", REDIS)
    w("MyBatis高频面试题与知识点.md", MYBATIS)
    patch_nav()


if __name__ == "__main__":
    main()
