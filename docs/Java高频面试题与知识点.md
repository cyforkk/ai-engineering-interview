# Java 基础 + 集合 · 高频面试

> **专题序：1 / 权重 P0（全级别必问）**  
> 主线：`equals/hashCode` → `String` → **HashMap** → ArrayList/CHM  
> **面渣级长口述：** [Java面渣级口述.md](./Java面渣级口述.md)  
> 索引：[README.md](./README.md)

---

## 一、优先级总览

| 级 | 模块 | 面试频率 | 建议 |
|----|------|----------|------|
| **P0** | equals/hashCode、String、HashMap | 极高 | 必须口述流畅 |
| **P0** | ArrayList、值传递、异常 | 高 | 必须会 |
| **P1** | ConcurrentHashMap、LinkedHashMap/LRU、fail-fast | 高 | 社招必会 |
| **P1** | 重写重载、抽象类接口、Integer 缓存 | 中高 | 校招重点 |
| **P2** | 泛型擦除、反射、Stream、IO | 中 | 有精力再看 |

---

## 二、P0 必会知识点

### 2.1 equals / hashCode / ==

| 点 | 结论 |
|----|------|
| `==` | 基本类型比值；引用比地址 |
| `equals` | 默认同 `==`；业务常重写比内容 |
| 契约 | equals 相等 ⇒ hashCode **必须**相等 |
| HashMap | 先 hash 定位桶，再 equals |

**高频题**

1. `==` 和 equals 区别？  
2. 为什么重写 equals 必须重写 hashCode？  
3. 不重写 hashCode 在 HashMap 里会怎样？  

**口述：**  
> equals 相等 hash 必须相等，否则 HashMap 进不同桶，逻辑相等却 get 不到。

---

### 2.2 String

| 点 | 结论 |
|----|------|
| 不可变 | final 类 + 内部数组不可变 API |
| 好处 | 常量池共享、hash 缓存、安全、线程安全 |
| 拼接 | 单线程 StringBuilder；多线程才考虑 StringBuffer |
| 字面量 | 进字符串常量池（JDK7+ 池在堆） |

**高频题**

1. String 为什么不可变？  
2. String / StringBuilder / StringBuffer？  
3. `new String("a")` 和 `"a"` 区别？  

---

### 2.3 HashMap（全库最重点之一）

| 点 | JDK8 结论 |
|----|-----------|
| 结构 | 数组 + 链表 + 红黑树 |
| 默认 | 容量 16，负载因子 0.75 |
| 树化 | 链长≥8 **且** 数组≥64 → 树；≤6 退回链表 |
| 扩容 | 2 倍；下标 i 或 i+oldCap |
| hash | `^ (h>>>16)` 扰动后 `(n-1)&hash` |
| null | 允许一个 null key |
| 线程 | **不安全**（并发用 CHM） |

**put 流程（口述顺序）**

1. 算 hash → 定位桶  
2. 空则放入  
3. key 相同则覆盖  
4. 链过长则树化或扩容  
5. size≥阈值则扩容  

**高频题**

1. HashMap 底层原理？put 流程？  
2. 为何容量是 2 的幂？  
3. 为何树化阈值 8、退化 6？  
4. 多线程会怎样？  
5. 自定义 key 注意什么？  

**口述骨架：**  
> 数组链树，0.75 扩容，2 的幂位运算取下标，链长 8 且容量够才树化。非线程安全。

---

### 2.4 ArrayList

| 点 | 结论 |
|----|------|
| 底层 | Object[] 动态数组 |
| 扩容 | 约 1.5 倍 |
| 访问 | get O(1)；中间插删 O(n) |
| 线程 | 不安全；遍历删用迭代器 |

**对比 LinkedList：** 随机访问用 ArrayList；头尾频繁插删可考虑 LinkedList（实际 ArrayList 更常用）。

**高频题**

1. ArrayList 扩容？  
2. 与 LinkedList 怎么选？  
3. foreach 里 remove 为什么挂？fail-fast？  

---

### 2.5 值传递 + 异常（P0 简）

- Java **只有值传递**（引用传的是副本）  
- Error vs Exception；运行时 vs 受检  
- try-with-resources 关资源  

**高频题：** 值传递还是引用传递？异常体系？

---

## 三、P1 常考

### 3.1 ConcurrentHashMap

| 点 | JDK8 |
|----|------|
| 手段 | CAS 挂头 + synchronized 锁桶头 |
| null | **不允许** null key/value |
| get | 基本无锁（volatile 语义） |
| size | 近似（CounterCell） |

**高频题：** 与 HashMap/Hashtable 区别？get 加锁吗？为何禁 null？

### 3.2 LinkedHashMap / LRU

- 维护插入序或访问序  
- `accessOrder=true` + `removeEldestEntry` → 简易 LRU  

### 3.3 其他集合速查

| 类 | 一句话 |
|----|--------|
| HashSet | 包 HashMap，value 固定 |
| TreeMap | 红黑树，有序 |
| Hashtable | 方法同步，基本淘汰 |
| COWArrayList | 写时复制，读多写少 |
| fail-fast | modCount，结构修改抛 CME |

### 3.4 OOP / 重写重载 / Integer

| 点 | 结论 |
|----|------|
| 重载 | 同名不同参，编译期 |
| 重写 | 子类覆盖实例方法，运行期 |
| 抽象类 vs 接口 | 单继承多实现；接口偏契约 |
| Integer | -128~127 缓存，比较用 equals |

---

## 四、P2 加分（可后背）

| 点 | 一句话 |
|----|--------|
| 泛型擦除 | 编译期检查，运行时擦除 |
| 反射 | 灵活、慢、破坏封装 |
| Stream | 中间懒、终端触发；并行注意池 |
| Optional | 防 NPE 语义，别当字段乱用 |
| final | 引用不可变 ≠ 对象内容不可变 |

---

## 五、自测清单（按优先级）

### P0（不会就过不了）

- [ ] equals / hashCode 契约  
- [ ] String 不可变原因  
- [ ] HashMap 结构 + put + 扩容 + 树化  
- [ ] HashMap 为何非线程安全  
- [ ] ArrayList 扩容与 fail-fast  
- [ ] 值传递  

### P1

- [ ] ConcurrentHashMap 原理  
- [ ] LRU 怎么做  
- [ ] 重写 vs 重载  
- [ ] Integer 缓存  
- [ ] 抽象类 vs 接口  

### P2

- [ ] 泛型擦除  
- [ ] 反射场景  
- [ ] Stream 注意点  

---

## 六、关联

| 文档 | 内容 |
|------|------|
| [并发](./并发高频面试题与知识点.md) | 线程安全、CHM 深挖 |
| [归档口述合集](./archive/Java高频面试口述答案-归档.md) | 历史合集，优先用面渣分册 |
| [追问与手写](./Java面试追问与手写题.md) | HashMap 追问、LRU 手写 |
| [README](./README.md) | 总序 |

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-20 | 定位基础+集合；删跨专题重复 |
| 2026-07-20 | **P0→P1→P2 重构**，高频优先 |
