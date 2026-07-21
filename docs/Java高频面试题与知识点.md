# Java 基础 + 集合 · 高频八股知识点

<!-- NAV:START -->
> 📖 **八股知识点** · 🗣️ [面渣](./Java面渣级口述.md) · 🃏 [卡片](./Java卡片速记.md)
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md) · [Java路径](./路径-Java后端.md) · [模块总览](./Java八股模块总览.md)
>
<!-- NAV:END -->


> 覆盖 P5–P7 基础与集合主考点。风格：**题目 + 核心要点**。完整口语 → 面渣。

---

# 一、Java 基础（必考）

## 1. == 与 equals 的区别？

| | == | equals |
|--|-----|--------|
| 基本类型 | 比较**值** | — |
| 引用类型 | 比较**内存地址** | 默认（Object）也比地址；重写后可比**内容**（String/Integer） |

---

## 2. 为什么重写 equals 必须重写 hashCode？（必考）

- **约定**：equals 为 true ⇒ hashCode **必须**相同。
- **原因**：HashMap/HashSet 先 hash 定位桶，再 equals 比 key。
- **后果**：hash 不同 → 进不同桶 → **存进去取不出**。
- hash 相同 **不** ⇒ equals 一定 true（允许碰撞）。

---

## 3. String / StringBuilder / StringBuffer？

| | 可变 | 线程安全 | 场景 |
|--|------|----------|------|
| String | 否 | 是（不可变） | 常量、少量拼接 |
| StringBuilder | 是 | 否 | 单线程拼接（首选） |
| StringBuffer | 是 | 是（synchronized） | 历史多线程拼接，现代少用 |

---

## 4. String 为什么不可变？

- 类 final；底层 `char[]`（JDK9+ 多为 `byte[]` + coder）；无对外修改内容的 API。
- **好处**
  - 常量池共享安全。
  - hashCode 可缓存（适合做 HashMap key）。
  - 天然线程安全、防篡改（类名、路径、密钥参数等）。

---

## 5. final / finally / finalize？

- **final**：类不可继承；方法不可重写；变量不可重新赋值（引用 final ≠ 对象内容不可变）。
- **finally**：try 后通常必执行（释放资源）；`System.exit` 等极端情况除外。
- **finalize**：GC 前调用，**已不推荐/废弃**，别依赖。

---

## 6. 面向对象三大特性？（+ 抽象）

- **封装**：隐藏细节，暴露接口。
- **继承**：复用、is-a。
- **多态**：同一引用不同实现（编译看父，运行看子——虚方法）。
- 常把 **抽象** 并列为第四特性。

---

## 7. 重载 vs 重写？

| | 重载 overload | 重写 override |
|--|---------------|---------------|
| 范围 | 同类（或继承可见） | 子类覆盖父类 |
| 规则 | 同名，**参数列表不同** | 方法签名相同（返回值协变等规则） |
| 绑定 | **编译期** | **运行时**多态 |

---

## 8. 抽象类 vs 接口？

| | 抽象类 | 接口 |
|--|--------|------|
| 构造 | 可有 | 无实例构造（不能 new 接口） |
| 成员变量 | 可有普通成员 | 多为常量（public static final） |
| 方法 | 可抽象可实现 | JDK8+：default / static / private 方法 |
| 多继承 | 单继承类 | 可实现多接口 |
| 设计 | is-a 模板 | can-do 能力 |

---

## 9. Integer 缓存？装箱拆箱？

- **装箱**：基本 → 包装（`Integer.valueOf`）。
- **拆箱**：包装 → 基本（`intValue`）。
- **缓存**：默认 **-128～127**；区间内 `==` 可能 true；区间外 false。
- 比内容用 `equals`；`new Integer(100)` 不走缓存。

---

## 10. 异常体系？

```text
Throwable
├── Error          （严重，一般不捕获：OOM、StackOverflow）
└── Exception
    ├── RuntimeException 及子类  → 非检查异常（可不声明）
    └── 其他 Exception           → 检查异常（需处理或声明）
```

- 检查异常：编译期强制处理（IOException 等）。
- 运行时异常：NPE、IllegalArgument 等。

---

## 11. Java 是值传递还是引用传递？

- **只有值传递**。
- 传引用类型时：传递的是**引用的副本**（地址值的拷贝）。
- 方法内改「副本指向」不影响外部引用；通过副本调用方法改对象内部状态，外部可见。

---

## 12. 常见补充（加分）

- **== 与 equals 对包装类**：缓存区间内外表现不同。
- **String intern**：尝试返回池中引用。
- **深拷贝 / 浅拷贝**：浅拷贝共享内部引用；深拷贝递归复制。

---

# 二、集合框架（超级高频）

## 13. HashMap 底层？（必考，分版本）

### JDK 1.7

- 数组 + 链表。
- 头插法；多线程扩容可能**死循环**（历史考点）。

### JDK 1.8+

- 数组 + 链表 + **红黑树**。
- **尾插**；树化条件：链长 **≥8** 且数组长度 **≥64**；树节点过少（≤6）退化链表。
- 默认容量 **16**，负载因子 **0.75**，扩容 **2 倍**。
- hash 扰动：高低位异或，减少碰撞。
- 容量 **2 的幂**：`(n-1) & hash` 代替取模。

### put 要点

1. hash → 下标  
2. 空桶直接放 / 相等覆盖 / 链或树插入  
3. 可能树化、扩容  

### get 要点

hash → 下标 → 链/树用 equals 找 key。

### 线程安全

- HashMap **否**。
- 并发用 ConcurrentHashMap。

---

## 14. ArrayList vs LinkedList？

| | ArrayList | LinkedList |
|--|-----------|------------|
| 结构 | 动态数组 | 双向链表 |
| 随机访问 | O(1) | O(n) |
| 头尾插删 | 尾部均摊 O(1)；中间要搬移 | 头尾 O(1) |
| 实践 | **默认首选** | 特定链表算法场景 |

---

## 15. HashMap vs Hashtable vs ConcurrentHashMap？

| | 线程安全 | 锁粒度 | null |
|--|----------|--------|------|
| HashMap | 否 | — | key/value 可 null（一个 null key） |
| Hashtable | 是 | 基本全表 synchronized | 不允许 null |
| ConcurrentHashMap | 是 | JDK7 分段锁；**JDK8 CAS + synchronized 锁桶头节点** | 不允许 null |

### ConcurrentHashMap 为何相对高效？

- 不锁整表；JDK8 按节点/桶同步 + CAS 初始化。
- 读多写少场景吞吐通常优于 Hashtable。

---

## 16. HashSet / TreeMap？

- **HashSet**：底层 HashMap，value 为固定 PRESENT 对象；靠 key 去重。
- **TreeMap**：红黑树，**有序**（Comparable / Comparator）；操作 O(log n)。

---

## 17. fail-fast / fail-safe？

- fail-fast：迭代时结构被改可能 CME（ArrayList 等）。
- 并发容器迭代多为弱一致，不保证强 fail-fast。

---

## 18. 集合选用速记

| 需求 | 选择 |
|------|------|
| 列表随机访问 | ArrayList |
| KV 缓存（单线程） | HashMap |
| KV 并发 | ConcurrentHashMap |
| 去重无序 | HashSet |
| 有序 KV | TreeMap / LinkedHashMap |

---

# 自测清单

- [ ] equals/hashCode + Integer 缓存  
- [ ] String 三兄弟 + 不可变原因  
- [ ] 值传递一句话  
- [ ] HashMap 7/8 差异 + 树化 + 2 的幂  
- [ ] CHM 与 Hashtable 区别  

**口述：** [Java面渣级口述.md](./Java面渣级口述.md) · **卡片：** [Java卡片速记.md](./Java卡片速记.md)  
**下一模块：** [并发](./并发高频面试题与知识点.md)
