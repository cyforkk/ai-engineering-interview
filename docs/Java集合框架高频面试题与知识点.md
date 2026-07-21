# Java 集合框架 · 高频八股知识点（完整卷）

<!-- NAV:START -->
> 📖 **集合框架八股** · 🗣️ [Java面渣](./Java面渣级口述.md) · 🃏 [集合卡片](./Java集合卡片速记.md)
>
> [模块总览](./Java八股模块总览.md) · [Java基础](./Java高频面试题与知识点.md) · [并发](./并发高频面试题与知识点.md)
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md) · [路径](./路径-Java后端.md)
>
<!-- NAV:END -->

> 结构图：[HashMap](./核心结构图.md#1-hashmapjdk8)



> 集合是面试 **出现频率最高** 模块之一；**HashMap / ConcurrentHashMap** 几乎每场必问。  
> 格式：题目 + 核心知识点；强调对比、JDK7/8 差异、场景。

### 面试回答建议

1. HashMap 能 **画结构图**，完整说 put / get / 扩容  
2. 主动对比 **JDK 1.7 vs 1.8**  
3. 线程安全优先推 **ConcurrentHashMap** 并说明原因  
4. 能提关键字段：`table`、`size`、`threshold`、`loadFactor`、`modCount` 更加分  

---

# 一、集合框架整体结构

## 1. 核心接口体系？

```text
Iterable
 └── Collection（单列）
      ├── List   有序、可重复
      ├── Set    不可重复（通常无序，实现类有序变体）
      └── Queue / Deque  队列 / 双端队列

Map（双列，键值对，键唯一）—— 不继承 Collection
```

---

## 2. Collection 和 Collections 的区别？

| | Collection | Collections |
|--|------------|-------------|
| 类型 | **接口** | **工具类** |
| 作用 | 集合根接口之一 | 排序、同步包装、查找、不可变集合等静态方法 |

---

## 3. List、Set、Map 的区别？

| | List | Set | Map |
|--|------|-----|-----|
| 结构 | 有序序列 | 不重复集合 | 键值对 |
| 重复 | 可重复 | 不可重复 | 键唯一，值可重复 |
| 典型 | ArrayList | HashSet | HashMap |

---

# 二、List 相关

## 4. ArrayList vs LinkedList？（必考对比）

| 对比项 | ArrayList | LinkedList |
|--------|-----------|------------|
| 底层 | **动态数组** | **双向链表** |
| 随机访问 | **O(1)** | O(n) |
| 插入/删除 | 中间 **O(n)**（搬移） | 已知节点时 O(1)；查找节点仍 O(n) |
| 内存 | 较少（连续） | 较多（前后指针） |
| 场景 | **查询多、增删少**（默认首选） | 头尾频繁插删、队列场景等 |

---

## 5. ArrayList 默认容量与扩容？

- 无参构造：默认容量 **10**（JDK8：首次 add 时才分配到 10，懒加载）。  
- 扩容：约为原来的 **1.5 倍**（`old + (old >> 1)`）。  
- 扩容要 **数组拷贝**，频繁扩容有成本 → 可知大小时指定初始容量。

---

## 6. Vector？为何少用？

- 方法多 `synchronized`，**线程安全但粗粒度**，性能差。  
- 扩容通常 2 倍（与 ArrayList 不同）。  
- 现代用 **CopyOnWriteArrayList** 或外部同步 / 并发集合替代。

---

## 7. CopyOnWriteArrayList？

- **写时复制**：写操作复制新数组，改完替换引用。  
- **读几乎无锁**，适合 **读多写少**。  
- 写贵、内存占用高；迭代为快照，弱一致。  
- 属于 **Fail-Safe** 一类思路。

---

## 8. Fail-Fast 机制？

- 用 Iterator 遍历时，若集合结构被**其他方式**修改 → 可能 `ConcurrentModificationException`。  
- 原理：`modCount` 与迭代器 `expectedModCount` 不一致。  
- 迭代器自己的 `remove` 会同步 expected，一般安全。

---

# 三、Set 相关

## 9. HashSet / LinkedHashSet / TreeSet？

| 实现 | 底层 | 特点 | 顺序 |
|------|------|------|------|
| HashSet | **HashMap** | 允许一个 null | 无序 |
| LinkedHashSet | LinkedHashMap | 保留插入顺序 | 插入有序 |
| TreeSet | TreeMap（红黑树） | 自然序/Comparator | 排序有序 |

---

## 10. HashSet 如何保证不重复？添加流程？

- 元素作 HashMap 的 **key**，value 为固定 `PRESENT`。  
- 靠 key 的 **hashCode + equals** 判重。  

**添加流程（同 HashMap put key）：**

1. 算 hash  
2. 定位桶  
3. 桶内 equals 比较  
4. 不存在则放入  

---

# 四、Map 相关（最核心）

## 11. HashMap 底层结构？（必画图口述）

### JDK 1.7

- 数组 + 链表  
- **头插法**  
- 多线程扩容可能 **环形链表死循环**（历史考点）

### JDK 1.8+

- **数组 + 链表 + 红黑树**  
- **尾插法**  
- 树化：链表长度 **≥ 8** 且数组长度 **≥ 64**  
- 退化：树节点过少（≤ 6）转回链表  

### 关键字段（加分）

| 字段 | 含义 |
|------|------|
| table | Node 数组 |
| size | 键值对数量 |
| threshold | 扩容阈值 ≈ capacity × loadFactor |
| loadFactor | 负载因子，默认 **0.75** |
| modCount | 结构修改次数（fail-fast） |

### 默认值

- 容量 **16**，负载因子 **0.75**，扩容 **2 倍**。

---

## 12. HashMap put 流程？（必须完整说）

1. 若 table 空 → 首次 resize 初始化  
2. 计算 key 的 **hash**（扰动）  
3. 下标：`hash & (n - 1)`  
4. 桶为空 → 新节点放入  
5. 桶头 key 的 hash 相同且 equals → **覆盖 value**  
6. 若为树节点 → 树插入  
7. 若为链表 → 遍历；存在则覆盖，否则尾插；插后若链长 ≥8 → 尝试 **treeifyBin**（数组 <64 则优先扩容）  
8. size 超过 threshold → **resize 扩容**  
9. 返回旧 value 或 null  

### get 流程（简）

hash → 下标 → 头结点匹配 / 树查找 / 链遍历 equals。

---

## 13. 为什么容量必须是 2 的幂次？

- 用 **`hash & (n-1)`** 代替 `hash % n`，更快。  
- 在 2 的幂下与取模等价，分布更均匀。  
- 扩容时元素位置：原下标 或 **原下标 + 旧容量**（高位决定）。

---

## 14. 为什么链表转红黑树阈值是 8？

- 理想扰动下，桶内链长服从类似泊松分布；  
- 负载因子 0.75 时，长度到 8 的概率 **极低**。  
- 树化优化 **极端碰撞** 下查询（O(log n)）。  
- 阈值太小则频繁树化，空浪费（树节点比链表节点大）。  
- 还要求 **table 长度 ≥64**，太短优先 **扩容摊平** 而非树化。

---

## 15. 扩容机制？JDK7/8 差异？

- **阈值** = 容量 × 负载因子（0.75）。  
- 扩容为 **2 倍**，rehash 搬迁。  
- **JDK7 头插**：多线程扩容可能死链。  
- **JDK8 尾插** + 优化拆分：节点要么在原索引，要么在 `index + oldCap`。  

---

## 16. hash 为什么要扰动？

- `hash ^ (hash >>> 16)`：高 16 位与低 16 位异或。  
- 让高位参与运算，**减少碰撞**（尤其容量较小时只看低位）。

---

## 17. HashMap vs Hashtable？

| 对比 | HashMap | Hashtable |
|------|---------|-----------|
| 线程安全 | 否 | 是（方法 synchronized，粗） |
| null | 允许一个 null key、多个 null value | 不允许 null |
| 继承 | AbstractMap | Dictionary（遗留） |
| 性能 | 高 | 低 |
| 初始容量 | 16 | 11（历史） |
| 现代选型 | 单线程用 HashMap | 基本不用，改 CHM |

---

## 18. ConcurrentHashMap？（并发必问）

### JDK 版本差异（超级高频）

| 版本 | 实现 | 锁粒度 |
|------|------|--------|
| **JDK 1.7** | Segment 分段锁 + HashEntry | 段（默认 16） |
| **JDK 1.8** | Node 数组 + **CAS** + **synchronized** | 锁链表/树的 **头节点** |

### JDK 1.8 核心原理

- 初始化、部分更新用 **CAS**。  
- 冲突时 **synchronized 锁桶头**，粒度细于全表锁。  
- 读：节点 val、链表多用 **volatile**，读路径基本无锁。  
- 仍 **不允许 null key/value**（二义性：没有 vs 值为 null）。  
- **size**：`baseCount + CounterCell`（类似 LongAdder 分段累加）。  
- 性能通常远优于 Hashtable。

### 何时用

- 并发 map → **ConcurrentHashMap**  
- 非并发 → HashMap  
- 不要用 Hashtable  

---

## 19. 其他 Map？

| 类 | 要点 |
|----|------|
| LinkedHashMap | 插入序或访问序；可实现 **LRU**（重写 removeEldestEntry） |
| TreeMap | 红黑树，按 key 排序（Comparable/Comparator） |
| WeakHashMap | 键弱引用，适合特定缓存场景（键不强引用时易被回收） |

---

# 五、Queue / Deque

## 20. PriorityQueue？

- 基于 **堆**，默认 **小顶堆**。  
- 元素需可比（Comparable/Comparator）。  
- **非线程安全**；并发用 PriorityBlockingQueue。

---

## 21. ArrayDeque？

- 可作双端队列、栈。  
- 通常比 `Stack`（继承 Vector）更合适；很多场景也优于 LinkedList 作队列。  
- **非线程安全**。

---

## 22. BlockingQueue（JUC）？

| 类 | 特点 |
|----|------|
| ArrayBlockingQueue | 有界数组 |
| LinkedBlockingQueue | 链表，可选有界（默认可选大容量） |
| SynchronousQueue | 不存储元素，直接交接 |
| DelayQueue | 延迟获取 |
| PriorityBlockingQueue | 无界优先级 |

- 用于线程池工作队列、生产者消费者模型。

---

# 六、其他高频点

## 23. Comparable vs Comparator？

| | Comparable | Comparator |
|--|------------|------------|
| 定义位置 | 元素自身 `compareTo` | 独立比较器 |
| 排序 | 自然排序 | 定制排序（策略） |
| 例 | Integer、String | 外部传入 TreeMap/sort |

---

## 24. 遍历方式？

- for-each（本质 Iterator）  
- Iterator / ListIterator（可双向、可改 List）  
- 下标 for（仅 List/数组）  
- Stream（JDK8+）  

注意：遍历中结构性修改要遵守 fail-fast 规则。

---

## 25. 如何让集合线程安全？

1. `Collections.synchronizedList/Map/...`（粗粒度，整集合锁）  
2. **JUC 并发集合（推荐）**  
   - ConcurrentHashMap  
   - CopyOnWriteArrayList  
   - BlockingQueue 等  
3. 外部手动加锁（少用，易漏）

---

## 26. Fail-Fast vs Fail-Safe？

| | Fail-Fast | Fail-Safe |
|--|-----------|-----------|
| 代表 | ArrayList、HashMap 迭代器 | CopyOnWrite、多数 Concurrent 迭代 |
| 行为 | 结构被改可能 CME | 不抛 CME，可能弱一致快照 |
| 原理 | modCount | 拷贝 / 并发容器机制 |

---

# 七、选型速查

| 需求 | 推荐 |
|------|------|
| 列表默认 | ArrayList |
| 读多写少列表并发 | CopyOnWriteArrayList |
| KV 单线程 | HashMap |
| KV 并发 | ConcurrentHashMap |
| 去重 | HashSet |
| 插入顺序去重 | LinkedHashSet |
| 排序 KV | TreeMap |
| LRU | LinkedHashMap |
| 阻塞队列 | ArrayBlockingQueue / LinkedBlockingQueue 等 |

---

# 自测清单

- [ ] Collection vs Collections；List/Set/Map  
- [ ] ArrayList 扩容 1.5；与 LinkedList 对比表  
- [ ] HashSet 不重复原理  
- [ ] HashMap 结构图 + put 全流程  
- [ ] 2 的幂、阈值 8、扰动、扩容  
- [ ] HashMap vs Hashtable  
- [ ] CHM 7 分段 vs 8 CAS+synchronized  
- [ ] Fail-Fast vs Fail-Safe  
- [ ] 线程安全集合选型  

**口述（含 HashMap 长答）：** [Java面渣级口述.md](./Java面渣级口述.md)  
**基础卷：** [Java高频面试题与知识点.md](./Java高频面试题与知识点.md)  
**并发：** [并发高频面试题与知识点.md](./并发高频面试题与知识点.md)  

---

## 可继续深挖（点名即可）

- HashMap put **源码级逐步对照**  
- ConcurrentHashMap JDK8 **源码级**  
- 红黑树转换条件与树化细节  
- ArrayList **ensureCapacity 扩容源码**  

---

---

## 版本与假设

| 项 | 说明 |
|----|------|
| 复核 | 2026-07 |
| 默认假设 | JDK 8+ HashMap/CHM 结构；树化等 8+ 行为 |
| 维护 | 正文以本完整卷为 SSOT；频率页/精简页不重复堆考点 |

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 集合框架完整卷：结构/List/Set/Map/Queue/对比 |
