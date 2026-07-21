# Redis · 卡片速记

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
