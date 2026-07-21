# Java 集合 · 卡片速记

<!-- NAV:START -->
> [完整知识点](./Java集合框架高频面试题与知识点.md) · [面渣](./Java面渣级口述.md) · [总览](./Java八股模块总览.md)
<!-- NAV:END -->

> 遮住 A。

---

**Q1 Collection vs Collections？**  
A: 接口 vs 工具类。

**Q2 List/Set/Map？**  
A: 有序可重复 / 不重复 / 键值对。

**Q3 ArrayList vs LinkedList？**  
A: 动态数组随机O(1) vs 双向链表；默认AL。

**Q4 ArrayList 扩容？**  
A: 默认10；约1.5倍。

**Q5 COW List？**  
A: 写时复制；读多写少。

**Q6 Fail-Fast？**  
A: modCount 不一致抛 CME。

**Q7 HashSet 不重复？**  
A: 底层HashMap，key唯一，value=PRESENT。

**Q8 HashMap JDK8 结构？**  
A: 数组+链+红黑树；尾插。

**Q9 树化条件？**  
A: 链≥8 且 表≥64。

**Q10 容量 2 的幂？**  
A: `(n-1)&hash` 快且均匀。

**Q11 阈值为何 8？**  
A: 泊松分布极端少；树优化极端碰撞。

**Q12 put 流程一句话？**  
A: hash→下标→空放/覆盖/链或树→树化或扩容。

**Q13 扰动？**  
A: 高低16位异或，减碰撞。

**Q14 HashMap vs Hashtable？**  
A: 非安全可null vs 全表锁禁null。

**Q15 CHM JDK7 vs 8？**  
A: 分段锁 vs CAS+锁头节点。

**Q16 CHM 为啥快？**  
A: 锁粒度细；读多无锁。

**Q17 LinkedHashMap？**  
A: 插入/访问序；可做LRU。

**Q18 TreeMap？**  
A: 红黑树有序。

**Q19 PriorityQueue？**  
A: 堆，默小顶堆。

**Q20 ArrayDeque？**  
A: 双端队列，常优于Stack。

**Q21 Comparable vs Comparator？**  
A: 自然序 vs 定制比较器。

**Q22 Fail-Safe？**  
A: COW/Concurrent 迭代不抛CME，弱一致。

**Q23 并发 Map 选型？**  
A: ConcurrentHashMap，别用Hashtable。

---

详解：[Java集合框架高频面试题与知识点.md](./Java集合框架高频面试题与知识点.md)

---

## P0 口述骨架（考前必背）

**HashMap put（30 秒）：**  
hash 扰动 → \(n-1)&hash\ 下标 → 空位放入 / key 相等覆盖 / 链或树插入 → 链长≥8 且 表长≥64 树化 → 超阈值 2 倍扩容重哈希。  
**易错：** 忘说线程不安全；树化只讲 8 不讲 64；扩容因子 0.75 说不清。

**CHM（20 秒）：**  
1.8 CAS + 同步头节点；读多无锁；禁止 null。  
**易错：** 只背分段锁不说 1.8。

**选型：** 局部 List 用 ArrayList；并发 Map 用 CHM；LRU 想 LinkedHashMap 或自研。

**链：** [完整卷](./Java集合框架高频面试题与知识点.md) · [面渣](./Java面渣级口述.md) · [结构图](./核心结构图.md)
