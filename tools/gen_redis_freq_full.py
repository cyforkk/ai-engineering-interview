# -*- coding: utf-8 -*-
"""Redis：按超高/高/中/低频完整卷 + 频率导航。不碰面渣。"""
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def w(name, text):
    p = DOCS / name
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print(name, p.stat().st_size)


NAV = """<!-- NAV:START -->
> 📖 **Redis 完整卷** · 🗣️ [面渣](./Redis面渣级口述.md) · 🃏 [卡片](./Redis卡片速记.md) · 🔥 [频率导航](./Redis八股频率排序.md)
>
> [四档主线](./Java后端面试频率-四档.md) · [MySQL](./MySQL高频面试题与知识点.md)
>
<!-- NAV:END -->
"""

REDIS = f"""# Redis · 高频八股知识点（完整卷）

{NAV}

> 后端面试出现频率极高。**三连 + 持久化 + 分布式锁 + 数据类型** 几乎必考。  
> 建议：原理 + **项目场景** + 方案优缺点与失败怎么办。

### 专项时间占比

| 优先级 | 模块 | 时间 |
|--------|------|:----:|
| **P0** | 数据类型 + 缓存三大问题 + 持久化 + 分布式锁 | **50%** |
| **P1** | 主从/哨兵/Cluster + 过期淘汰 + 双写一致性 | **25%** |
| **P2** | 为什么快 + Pipeline/Lua + 大Key/热Key | **15%** |
| **P3** | 底层结构 + 运维监控 | **10%** |

### 高效准备

1. 三连 + 锁 + 持久化 **能结合项目讲**  
2. 类型：底层 + 复杂度 + 业务场景  
3. 准备：穿透击穿、分布式锁、缓存预热与双写  
4. 追问：为何这方案？更好吗？失败怎么办？  

---

# 一、超高频（几乎必问）

## 1. 数据类型及场景

### 1.1 基本类型与底层（了解加分）

| 类型 | 典型底层（随版本演进） | 直觉 |
|------|------------------------|------|
| String | SDS | 二进制安全动态串 |
| Hash | hashtable / listpack | 字段对象 |
| List | quicklist（listpack 链表） | 列表 |
| Set | intset / hashtable | 去重集合 |
| ZSet | **skiplist** + dict | 有序集合 |

### 1.2 业务场景

| 类型 | 场景 |
|------|------|
| String | 缓存 JSON、计数器、Session、分布式锁、限流计数 |
| Hash | 用户资料多字段、购物车 |
| List | 最新消息、简单队列、时间线 |
| Set | 点赞、关注、共同好友、抽奖去重 |
| ZSet | **排行榜**、延时任务（score=时间） |

### 1.3 String 为何能做计数器/锁/Session？

- 原子 `INCR`/`DECR` 做计数  
- `SET NX EX` 做锁  
- 字符串存 Session/Token，TTL 自动过期  

### 1.4 ZSet 排行榜与跳表？

- `ZADD` 按 score；`ZREVRANGE` 取 TopN  
- **跳表**：多层有序链表，平均查找 O(log n)，实现相对简单，范围查询友好  
- 同时用 dict 保证 member→score O(1)  

### 1.5 扩展类型场景

| 类型 | 场景 |
|------|------|
| Bitmap | 签到、布尔统计 |
| HyperLogLog | 基数估算（UV），省内存有误差 |
| GEO | 附近的人、距离 |
| Stream | 消息流、消费组（近似 MQ） |

---

## 2. 缓存三大经典问题

### 2.1 穿透

- **定义**：查**根本不存在**的数据，缓存不中，每次打 DB。  
- **解决**：  
  1. 缓存空值（短 TTL）  
  2. **布隆过滤器**拦截一定不存在  
  3. 参数校验、网关限流  

### 2.2 击穿

- **定义**：**热点 key** 过期瞬间，并发打穿 DB。  
- **解决**：  
  1. 互斥锁重建（只一人回源）  
  2. **逻辑过期**（value 带过期时间，异步刷新）  
  3. 热点永不过期 + 后台刷新  

### 2.3 雪崩

- **定义**：大量 key **同时过期**，或 Redis **宕机**，流量打向 DB。  
- **解决**：  
  1. TTL **加随机**，打散过期  
  2. Redis 高可用（主从/哨兵/Cluster）  
  3. 多级缓存、限流熔断降级  
  4. 预热  

### 2.4 三者区别

| | 对象 | 关键词 |
|--|------|--------|
| 穿透 | 不存在的数据 | 假请求/乱 id |
| 击穿 | **单个热点**过期 | 针尖 |
| 雪崩 | **大面积**失效或 Redis 挂 | 一片 |

---

## 3. 持久化

### 3.1 RDB vs AOF

| | RDB | AOF |
|--|-----|-----|
| 内容 | 内存快照 | 写命令日志 |
| 体积 | 相对小 | 通常更大（可重写） |
| 恢复 | 快 | 可更完整 |
| 丢数据 | 最近一次快照后 | 视刷盘策略 |
| 性能影响 | fork 写时复制 | 刷盘策略影响 |

### 3.2 RDB 触发

- `save`：阻塞  
- `bgsave`：子进程，写时复制  
- 配置自动策略：`save 900 1` 等  

### 3.3 AOF 刷盘策略

| 策略 | 含义 |
|------|------|
| always | 每命令刷盘，最安全最慢 |
| **everysec** | 每秒（常用折中） |
| no | 交给 OS，快但丢得多 |

### 3.4 混合持久化（4.0+）

- AOF 重写文件含 **RDB 前缀 + 增量 AOF**，恢复更快、兼顾完整。  

### 3.5 如何选？恢复流程？

| 场景 | 方向 |
|------|------|
| 可丢一点、要恢复快 | 偏 RDB |
| 尽量少丢 | AOF everysec 或混合 |
| 生产常见 | **混合** 或 RDB+AOF |

- 恢复：优先 AOF（若开启）；否则 RDB。混合则按文件格式加载。  

---

## 4. 分布式锁

### 4.1 正确姿势

```text
SET lock_key unique_value NX EX seconds
```

- NX：互斥  
- EX：超时防死锁  
- unique：标识持有者  

### 4.2 简单 SETNX 问题

- 无过期 → 持锁崩溃死锁  
- 固定删 key → **误删别人的锁**  
- 业务超时 > EX → 锁提前释放  

### 4.3 删除原子性

```text
Lua: if get==me then del
```

### 4.4 Redisson 看门狗

- 加锁后后台线程 **定期续期**，避免业务未完锁过期  
- 默认租约与续期间隔可配置  
- 可重入：同线程可再次加锁（本地计数 + Redis）  

### 4.5 RedLock？

- 多独立实例上依次加锁，多数成功才算成功。  
- **争议**：时钟漂移、正确性在学术界/工业界有讨论。  
- 面试：知道用途与争议，业务强一致可考虑 ZK/etcd。  

### 4.6 可重入与原子

- 可重入：hash 存线程标识 + 重入次数（Redisson）  
- 原子：SET NX EX 原子；解锁 Lua 原子  

---

## 5. 过期删除与内存淘汰

### 5.1 过期删除

| 策略 | 含义 |
|------|------|
| **惰性删除** | 访问时发现过期再删 |
| **定期删除** | 定时抽样清理 |

- 不是每个 key 一个定时器全扫。  

### 5.2 内存淘汰（maxmemory）

| 策略 | 含义 |
|------|------|
| noeviction | 不淘汰，写报错 |
| allkeys-lru | 所有 key 中 LRU |
| volatile-lru | 仅有 TTL 的 key LRU |
| allkeys-lfu / volatile-lfu | LFU |
| volatile-ttl | 优先更短 TTL |
| random 等 | 了解 |

### 5.3 LRU vs LFU

| LRU | LFU |
|-----|-----|
| 最久未使用 | 使用频率最低 |
| 扫一次冷数据可能误伤 | 对周期性访问更稳 |

### 5.4 大 Key 问题

- **危害**：阻塞删除/序列化、网络带宽、倾斜、集群迁移难  
- **解决**：拆分 key、压缩、异步删除（UNLINK）、扫描大 key 工具、禁止 bigkeys 操作高峰期  

---

# 二、高频

## 6. 高可用架构

### 6.1 主从复制

- 从连主 → **全量**（RDB/PSYNC）→ 之后 **增量** backlog  
- 主写从读；从默认可设只读  

### 6.2 哨兵 Sentinel

- 监控主从、主观/客观下线、**自动故障转移**、通知客户端新主  
- 适合：主从 + 自动切主，数据量单机可扛  

### 6.3 Cluster

- 数据分片：**16384 哈希槽**，key CRC16 取模映射槽  
- **为何 16384**：心跳包携带槽位图，包大小与实现折中（常考说法）  
- 每个主负责部分槽；从负责复制  
- 高可用：主挂从升；槽可迁移 rebalance  
- **脑裂**：网络分区可能双主写；`min-replicas-to-write` 等缓解  

### 6.4 选型

| 模式 | 场景 |
|------|------|
| 主从 | 读写分离、备份 |
| 哨兵 | 自动切主，容量单机够 |
| Cluster | 数据/流量大，要分片 |

---

## 7. 性能与原理

### 7.1 为什么快？

1. 纯内存  
2. **命令执行单线程**（无锁竞争）  
3. 高效结构  
4. **IO 多路复用**（epoll 等）  

### 7.2 单线程为何高并发？

- 瓶颈多在网络与内存；无锁；命令快。  
- 非 CPU 密集计算型业务。  
- **注意**：大 key、慢命令仍会阻塞整实例。  

### 7.3 epoll 直觉

- 一线程监听多 fd，只处理就绪连接，非一连接一线程阻塞。  

### 7.4 Pipeline vs 事务

| | Pipeline | MULTI/EXEC 事务 |
|--|----------|-----------------|
| 目的 | 批量减 RTT | 命令排队执行 |
| 原子 | 否 | 不保证隔离；**不支持回滚** |
| 场景 | 批量读写提吞吐 | 需一组命令连续执行 |

### 7.5 Lua

- 服务端执行脚本，中间无其他命令插入 → **原子**  
- 场景：限流、解锁、复杂原子逻辑  

---

## 8. 缓存一致性

### 8.1 双写策略

| 策略 | 说明 |
|------|------|
| **Cache Aside** | 读：缓存 miss 再 DB 回填；写：**先 DB 再删缓存** |
| 延迟双删 | 删 → 更 DB → 延迟再删（防并发脏读窗口） |
| binlog 订阅 | 异步删/更新缓存，最终一致 |

### 8.2 为何推荐删而不是更新缓存？

- 更新缓存：并发下难保证顺序，易写脏。  
- 删除：下次读回源，更简单；用 TTL 兜底。  
- 删失败：重试/消息补偿。  

---

# 三、中频

## 9. 事务特点

- `MULTI/EXEC`：队列执行；**错误不回滚**已成功命令（与 DB 事务不同）。  
- `WATCH` 乐观锁。  

## 10. Pub/Sub

- 实时推送；**不持久化**，订阅者不在线会丢。  
- 可靠消息用 Stream 或专业 MQ。  

## 11. 延时队列 / MQ

- ZSet score=执行时间 + 轮询  
- Stream 消费组  
- 复杂可靠 → Kafka/RocketMQ  

## 12. 热 Key

- **危害**：单点打爆、流量倾斜  
- **解决**：本地缓存、打散 key、读写分离、热点发现与限流  

## 13. 慢查询

- `SLOWLOG GET`；避免 keys *、大范围 hgetall、无界 zrange  
- 监控 latency  

## 14. 阻塞常见原因

- 大 key 删除/序列化  
- AOF rewrite / RDB fork  
- 集群gossip 异常  
- 慢客户端 / 客户端缓冲区  

## 15. 布隆过滤器

- 位图 + 多哈希；判断「一定不存在 / 可能存在」  
- **有误判**（假阳性），无假阴性（说不存在一定没有）  

## 16. 分布式限流

- 固定窗口 / 滑动窗口 / 令牌桶  
- Redis + **Lua** 原子增减  

---

# 四、低频 / 进阶加分

- SDS、dict、listpack、quicklist、skiplist 细节  
- **渐进式 rehash**（分步迁移字典，避免一次阻塞）  
- Redis 6 **多线程 IO**：网络读写多线程，命令执行仍单线程逻辑  
- Redis 7 特性（了解）  
- 故障转移与 reshard  
- 内存碎片与 `ACTIVEDFRAG`  
- 监控：命中率、used_memory、QPS、慢查询、连接数、主从延迟  

---

# 自测清单

### P0
- [ ] 五类型 + 场景 + ZSet 跳表一句  
- [ ] 三连定义与方案不混  
- [ ] RDB/AOF/混合 + 刷盘  
- [ ] 锁：NX EX + Lua + 看门狗 + RedLock 争议  

### P1
- [ ] 主从/哨兵/Cluster 槽  
- [ ] 过期 + 淘汰策略  
- [ ] Cache Aside 先 DB 再删  

### P2–P3
- [ ] 为何快 + 单线程  
- [ ] Pipeline vs 事务 vs Lua  
- [ ] 大 Key / 热 Key  

**口述：** [Redis面渣级口述.md](./Redis面渣级口述.md)  
**卡片：** [Redis卡片速记.md](./Redis卡片速记.md)  
**频率：** [Redis八股频率排序.md](./Redis八股频率排序.md)  

---

## 点名深挖

- 穿透/击穿/雪崩完整对比  
- Redisson 锁原理  
- RDB vs AOF 细节  
- 跳表实现 ZSet  

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 按超高/高/中/低频大纲重写 Redis 完整卷 |
"""

RANK = f"""# Redis · 频率导航（2025–2026）

> **完整卷：** [Redis高频面试题与知识点.md](./Redis高频面试题与知识点.md)  
> **面渣：** [Redis面渣级口述.md](./Redis面渣级口述.md) · **卡片：** [Redis卡片速记.md](./Redis卡片速记.md)  
> **全库主线：** [四档 P0](./Java后端面试频率-四档.md)

---

## 专项时间

| 优先级 | 模块 | 时间 |
|--------|------|:----:|
| P0 | 数据类型 + 三连 + 持久化 + 分布式锁 | **50%** |
| P1 | 主从/哨兵/Cluster + 淘汰 + 双写一致 | 25% |
| P2 | 为什么快 + Pipeline/Lua + 大/热 Key | 15% |
| P3 | 底层结构 + 监控运维 | 10% |

---

## 一、超高频

| # | 主题 | 入口 |
|---|------|------|
| 1 | 数据类型与场景（含跳表、扩展类型） | [§1](./Redis高频面试题与知识点.md) |
| 2 | 穿透 / 击穿 / 雪崩 | [§2](./Redis高频面试题与知识点.md) |
| 3 | RDB / AOF / 混合 / 刷盘 | [§3](./Redis高频面试题与知识点.md) |
| 4 | 分布式锁 / Redisson / RedLock | [§4](./Redis高频面试题与知识点.md) |
| 5 | 过期删除 + 内存淘汰 + 大 Key | [§5](./Redis高频面试题与知识点.md) |

---

## 二、高频

主从 · 哨兵 · Cluster 16384 · 为何快 · epoll · Pipeline/事务/Lua · Cache Aside  

---

## 三、中频

Redis 事务 · Pub/Sub · 延时队列 · 热 Key · 慢查询 · 阻塞 · 布隆 · 限流  

---

## 四、低频加分

SDS/跳表细节 · 渐进 rehash · 6.0 多线程 IO · 碎片 · 监控指标  

---

## 必须能讲清的三块

```text
1. 缓存三连（定义不混 + 方案）
2. 分布式锁（NX EX + Lua + 看门狗）
3. RDB vs AOF 选型
```

## 追问链

```text
为何这方案？ → 优缺点？ → 失败怎么办？ → 有没有更好？
```

---

## 点名

`三连对比` · `Redisson` · `RDB/AOF` · `跳表` · `Cluster槽`

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | Redis 专项频率导航 |
"""

CARDS = f"""# Redis · 卡片速记

<!-- NAV:START -->
> [完整卷](./Redis高频面试题与知识点.md) · [频率](./Redis八股频率排序.md) · [面渣](./Redis面渣级口述.md)
<!-- NAV:END -->

> 遮住 A。**先 P0。**

---

## 类型

**Q1 五类型场景？** A: 缓存计数锁/对象字段/列表/去重/排行榜。

**Q2 ZSet 结构？** A: 跳表+dict。

**Q3 Bitmap/HLL/GEO/Stream？** A: 签到/UV/附近/消息流。

## 三连

**Q4 穿透？** A: 不存在→空值/布隆。

**Q5 击穿？** A: 热点过期→互斥/逻辑过期。

**Q6 雪崩？** A: 大量过期或挂→TTL随机+HA+限流。

**Q7 区别？** A: 假数据 vs 单热点 vs 大面积。

## 持久化

**Q8 RDB vs AOF？** A: 快照快恢复 vs 日志更全。

**Q9 AOF 刷盘？** A: always/everysec/no。

**Q10 混合？** A: RDB前缀+增量AOF。

## 锁

**Q11 命令？** A: SET key val NX EX。

**Q12 误删？** A: 唯一value + Lua删。

**Q13 看门狗？** A: Redisson 自动续期。

**Q14 RedLock？** A: 多数实例加锁；有争议。

## 过期淘汰

**Q15 过期？** A: 惰性+定期。

**Q16 淘汰？** A: allkeys-lru/lfu 等。

**Q17 LRU vs LFU？** A: 最久未用 vs 频率。

**Q18 大Key？** A: 拆分、UNLINK、避高峰。

## 高频

**Q19 为何快？** A: 内存、单线程命令、结构、多路复用。

**Q20 主从？** A: 全量+增量复制。

**Q21 哨兵？** A: 监控+自动切主。

**Q22 Cluster？** A: 16384槽分片。

**Q23 Cache Aside写？** A: 先DB再删缓存。

**Q24 Pipeline vs 事务？** A: 减RTT vs 排队不回滚。

**Q25 Lua？** A: 服务端原子执行。

---

详解：[Redis高频面试题与知识点.md](./Redis高频面试题与知识点.md)
"""


def patch():
    ft = DOCS / "Java后端面试频率-四档.md"
    if ft.exists():
        t = ft.read_text(encoding="utf-8")
        if "Redis八股频率排序" not in t:
            t = t.replace(
                "🗣️ [Redis面渣](./Redis面渣级口述.md) · 🃏 [Redis卡](./Redis卡片速记.md)",
                "🗣️ [Redis面渣](./Redis面渣级口述.md) · 🃏 [Redis卡](./Redis卡片速记.md) · 🔥 [Redis频率](./Redis八股频率排序.md)",
            )
            ft.write_text(t, encoding="utf-8")
            print("fourtier")

    sb = DOCS / "_sidebar.md"
    if sb.exists():
        t = sb.read_text(encoding="utf-8")
        if "Redis八股频率排序" not in t:
            t = t.replace(
                "  * [Redis完整卷](Redis高频面试题与知识点.md) · [卡片](Redis卡片速记.md)\n",
                "  * [Redis完整卷](Redis高频面试题与知识点.md) · [频率](Redis八股频率排序.md) · [卡片](Redis卡片速记.md)\n",
            )
            t = t.replace(
                "  * [Redis](Redis高频面试题与知识点.md) · [卡片](Redis卡片速记.md)\n",
                "  * [Redis完整卷](Redis高频面试题与知识点.md) · [频率](Redis八股频率排序.md) · [卡片](Redis卡片速记.md)\n",
            )
            sb.write_text(t, encoding="utf-8")
            print("sidebar")

    path = DOCS / "路径-Java后端.md"
    if path.exists():
        t = path.read_text(encoding="utf-8")
        if "Redis八股频率排序" not in t:
            t = t.replace(
                "[Redis八股](./Redis高频面试题与知识点.md)",
                "[Redis完整卷](./Redis高频面试题与知识点.md)·[频率](./Redis八股频率排序.md)",
            )
            path.write_text(t, encoding="utf-8")
            print("path")


def main():
    w("Redis高频面试题与知识点.md", REDIS)
    w("Redis八股频率排序.md", RANK)
    w("Redis卡片速记.md", CARDS)
    patch()


if __name__ == "__main__":
    main()
