# Java · 卡片速记

<!-- NAV:START -->
> **只背要点。** 原理 → [知识点](./Java高频面试题与知识点.md) · 怎么说 → [面渣](./Java面渣级口述.md)
>
> [模块总览](./Java八股模块总览.md) · [如何使用](./如何使用本仓库.md)
>
<!-- NAV:END -->

> 遮住 A，只看 Q。

---

## 1. == 与 equals？
**A:** 基本比値/引用比地址；equals 默认同地址，可重写比内容。

## 2. 重写 equals 为何必须 hashCode？
**A:** 相等对象同 hash；否则 HashMap 存取失败。

## 3. String 三兄弟？
**A:** String 不可变；Builder 可变非安全；Buffer 可变且安全。

## 4. String 为何不可变？
**A:** final+无改API；池化、hash缓存、安全。

## 5. Integer 缓存？
**A:** -128~127；外用 equals。

## 6. 值传递？
**A:** 只有值传递；引用传的是副本。

## 7. 重载 vs 重写？
**A:** 参数不同编译期 / 子类覆盖运行期。

## 8. 抽象类 vs 接口？
**A:** 抽象类可有状态构造；接口多实现+default。

## 9. HashMap JDK8？
**A:** 数组+链+红黑树；≥8且表≥64树化；0.75；2的幂。

## 10. JDK7 vs 8 HashMap？
**A:** 7头插可能死链；8尾插+树。

## 11. CHM vs Hashtable？
**A:** 8用CAS+锁节点；HT全表锁；都不允许null。

## 12. ArrayList vs LinkedList？
**A:** 数组随机快 / 链表头尾插删。

## 13. HashSet 底层？
**A:** HashMap，value 固定对象。

## 14. 异常体系？
**A:** Error/Exception；检查 vs 运行时。

## 15. final/finally/finalize？
**A:** 修饰/必执行块/废弃的GC回调。

详解：[Java高频面试题与知识点.md](./Java高频面试题与知识点.md)
