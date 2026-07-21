# Java 基础 · 知识点

<!-- NAV:START -->
> 📖 **知识点（笔记体）** · 🗣️ [面渣练嘴](./Java面渣级口述.md) · 🃏 [卡片](./Java卡片速记.md)
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md) · [路径](./路径-Java后端.md)
>
<!-- NAV:END -->


> 笔记体：题号 + 分层要点。要完整口述 → [面渣](./Java面渣级口述.md)；速记 → [卡片](./Java卡片速记.md)。

---

## 1. == 和 equals() 的区别？

- **==**
  - 基本数据类型：比较**值**。
  - 引用数据类型：比较**内存地址**（是不是同一个对象）。
- **equals()**
  - 默认（`Object`）：等价于 `==`，比较地址。
  - 重写后（如 `String`、`Integer`）：比较**内容**。

---

## 2. 为什么重写 equals() 必须重写 hashCode()？（必考）

- **约定**：两个对象 `equals` 为 true，它们的 `hashCode` **必须**相等。
- **原因**：`HashMap` / `HashSet` 先按 `hashCode` 找桶，再在桶里用 `equals` 比 key。
- **后果**：只重写 `equals` 不重写 `hashCode` → 逻辑上相等的对象进不同桶 → **put 进去 get 不出来**。
- **反向**：`hashCode` 相同 **不代表** `equals` 一定为 true（允许碰撞）。

---

## 3. String、StringBuffer、StringBuilder 的区别？

- **String**
  - 不可变（`final` 类 + 内部数组不可对外改）。
  - 线程安全（状态不可变）。
  - 修改会生成新对象；常量池可共享。
- **StringBuilder**
  - 可变；**线程不安全**；单线程拼接**效率最高**。
- **StringBuffer**
  - 可变；方法带 `synchronized`，**线程安全**；效率较低。
- **选型**：单线程拼接用 `StringBuilder`；需要同步再用 `StringBuffer`（现代代码少用）。

---

## 4. 自动装箱与拆箱？Integer 的缓存机制？

- **装箱**：基本类型 → 包装类（如 `Integer.valueOf(i)`）。
- **拆箱**：包装类 → 基本类型（如 `intValue()`）。
- **Integer 缓存**（默认 **-128～127**）
  - 该区间 `valueOf` 复用缓存对象。
  - `Integer a = 100; Integer b = 100;` → `a == b` 为 **true**（同一缓存对象）。
  - `Integer a = 200; Integer b = 200;` → `a == b` 为 **false**（不同对象）；比内容用 `equals`。
- **注意**：`new Integer(100)` 不走缓存；业务比较包装类内容优先 `equals`。

---

## 5. HashMap 底层结构？（必考）

- **JDK 8**：数组 + 链表 + 红黑树。
- **默认**：容量 16，负载因子 0.75，扩容为 2 倍。
- **树化**：某桶链表长度 ≥ 8 **且** 数组长度 ≥ 64 → 红黑树；树节点 ≤ 6 可退回链表。
- **下标**：容量为 2 的幂时，用 `(n - 1) & hash` 代替取模。
- **线程安全**：否；并发用 `ConcurrentHashMap`。

---

## 6. HashMap 的 put 流程？

1. 计算 key 的 hash（扰动）。
2. 算数组下标。
3. 桶为空 → 直接放入。
4. 桶头 key 的 hash 与 equals 相同 → 覆盖 value。
5. 否则沿链表/树查找；没有则追加。
6. 链长达到阈值且表够长 → 树化。
7. 元素数超过 `容量 × 负载因子` → 扩容 rehash。

---

## 7. HashMap 为什么线程不安全？ConcurrentHashMap？

- **HashMap**：多线程 put 可能丢数据、死循环（历史版本）等，结构非并发设计。
- **ConcurrentHashMap（JDK 8）**：CAS + `synchronized` 锁桶头节点等，读多写少场景常用；不锁整张表。

---

## 8. ArrayList 和 LinkedList？

- **ArrayList**：动态数组；随机访问 O(1)；尾部追加均摊 O(1)；中间插入/删除要搬移。
- **LinkedList**：双向链表；头尾插入删除快；随机访问慢。
- **实践**：绝大多数场景 `ArrayList`；小数据量中间插入也不一定 LinkedList 更快。

---

## 9. fail-fast 是什么？

- 用迭代器遍历时，若集合结构被**其他方式**修改，可能抛 `ConcurrentModificationException`。
- 目的：尽早暴露错误修改；并发容器迭代语义通常是弱一致，不保证同样 CME。

---

## 10. final、finally、finalize？

- **final**：类不可继承 / 方法不可重写 / 变量不可重新赋值（引用不可变，不代表对象内容不可变）。
- **finally**：`try` 后几乎总执行的块（用于释放资源）；注意 `System.exit` 等极端情况。
- **finalize**：对象被 GC 前调用（已不推荐，别依赖）。

---

## 11. 深拷贝 vs 浅拷贝？

- **浅拷贝**：只复制外层对象，内部引用仍指向同一对象。
- **深拷贝**：递归复制内部对象，互不影响。

---

## 自测

- [ ] equals / hashCode 契约 + HashMap 后果  
- [ ] String 三兄弟选型  
- [ ] Integer 缓存区间与 `==`  
- [ ] HashMap 结构 + put + 树化条件  

**口述：** [Java面渣级口述.md](./Java面渣级口述.md) · **卡片：** [Java卡片速记.md](./Java卡片速记.md)
