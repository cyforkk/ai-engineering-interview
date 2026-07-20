# Java 基础 + 集合 · 面渣级长口述

> 配套：[Java高频面试题与知识点.md](./Java高频面试题与知识点.md)  
> 跨模块合集口述仍见：[Java高频面试口述答案.md](./Java高频面试口述答案.md)  
> 每题 2～4 分钟

---

## P0 长口述

### 1. == 和 equals，为什么要重写 hashCode

**口述：**

> == 对基本类型比较值，对引用类型比较是不是同一个对象，也就是地址。  
> equals 在 Object 里默认也是比地址，但 String、Integer 等重写了，变成比内容。业务类如果要按内容相等，也要重写 equals。  
>
> 重写 equals 必须重写 hashCode，这是契约：两个对象 equals 为 true，hashCode 必须一样。  
> 因为像 HashMap 这种结构，先用 hashCode 定位桶，再在桶里用 equals 比。  
> 如果你 equals 认为相等，但 hashCode 不同，它们会进不同桶，map.get 就找不到，逻辑就乱了。  
> 反过来 hashCode 相同不一定 equals，只是可能碰撞，再靠 equals 区分。

---

### 2. String 为什么不可变

**口述：**

> String 被设计成不可变：类是 final，内部字符数组不对外暴露修改，也没有提供改内容的方法。  
> 好处很多：  
> 第一，可以放进字符串常量池安全共享，省内存；  
> 第二，hashCode 可以缓存，做 HashMap 的 key 很合适；  
> 第三，天然线程安全，不用同步；  
> 第四，安全上，类名、文件路径、网络连接里的字符串不容易被中途篡改。  
>
> 所以大量拼接不要用 + 循环造很多中间对象，用 StringBuilder；多线程拼接才考虑 StringBuffer，现在更少见。

---

### 3. String、StringBuilder、StringBuffer

**口述：**

> String 不可变，每次修改都像新对象。  
> StringBuilder 可变，单线程拼接性能好。  
> StringBuffer 方法带同步，线程安全但更慢，现代代码里多线程拼接也更常用别的方式。  
> 选型：不可变用 String；单线程频繁改用 Builder。

---

### 4. HashMap 底层原理（核心长答，必背）

**口述：**

> 我按 JDK8 说。HashMap 底层是**数组 + 链表 + 红黑树**。  
>
> 默认容量 16，负载因子 0.75，也就是元素个数到容量的 0.75 会扩容。  
> put 的时候，先算 key 的 hash，JDK 会把 hashCode 高 16 位和低 16 位异或做扰动，让高位也参与，减少碰撞。然后用 `(n-1) & hash` 定位到数组下标，所以容量必须是 2 的幂，才能用位运算高效代替取模。  
>
> 如果桶是空的，直接放新节点。  
> 如果桶上已有节点，就遍历：key 的 hash 相同且 equals 相同，就覆盖 value；否则挂到链表后面。  
> 当链表长度达到 8，并且数组长度至少 64，就把链表转成红黑树，把最坏查找从 O(n) 降到 O(log n)。如果数组还不到 64，优先扩容而不是立刻树化。  
> 当树节点很少，比如小于等于 6，会退回链表，避免在边界上来回树化和退化。  
>
> 扩容是 2 倍扩，重新分布：元素要么还在原下标，要么在「原下标 + 旧容量」。  
> HashMap 允许一个 null key。  
> **它不是线程安全的**：并发 put 可能丢数据；JDK7 还有并发扩容死链的问题，JDK8 改善了死链但仍不能当并发容器用。并发场景用 ConcurrentHashMap。  
>
> 自定义 key 要正确重写 equals 和 hashCode，并且最好不可变，否则 key 改了 hash 变了，就 get 丢了。

**1 分钟精简版：**  
> 数组链树，16 和 0.75，扰动后位运算定位，链 8 且容量够树化，2 倍扩容，非线程安全。

---

### 5. ArrayList 原理

**口述：**

> ArrayList 底层是动态 Object 数组，随机访问 O(1)。  
> 默认空数组，添加时扩容，一般按约 1.5 倍扩，然后 copy 到新数组。  
> 中间插入删除要搬元素，O(n)。  
> 非线程安全。foreach 遍历时如果直接调用列表 remove，modCount 变化会触发 fail-fast，抛 ConcurrentModificationException，应该用迭代器的 remove。  
> 已知大概容量时指定 initialCapacity，减少扩容拷贝。  
> 和 LinkedList 比：LinkedList 双向链表，头尾快、随机访问慢，一般更常用 ArrayList。

---

### 6. Java 是值传递还是引用传递

**口述：**

> 只有**值传递**。  
> 传基本类型，传的是值的副本。  
> 传对象，传的是**引用的副本**，不是对象本身。方法里改引用指向不影响外面变量，但通过这个引用改对象内部字段，外面看得到。  
> 很多人说的「引用传递」不准确，准确说是传递引用值的拷贝。

---

### 7. 异常体系

**口述：**

> Throwable 下分 Error 和 Exception。  
> Error 如 OOM、StackOverflow，一般不捕获恢复。  
> Exception 分受检异常和运行时异常。受检要你处理或声明；运行时如 NPE、IllegalArgument 是编程问题。  
> 资源关闭用 try-with-resources，实现 AutoCloseable，避免 finally 里再出异常盖住原异常。

---

## P1 长口述

### 8. ConcurrentHashMap

**口述：**

> JDK8 的 ConcurrentHashMap 用 Node 数组，桶为空时 CAS 挂头节点，桶不为空时对桶头 synchronized，再操作链表或树，把锁粒度降到桶级。  
> 扩容时多线程可以协助迁移。  
> get 基本不加锁，靠 volatile 等语义保证可见。  
> 不允许 null key/value，因为并发下不好区分「没有」和「值就是 null」。  
> size 是近似统计，用类似 LongAdder 的分段计数，追求性能。  
> 和 Hashtable 整表锁比，并发好得多；和 HashMap 比，安全。

---

### 9. 如何用 LinkedHashMap 做 LRU

**口述：**

> LinkedHashMap 可以按访问顺序维护链表。  
> 构造时 accessOrder=true，重写 removeEldestEntry，当 size 超过容量返回 true 删最老节点，就是简易 LRU。  
> 注意默认不是线程安全，并发要外层同步或用专业缓存库如 Caffeine。

---

### 10. 重写和重载

**口述：**

> 重载是同名不同参数列表，编译期静态分派。  
> 重写是子类重新实现父类实例方法，运行期动态分派，实现多态。  
> 重写要求方法签名兼容，返回类型可协变，访问权限不能更严。static 方法不能多态重写，只能隐藏。

---

### 11. 抽象类和接口

**口述：**

> 抽象类可以有成员变量、构造器、普通方法实现，表达 is-a 模板。  
> 接口更偏 can-do 契约；Java8 后可有 default/static 方法。  
> 类单继承、多实现接口，扩展更灵活。能用接口抽象能力就用接口，需要复用实现和状态再用抽象类。

---

### 12. Integer 缓存

**口述：**

> valueOf 对 -128 到 127 用缓存，这个范围两个 Integer 可能 == 为 true；范围外是新对象，== 为 false。  
> 业务比较一律 equals，别用 == 比包装类型。

---

## 场景口述

### HashMap 在多线程下出问题

> 可能丢更新、数据不一致；老版本扩容死链导致 CPU 飙高。结论：并发用 CHM 或外层同步，别共享裸 HashMap 乱写。

### fail-fast

> 迭代中结构被改，modCount 不一致抛 CME，是快速失败保护，不是线程安全机制。

---

## 考前骨架

```text
equals 相等 ⇒ hash 必等；HashMap 先 hash 再 equals
String 不可变：池、安全、hash 缓存
HashMap：数组链树，0.75，2幂，8树化，非线程安全
ArrayList：数组 1.5 扩，fail-fast
CHM：CAS+锁桶头，禁 null
```

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-20 | 面渣级长口述初版（基础+集合） |
