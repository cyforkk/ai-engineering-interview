# Redis · 卡片速记

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

---

## P0 口述骨架（考前必背）

**三连（40 秒）：**  
穿透：查不存在 → 空值/布隆；击穿：热点过期 → 互斥重建/逻辑过期；雪崩：大量同时过期 → TTL 随机 + HA + 限流。  
**分布式锁：** SET key value NX EX + 解锁 Lua 校验 value；可提 Redisson 看门狗。  
**双写：** Cache Aside 先 DB 再删缓存，接受短暂不一致。  
**易错：** 三连定义对调；锁只说 setnx 不说过期与误解锁。

**链：** [完整卷](./Redis高频面试题与知识点.md) · [面渣](./Redis面渣级口述.md) · [场景题](./场景题高频面试题与知识点.md)
