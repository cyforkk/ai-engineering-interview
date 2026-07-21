# -*- coding: utf-8 -*-
"""MySQL：按超高/高/中/低频完整卷 + 频率导航。不碰面渣。"""
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def w(name, text):
    p = DOCS / name
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print(name, p.stat().st_size)


NAV = """<!-- NAV:START -->
> 📖 **MySQL 完整卷** · 🗣️ [面渣](./MySQL面渣级口述.md) · 🃏 [卡片](./MySQL卡片速记.md) · 🔥 [频率导航](./MySQL八股频率排序.md)
>
> [四档主线](./Java后端面试频率-四档.md) · [Redis](./Redis高频面试题与知识点.md)
>
<!-- NAV:END -->
"""

MYSQL = f"""# MySQL · 高频八股知识点（完整卷）

{NAV}

> 后端面试出现频率极高。**索引 + 事务 + 锁 + MVCC 几乎必考。**  
> 建议：画图（B+、版本链、临键锁）+ 优化/死锁案例。

### 专项时间占比

| 优先级 | 模块 | 时间 |
|--------|------|:----:|
| **P0** | 索引（B+/最左/回表/失效）+ 事务 + MVCC + 锁 | **55%** |
| **P1** | redo/undo/binlog + Explain + 慢查询 | **20%** |
| **P2** | InnoDB vs MyISAM + 主从 + 分库分表基础 | **15%** |
| **P3** | Buffer Pool、大表变更、进阶 | **10%** |

### 高效准备

1. 索引/事务/锁/MVCC **能独立画图讲**  
2. 准备慢 SQL、深分页、死锁案例  
3. 追问链：失效 → 为何 → 怎么优 → 覆盖/回表代价  
4. 项目有读写分离/分库分表/优化 → 能展开  

---

# 一、超高频（几乎必问）

## 1. 索引（重中之重）

### 1.1 为什么用 B+ 树？对比？

| 结构 | 点查 | 范围 | 磁盘友好 |
|------|------|------|----------|
| 二叉树 | 差（太高） | 一般 | IO 多 |
| 哈希 | 极快 | **弱** | — |
| B 树 | 好 | 一般 | 较好 |
| **B+ 树** | 好 | **强**（叶子链表） | **矮胖**，非叶少存数据 |

- **为什么 B+**：非叶子主要存键与指针，分支因子大、树矮 → 少磁盘 IO；叶子有序链表适合 `BETWEEN`/`ORDER BY`。

### 1.2 聚簇索引 vs 二级索引？

| | 聚簇（主键） | 二级（非聚簇） |
|--|--------------|----------------|
| 叶子 | **整行数据** | **主键值** |
| 点查 | 直接拿行 | 常需 **回表** |

- InnoDB 表必须有聚簇索引（无主键会选唯一非空或隐藏 row_id）。

### 1.3 回表？覆盖索引？如何避免回表？

- **回表**：二级索引找到主键后，再回聚簇索引取完整行。  
- **覆盖索引**：查询列都在二级索引中，**Extra: Using index**，免回表。  
- **避免**：联合索引覆盖 SELECT 列；只查必要字段。  

### 1.4 最左前缀？举例

- 索引 `(a, b, c)` 按 a→b→c 排序。  
- 可用：`a`；`a,b`；`a,b,c`；`a,c` 可能只用到 a。  
- 通常不能：只有 `b` 或只有 `c`。  

### 1.5 索引失效常见场景？

1. 对索引列使用函数/表达式：`WHERE YEAR(ctime)=2024`  
2. 隐式类型转换：`varchar` 列与数字比较  
3. 左模糊：`LIKE '%xx'`  
4. 违反最左前缀  
5. `OR` 一侧无索引  
6. 不等于、`IS NOT NULL` 等部分情况优化器弃用  
7. 区分度极低、优化器认为全表更便宜  
→ **最终以 EXPLAIN 为准**

### 1.6 索引下推 ICP？

- Index Condition Pushdown：把部分 WHERE 条件下推到**引擎层**用索引过滤，减少回表次数（5.6+）。  
- Extra 可能见 `Using index condition`。

### 1.7 B+ 树能存多少？几层？

- 粗算：页 16KB，非叶存指针+键，层高 **2～4 层** 可支撑千万～亿级行量级（与键长、填充有关）。  
- 面试说：**矮，通常 3 层左右可扛大量数据**。

### 1.8 主键为何推荐自增而非 UUID？

| 自增 | UUID |
|------|------|
| 顺序插入，页分裂少 | 随机插入，页分裂多、碎片大 |
| 二级索引叶子更短 | 更长，二级索引膨胀 |

- 业务主键、分布式 ID（雪花）另论；InnoDB 更爱**顺序**聚簇键。

---

## 2. 事务

### 2.1 ACID 与机制？

| 特性 | 含义 | 主要机制（直觉） |
|------|------|------------------|
| A 原子 | 全成或全否 | undo 回滚 |
| C 一致 | 约束始终成立 | 业务+引擎约束 |
| I 隔离 | 并发互不干扰 | 锁 + MVCC |
| D 持久 | 提交不丢 | redo log（WAL） |

### 2.2 四种隔离级别？默认？

| 级别 | 脏读 | 不可重复读 | 幻读 |
|------|------|------------|------|
| 读未提交 RU | 可能 | 可能 | 可能 |
| 读已提交 RC | 否 | 可能 | 可能 |
| **可重复读 RR** | 否 | 否 | 可能* |
| 串行化 | 否 | 否 | 否 |

- **MySQL InnoDB 默认 RR**。  
- *RR 下 InnoDB 用 MVCC + 临键锁等尽量避免幻读。

### 2.3 脏读 / 不可重复读 / 幻读？

| 现象 | 含义 |
|------|------|
| 脏读 | 读到别人**未提交**的修改 |
| 不可重复读 | 同一事务两次读同一行，中间被**改** |
| 幻读 | 范围读行数变（**插入/删除**） |

### 2.4 MVCC 原理？

- **多版本**：行变更产生版本（undo 链）。  
- **ReadView**：当前事务能看见哪些版本。  
- 普通 SELECT **快照读**走 MVCC，一般不加锁。  

### 2.5 快照读 vs 当前读？

| | 快照读 | 当前读 |
|--|--------|--------|
| 语句 | 普通 SELECT | `SELECT ... FOR UPDATE` / `LOCK IN SHARE MODE`、更新删除 |
| 机制 | MVCC | 读最新 + **加锁** |

### 2.6 RR 下如何解决幻读？

- 快照读：MVCC 看到事务开启时的快照，新插入对快照不可见。  
- 当前读：用 **临键锁（Next-Key = 记录锁 + 间隙锁）** 锁住范围，阻止间隙插入。  

---

## 3. 锁

### 3.1 有哪些锁？

- 表锁、行锁、意向锁（IS/IX）  
- 记录锁 Record、间隙锁 Gap、临键锁 Next-Key  
- 插入意向锁等（了解）  

### 3.2 记录锁 / 间隙锁 / 临键锁？

| 锁 | 锁什么 | 作用 |
|----|--------|------|
| 记录锁 | 索引记录本身 | 防改该行 |
| 间隙锁 | 记录之间的间隙 | 防**间隙插入**（幻读） |
| 临键锁 | 记录 + 左边间隙 | RR 下范围当前读常见 |

### 3.3 何时间隙锁？

- RR 隔离级别下，当前读扫描范围时易对间隙加锁。  
- RC 下间隙锁很少（基本不用）。  

### 3.4 SELECT ... FOR UPDATE 加什么锁？

- **当前读**；对扫描到的索引记录加锁（常为临键/记录，视查询与隔离级别）。  
- 无合适索引可能锁更多行甚至表级倾向。  

### 3.5 死锁？排查避免？

- 原因：多事务交叉持锁等待成环。  
- 排查：`SHOW ENGINE INNODB STATUS`（LATERST DETECTED DEADLOCK）；应用日志。  
- InnoDB 会选代价小的一方 **回滚**。  
- 避免：固定访问顺序、缩短事务、合适索引减少锁范围、避免大事务。  

### 3.6 乐观锁 vs 悲观锁？

| | 悲观 | 乐观 |
|--|------|------|
| 思路 | 先锁再改（FOR UPDATE） | 版本号/CAS 更新 |
| 场景 | 冲突多 | 冲突少 |

---

## 4. 日志

### 4.1 redo / undo / binlog？

| 日志 | 层 | 作用 |
|------|-----|------|
| **redo log** | InnoDB | 崩溃恢复，保证持久 |
| **undo log** | InnoDB | 回滚 + MVCC 版本 |
| **binlog** | Server | 主从复制、时间点恢复 |

### 4.2 为什么两阶段提交？

- 事务提交要让 **redo 与 binlog 一致**，否则主从/恢复会对不齐。  
- 内部 prepare → 写 binlog → commit（简化理解两阶段思想）。  

### 4.3 WAL？

- Write-Ahead Logging：先写日志再落脏页，用顺序写换随机写，崩溃可重放。  

### 4.4 innodb_flush_log_at_trx_commit？

| 值 | 含义（简化） |
|----|----------------|
| **1** | 每事务刷盘（最安全，默认推荐生产） |
| 0 | 约每秒刷，宕机可能丢 1s |
| 2 | 写 OS 缓存，OS 刷盘；OS 挂可能丢 |

---

# 二、高频

## 5. 存储引擎

### InnoDB vs MyISAM

| | InnoDB | MyISAM |
|--|--------|--------|
| 事务 | ✓ | ✗ |
| 锁 | 行锁 | 表锁为主 |
| 外键 | ✓ | ✗ |
| 崩溃恢复 | 强（redo） | 弱 |
| 索引 | 聚簇 | 非聚簇为主 |
| 默认 | **是** | 历史 |

- **为何默认 InnoDB**：事务、并发行锁、崩溃安全是互联网标配。  

---

## 6. SQL 执行与优化

### 6.1 查询大致过程？

```text
连接器 → 查询缓存(8.0已移除) → 分析器 → 优化器 → 执行器 → 存储引擎
```

### 6.2 更新大致过程？

```text
执行器 → 引擎取数据 → 修改 → redo + undo
 → 事务提交：redo prepare → binlog → redo commit
 → 后台刷脏页
```

### 6.3 EXPLAIN 关键字段？

| 字段 | 看什么 |
|------|--------|
| type | 访问类型：system/const/eq_ref/ref/range/index/ALL… |
| possible_keys / key | 可能/实际索引 |
| rows | 估计扫描行 |
| Extra | Using index（覆盖）、Using filesort、Using temporary、Using index condition（ICP） |

- type 尽量别 ALL；rows 尽量小。  

### 6.4 慢查询如何优化？

1. 慢日志定位  
2. EXPLAIN  
3. 加合适索引 / 改写 SQL / 拆查询  
4. 避免 select *、函数包列  
5. 验证  

### 6.5 深分页？

- `LIMIT 1000000,10` 扫描大量再丢弃。  
- 优化：`WHERE id > last_id LIMIT 10`；或延迟关联（先索引查 id 再 join）。  

### 6.6 为何不推荐 SELECT *？

- 无法覆盖索引、传输放大、表结构变更易坏、难用到只读列优化。  

### 6.7 COUNT(*) / COUNT(1) / COUNT(列)？

- InnoDB：`COUNT(*)` 与 `COUNT(1)` 通常相当，要数行。  
- `COUNT(列)` **不计 NULL**。  
- 不要纠结 * 与 1 的玄学，以官方与版本实测为准。  

---

## 7. 其他高频

### 主从复制

```text
主库写 binlog → 从 IO 线程拉 binlog → relay log → SQL 线程重放
```

- binlog 格式：  
  - **STATEMENT**：记 SQL（省，不安全场景）  
  - **ROW**：记行变更（安全，日志大）  
  - **MIXED**：混合  

### 读写分离

- 写主读从；中间件/业务路由；注意**主从延迟**（读己之写、延迟敏感读主）。  

### 分库分表

| 策略 | 例 |
|------|-----|
| 垂直 | 按业务拆库拆表 |
| 水平 | hash/range 分片 |

- 问题：跨库事务、跨库 JOIN、全局 ID、扩容迁移。  

---

# 三、中频

## 8. Buffer Pool 与页

- **Buffer Pool**：缓存数据页与索引页，加速读写。  
- InnoDB 对 LRU 有优化（防全表扫污染，young/old 区域等）。  
- 默认页 **16KB**。  

## 9. 字符集

- **utf8mb4**：完整 Unicode（含 emoji）；旧 utf8 最多 3 字节。  
- 排序规则 collation 影响比较与排序。  

## 10. CHAR vs VARCHAR？

| CHAR | VARCHAR |
|------|---------|
| 定长 | 变长 + 长度前缀 |
| 适合固定短 | 适合变长 |

## 11. DELETE / TRUNCATE / DROP？

| | DELETE | TRUNCATE | DROP |
|--|--------|----------|------|
| 数据 | 可按行删，可回滚（事务内） | 整表清空更快 | 删表结构 |
| 日志 | 行级 | 较少 | — |

## 12. 大表加字段？

- 在线 DDL；MySQL 8 **INSTANT** 部分场景秒加。  
- 大表：`pt-online-schema-change` / gh-ost，影子表+触发器/行复制，控锁时间。  

## 13. 百万级删除？

- 分批 `DELETE ... LIMIT` + 睡眠；避免长事务、大 undo。  
- 或归档换表。  

## 14. 三大范式（简）

1NF 原子 → 2NF 完全依赖主键 → 3NF 消除传递依赖。  
业务可适度反范式换性能。  

## 15. 索引设计原则

- 高区分度列优先  
- 遵守最左  
- 覆盖常用查询  
- 控制索引数量（写放大）  
- 长字符串前缀索引权衡  

---

# 四、低频 / 进阶加分

- Redo 刷盘时机与 Checkpoint  
- Undo 版本链结构细节  
- ReadView 可见性判断细则  
- 半同步复制、并行复制  
- ShardingSphere 等中间件  
- 全局 ID：雪花、号段  
- 在线 DDL 风险  
- MySQL 8：降序索引、窗口函数、原子 DDL  

---

# 自测清单

### P0
- [ ] B+ 对比哈希/B 树  
- [ ] 聚簇/二级/回表/覆盖/最左/失效/ICP  
- [ ] ACID + 隔离级别 + 三种读现象  
- [ ] MVCC + 快照读/当前读  
- [ ] 记录/间隙/临键 + 死锁排查  

### P1
- [ ] 三日志 + 两阶段 + WAL  
- [ ] EXPLAIN 四字段 + 慢 SQL 四步 + 深分页  

### P2
- [ ] InnoDB 为何默认  
- [ ] 主从 + binlog 三格式  
- [ ] 分库分表痛点  

**口述：** [MySQL面渣级口述.md](./MySQL面渣级口述.md)  
**卡片：** [MySQL卡片速记.md](./MySQL卡片速记.md)  
**频率：** [MySQL八股频率排序.md](./MySQL八股频率排序.md)  

---

## 点名深挖

- B+ 画图  
- MVCC + ReadView  
- 临键锁与幻读  
- redo/binlog 两阶段  

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 按超高/高/中/低频大纲重写 MySQL 完整卷 |
"""

RANK = f"""# MySQL · 频率导航（2025–2026）

> **完整卷：** [MySQL高频面试题与知识点.md](./MySQL高频面试题与知识点.md)  
> **面渣：** [MySQL面渣级口述.md](./MySQL面渣级口述.md) · **卡片：** [MySQL卡片速记.md](./MySQL卡片速记.md)  
> **全库主线：** [四档 P0](./Java后端面试频率-四档.md)

---

## 专项时间

| 优先级 | 模块 | 时间 |
|--------|------|:----:|
| P0 | 索引 + 事务 + MVCC + 锁 | **55%** |
| P1 | 三日志 + Explain + 慢查询 | 20% |
| P2 | 引擎 + 主从 + 分库分表 | 15% |
| P3 | Buffer Pool、大表、进阶 | 10% |

---

## 一、超高频

| # | 主题 | 入口 |
|---|------|------|
| 1 | 索引（B+、聚簇、回表、覆盖、最左、失效、ICP、主键） | [§1](./MySQL高频面试题与知识点.md) |
| 2 | 事务 + MVCC + 快照/当前读 + 幻读 | [§2](./MySQL高频面试题与知识点.md) |
| 3 | 锁（记录/间隙/临键、FOR UPDATE、死锁） | [§3](./MySQL高频面试题与知识点.md) |
| 4 | redo/undo/binlog + 两阶段 + WAL | [§4](./MySQL高频面试题与知识点.md) |

---

## 二、高频

InnoDB vs MyISAM · SQL 执行过程 · Explain · 慢查询 · 深分页 · COUNT · 主从 · 读写分离 · 分库分表  

---

## 三、中频

Buffer Pool · 16KB 页 · utf8mb4 · CHAR/VARCHAR · DELETE/TRUNCATE · 大表 DDL · 范式  

---

## 四、低频加分

Checkpoint · ReadView 细节 · 半同步 · Sharding · 雪花 ID · MySQL 8 特性  

---

## 必须画图的三块

```text
1. B+ 树与回表
2. MVCC 版本链 + ReadView 直觉
3. 临键锁范围（防幻读）
```

## 追问链（索引）

```text
失效了？ → 为什么？ → 怎么改？ → 覆盖索引？ → 回表代价？
```

---

## 点名

`B+画图` · `MVCC` · `临键锁` · `两阶段提交` · `深分页`

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | MySQL 专项频率导航 |
"""

CARDS = f"""# MySQL · 卡片速记

<!-- NAV:START -->
> [完整卷](./MySQL高频面试题与知识点.md) · [频率](./MySQL八股频率排序.md) · [面渣](./MySQL面渣级口述.md)
<!-- NAV:END -->

> 遮住 A。**先 P0。**

---

## 索引

**Q1 为何 B+？** A: 矮胖少IO；叶子链表利范围。

**Q2 聚簇 vs 二级？** A: 叶子整行 vs 主键；二级常回表。

**Q3 覆盖索引？** A: 查询列都在索引，免回表。

**Q4 最左？** A: (a,b,c) 从左连续用。

**Q5 失效？** A: 函数、左模糊、隐式转换、违背最左。

**Q6 ICP？** A: 条件下推引擎，少回表。

**Q7 主键自增？** A: 顺序插，减页分裂。

## 事务 / MVCC

**Q8 默认隔离？** A: RR。

**Q9 脏读/不可重复/幻读？** A: 未提交/行被改/范围行数变。

**Q10 MVCC？** A: undo版本链+ReadView。

**Q11 快照读 vs 当前读？** A: 普通SELECT vs FOR UPDATE等。

**Q12 RR 防幻读？** A: MVCC + 临键锁（当前读）。

## 锁

**Q13 三种行级？** A: 记录锁、间隙锁、临键锁。

**Q14 间隙锁？** A: 锁间隙防插入；RR 当前读常见。

**Q15 FOR UPDATE？** A: 当前读加锁。

**Q16 死锁排查？** A: SHOW ENGINE INNODB STATUS。

## 日志

**Q17 三日志？** A: redo持久；undo回滚MVCC；binlog复制。

**Q18 两阶段？** A: redo与binlog一致。

**Q19 WAL？** A: 先日志后数据页。

**Q20 flush=1？** A: 每事务刷盘最安全。

## 高频

**Q21 InnoDB？** A: 事务+行锁；现代默认。

**Q22 EXPLAIN？** A: type/key/rows/Extra。

**Q23 慢SQL？** A: 慢日志→EXPLAIN→改→验证。

**Q24 深分页？** A: id>last 或延迟关联。

**Q25 主从？** A: binlog→relay→重放。

**Q26 binlog格式？** A: STATEMENT/ROW/MIXED。

---

详解：[MySQL高频面试题与知识点.md](./MySQL高频面试题与知识点.md)
"""


def patch():
    ft = DOCS / "Java后端面试频率-四档.md"
    if ft.exists():
        t = ft.read_text(encoding="utf-8")
        if "MySQL八股频率排序" not in t:
            t = t.replace(
                "🗣️ [MySQL面渣](./MySQL面渣级口述.md) · 🃏 [MySQL卡](./MySQL卡片速记.md)",
                "🗣️ [MySQL面渣](./MySQL面渣级口述.md) · 🃏 [MySQL卡](./MySQL卡片速记.md) · 🔥 [MySQL频率](./MySQL八股频率排序.md)",
            )
            ft.write_text(t, encoding="utf-8")
            print("fourtier")

    sb = DOCS / "_sidebar.md"
    if sb.exists():
        t = sb.read_text(encoding="utf-8")
        if "MySQL八股频率排序" not in t:
            t = t.replace(
                "  * [MySQL完整卷](MySQL高频面试题与知识点.md) · [卡片](MySQL卡片速记.md)\n",
                "  * [MySQL完整卷](MySQL高频面试题与知识点.md) · [频率](MySQL八股频率排序.md) · [卡片](MySQL卡片速记.md)\n",
            )
            t = t.replace(
                "  * [MySQL](MySQL高频面试题与知识点.md) · [卡片](MySQL卡片速记.md)\n",
                "  * [MySQL完整卷](MySQL高频面试题与知识点.md) · [频率](MySQL八股频率排序.md) · [卡片](MySQL卡片速记.md)\n",
            )
            sb.write_text(t, encoding="utf-8")
            print("sidebar")

    path = DOCS / "路径-Java后端.md"
    if path.exists():
        t = path.read_text(encoding="utf-8")
        if "MySQL八股频率排序" not in t:
            t = t.replace(
                "[MySQL八股](./MySQL高频面试题与知识点.md)",
                "[MySQL完整卷](./MySQL高频面试题与知识点.md)·[频率](./MySQL八股频率排序.md)",
            )
            path.write_text(t, encoding="utf-8")
            print("path")


def main():
    w("MySQL高频面试题与知识点.md", MYSQL)
    w("MySQL八股频率排序.md", RANK)
    w("MySQL卡片速记.md", CARDS)
    patch()


if __name__ == "__main__":
    main()
