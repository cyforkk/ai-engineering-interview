# MySQL · 卡片速记

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
