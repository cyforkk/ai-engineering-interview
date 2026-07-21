# MySQL · 卡片速记

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
