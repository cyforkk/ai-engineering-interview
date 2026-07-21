# Java · 卡片速记

<!-- NAV:START -->
> **只背要点。** 原理 → [详解](./Java高频面试题与知识点.md) · 怎么说 → [面渣](./Java面渣级口述.md)
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md) · [路径](./路径-Java后端.md)
>
<!-- NAV:END -->

> 用法：遮住 **A**，只看 **Q** 回忆；卡壳回详解。

---

## 1. == 和 equals 区别？

**A:** 基本类型/引用地址 vs 可重写的内容相等；默认 equals≈==。

## 2. equals 与 hashCode 契约？

**A:** equals 为 true ⇒ hashCode 必须相同；否则 HashMap 找错桶。

## 3. String 为何不可变？

**A:** 池化共享、hash 可缓存、线程安全/防篡改；拼接用 StringBuilder。

## 4. HashMap 结构？

**A:** 数组 + 链表/红黑树；JDK8。

## 5. put 流程要点？

**A:** hash→下标→空则放/equals 覆盖/链追加→可能树化扩容。

## 6. 树化条件？

**A:** 链长≥8 且 表长≥64；≤6 退化链表。

## 7. 为何容量 2 的幂？

**A:** (n-1)&hash 代替取模，分布均匀且快。

## 8. HashMap 线程安全？

**A:** 否；并发用 ConcurrentHashMap。

## 9. ArrayList vs LinkedList？

**A:** 随机访问数组优；中间插删链表理论优，实际小数据 ArrayList 常更快。

## 10. fail-fast？

**A:** 迭代时结构被改抛 CME；并发容器弱一致迭代。

---


## 11. Integer 缓存？

**A:** 默认 -128～127；区间内 a==b 可能 true；区间外 false，比内容用 equals。

## 12. 装箱拆箱？

**A:** 基本↔包装；valueOf/intValue；比较内容用 equals。

详解：[Java高频面试题与知识点.md](./Java高频面试题与知识点.md) · 面渣：[Java面渣级口述.md](./Java面渣级口述.md)
