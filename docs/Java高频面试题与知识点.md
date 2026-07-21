# Java 基础 · 高频八股知识点（完整卷）

<!-- NAV:START -->
> 📖 **Java 基础完整卷** · 🗣️ [面渣](./Java面渣级口述.md) · 🃏 [卡片](./Java卡片速记.md) · 🔥 [频率导航](./Java基础八股频率排序.md)
>
> [集合完整卷](./Java集合框架高频面试题与知识点.md) · [四档主线](./Java后端面试频率-四档.md) · [Java8+](./Java8加分项知识点.md)
>
<!-- NAV:END -->


> 所有后端面试的基石。**OOP、String、equals/hashCode、异常** 出现频率极高。  
> 集合见独立卷；本卷聚焦语言基础。

### 专项时间占比

| 优先级 | 模块 | 时间 |
|--------|------|:----:|
| **P0** | 面向对象 + equals/hashCode + String + 异常 | **50%** |
| **P1** | 装箱拆箱 + final/static + 值传递 + 深浅拷贝 | **20%** |
| **P2** | 泛型 + Java 8（Lambda/Stream/Optional） | **20%** |
| **P3** | 反射、序列化、IO、注解等 | **10%** |

### 高效准备

1. equals/hashCode + String 不可变 **讲清原理+举例**  
2. OOP 结合代码讲多态  
3. try-catch-finally 带 return 的代码题  
4. Stream/Optional 正确用法，防 NPE  
5. 踩坑：Integer 缓存、拼接性能、异常被吞  

---

# 一、超高频（几乎必问）

## 1. 面向对象

### 1.1 四大特性？

| 特性 | 含义 |
|------|------|
| **封装** | 隐藏实现，暴露接口 |
| **继承** | 复用、is-a |
| **多态** | 同一引用，不同实现 |
| **抽象** | 抽共性（抽象类/接口） |

### 1.2 重载 vs 重写？

| | 重载 Overload | 重写 Override |
|--|---------------|---------------|
| 范围 | 同类 | 子类覆盖父类 |
| 规则 | 同名，**参数列表不同** | 方法签名基本相同 |
| 绑定 | **编译期**（静态分派） | **运行期**（动态分派） |

### 1.3 抽象类 vs 接口？

| | 抽象类 | 接口 |
|--|--------|------|
| 构造 | 可有 | 不能实例化接口 |
| 成员变量 | 可有普通字段 | 多为常量 |
| 方法 | 抽象+普通 | JDK8+ default/static；JDK9 private |
| 继承 | 单继承 | 多实现 |
| 设计 | is-a 模板 | can-do 能力 |

### 1.4 访问修饰符？

```text
public > protected > default（包内）> private
```

| 修饰符 | 同类 | 同包 | 子类(异包) | 其他 |
|--------|------|------|------------|------|
| private | ✓ | | | |
| default | ✓ | ✓ | | |
| protected | ✓ | ✓ | ✓ | |
| public | ✓ | ✓ | ✓ | ✓ |

### 1.5 this 与 super？

- **this**：当前对象；`this()` 调本类构造（第一行）  
- **super**：父类；`super()` 调父构造（第一行）；`super.method()`  

### 1.6 多态实现原理？

- 条件：继承/实现 + 重写 + 父引用指子对象  
- **动态绑定**：实例方法调用看运行时类型（虚方法表直觉）  
- 静态方法/私有/final 等多为静态绑定  

---

## 2. equals 与 hashCode

### 2.1 == 与 equals？

| | == | equals |
|--|-----|--------|
| 基本类型 | 比**值** | — |
| 引用类型 | 比**地址** | 默认同地址；可重写比**内容** |

### 2.2 为何重写 equals 必须重写 hashCode？

- 约定：equals 为 true ⇒ hashCode **必须**相同  
- HashMap/HashSet：**先 hash 分桶，再 equals**  
- 只改 equals → 相等对象不同桶 → **存取异常**  

### 2.3 Object.equals 默认？

- 默认：`return (this == obj);` 比引用  

### 2.4 如何正确重写？

- 自反、对称、传递、一致；`equals(null)` 为 false  
- 用 `Objects.equals` / IDE / `record` 生成  
- **参与 equals 的字段必须参与 hashCode**  
- 建议用 `Objects.hash(...)`  

---

## 3. String 相关

### 3.1 String / StringBuilder / StringBuffer？

| | 可变 | 线程安全 | 场景 |
|--|------|----------|------|
| String | 否 | 是（不可变） | 常量、少量拼接 |
| StringBuilder | 是 | 否 | **单线程拼接首选** |
| StringBuffer | 是 | 是（synchronized） | 历史多线程场景 |

### 3.2 为何不可变？

- 类 `final`；内部 `private final` 数组（JDK9+ 多为 `byte[]`）；无对外修改内容的 API  
- **好处**：常量池共享安全；hash 可缓存；线程安全；防篡改  

### 3.3 `"abc"` vs `new String("abc")`？

- `"abc"`：常量池引用（池中无则创建）  
- `new String("abc")`：堆上**一定新建**对象；字面量可能使池中也有  
- 对象个数题要分「池中是否已有」讨论  

### 3.4 字符串常量池？

- 复用相同字面量，省内存  
- **JDK7+ 池在堆中**  

### 3.5 intern()？

- 尝试放入常量池并**返回池中引用**  
- 7+ 行为与 6 有差异（了解即可）  

### 3.6 拼接：+ 还是 StringBuilder？

- 循环内大量拼接 → **StringBuilder**  
- 单行/编译器可优化的 `+` 可能变成 Builder；**循环别依赖优化**  

---

## 4. 基本类型与包装类

### 4.1 自动装箱拆箱？

- 装箱：基本 → 包装（`Integer.valueOf`）  
- 拆箱：包装 → 基本（`intValue`）  
- 语法糖；注意 **NPE**（null 拆箱）  

### 4.2 Integer 缓存？

- `valueOf` 缓存 **-128～127**（默认）  
- `Integer a=127; Integer b=127;` → `a==b` **true**  
- `128` → **false**（不同对象）  
- 比内容用 **equals**  

### 4.3 基本类型字节？

| 类型 | 字节 |
|------|------|
| byte | 1 |
| short | 2 |
| int | 4 |
| long | 8 |
| float | 4 |
| double | 8 |
| char | 2 |
| boolean | 未严格规定（实现相关） |

---

## 5. 异常体系

### 5.1 分类？

```text
Throwable
├── Error          （OOM、StackOverflow 等，通常不捕获）
└── Exception
    ├── RuntimeException  → 非检查/运行时
    └── 其他 Exception    → 检查异常（编译期需处理）
```

### 5.2 try-catch-finally？finally 一定执行？

- 正常：try → catch(若有) → finally  
- **return**：先算返回值暂存 → finally → 再返回  
- finally 中 return 会覆盖（极不推荐）  
- 不一定执行：`System.exit`、JVM 崩溃、线程被 kill 等极端  

### 5.3 如何处理？throws vs throw？

| | throws | throw |
|--|--------|-------|
| 位置 | 方法签名 | 方法体 |
| 含义 | 声明可能抛出 | 手动抛出实例 |

- 能处理则 catch；否则声明；勿空 catch 吞掉  
- 资源：try-with-resources  

### 5.4 常见运行时异常？

- NPE、IndexOutOfBounds、ClassCast、IllegalArgument、Arithmetic、ConcurrentModification 等  

---

# 二、高频

## 6. 关键字与语法

### 6.1 final / finally / finalize？

| | 含义 |
|--|------|
| final | 类不可继承 / 方法不可重写 / 变量不可重新赋值 |
| finally | try 后通常必执行块 |
| finalize | GC 前回调，**已废弃** |

- final 引用：引用不可变，对象内容可变  

### 6.2 static？

- 静态变量：类共享  
- 静态方法：无 this，不能直接访问非静态  
- 静态代码块：类加载时执行  
- 静态内部类：不持有外部类引用  

### 6.3 成员变量 vs 局部变量？

| | 成员 | 局部 |
|--|------|------|
| 默认值 | 有 | **必须先赋值** |
| 位置 | 类中 | 方法/块内 |

### 6.4 值传递还是引用传递？

- **只有值传递**  
- 引用类型：传的是**地址副本**  
- 方法内 `param = new X()` 不改外部引用；`param.set` 可改同一对象  

### 6.5 深拷贝 vs 浅拷贝？

| 浅 | 深 |
|----|-----|
| 只拷外壳，内部引用共享 | 递归拷内部对象 |
| clone 默认浅 | 拷贝构造、序列化、手动、库 |

---

## 7. Object 类

### 常用方法

- equals / hashCode / toString / getClass  
- clone（需 Cloneable，浅拷注意）  
- wait / notify / notifyAll（锁与等待）  
- finalize（废弃）  

### clone 注意

- 默认浅拷贝；深拷需自己实现  
- 实现 Cloneable；异常 CloneNotSupportedException  

---

## 8. 泛型

### 是什么？好处？

- 参数化类型；编译期类型检查  
- 好处：类型安全、少强转  

### 类型擦除？

- 运行时泛型信息擦除为原始类型（边界内）  
- 不能 `new T()`、不能泛型数组等限制由此来  

### ? extends vs ? super（PECS）

| | extends 上界 | super 下界 |
|--|--------------|------------|
| 读 | 适合（生产者） | 只能当 Object |
| 写 | 受限 | 适合（消费者） |

- **PECS**：Producer Extends, Consumer Super  

---

## 9. Java 8 新特性（详见加分页）

| 特性 | 要点 |
|------|------|
| Lambda | 函数式接口的实例；本质匿名函数写法 |
| Stream | filter/map/reduce/collect；中间惰性、终端触发 |
| Optional | 显式可能为空；orElse/orElseGet/map；别滥用字段类型 |
| 接口 default/static | 兼容扩展 |
| LocalDateTime 等 | 不可变、线程安全，替代 Date |

完整：[Java8加分项知识点.md](./Java8加分项知识点.md)

---

# 三、中频

## 10. 反射

- 运行时获取类、方法、字段并调用  
- **场景**：Spring、框架、通用工具  
- **代价**：性能低、破坏封装、安全检查  

## 11. 注解生命周期

| Retention | 阶段 |
|-----------|------|
| SOURCE | 仅源码 |
| CLASS | 字节码（默认） |
| RUNTIME | 运行时（反射可读） |

## 12. 序列化

- 对象 ↔ 字节流；实现 Serializable  
- **serialVersionUID**：版本兼容  
- **transient**：不序列化该字段  
- 反序列化可不走构造（注意）  

## 13. BIO / NIO / AIO

| | BIO | NIO | AIO |
|--|-----|-----|-----|
| 模型 | 同步阻塞 | 同步非阻塞/多路复用 | 异步 |
| 典型 | 一连接一线程 | Selector/Channel | 回调完成 |

详见：[网络](./计算机网络高频面试题与知识点.md)

## 14. 枚举

- 本质 final 类 + 静态实例  
- 防反射/反序列化破坏单例：枚举单例最安全（Effective Java）  

## 15. 内部类

- 成员 / 静态 / 局部 / 匿名  
- 静态内部类不持外部引用  

## 16. 创建对象方式

1. new  
2. 反射  
3. clone  
4. 反序列化  
5. Unsafe 等（框架）  

---

# 四、低频 / 进阶

- 位运算：权限掩码、状态位  
- switch：JDK7 String；12+ 箭头与 yield；21 模式匹配  
- 浮点：用 **BigDecimal(String)**，忌 `new BigDecimal(0.1)`  
- 类初始化时机：new、访问静态、反射、主类等  
- JPMS 模块化（9+）了解  
- Record / Sealed / Pattern Matching（14+）加分  

---

# 自测清单

### P0
- [ ] 四大特性 + 重载重写 + 抽象类接口 + 多态  
- [ ] ==/equals/hashCode 契约与正确重写  
- [ ] String 不可变三原因 + 三兄弟 + 池/new  
- [ ] 异常体系 + finally 与 return  

### P1
- [ ] Integer 缓存  
- [ ] final/static + 值传递  
- [ ] 深浅拷贝  

### P2–P3
- [ ] 泛型擦除 + PECS  
- [ ] Stream/Optional  
- [ ] 反射用途  

**口述：** [Java面渣级口述.md](./Java面渣级口述.md)  
**卡片：** [Java卡片速记.md](./Java卡片速记.md)  
**频率：** [Java基础八股频率排序.md](./Java基础八股频率排序.md)  
**集合：** [Java集合框架高频面试题与知识点.md](./Java集合框架高频面试题与知识点.md)  

---

## 点名深挖

- String 不可变 + 常量池  
- equals/hashCode 正确模板  
- Integer 缓存机制  
- 异常 finally+return 代码题  

---

---

## 版本与假设

| 项 | 说明 |
|----|------|
| 复核 | 2026-07 |
| 默认假设 | Java 8–17 语法与集合语义；面试以 8/11/17 为主 |
| 维护 | 正文以本完整卷为 SSOT；频率页/精简页不重复堆考点 |

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 按超高/高/中/低频大纲重写 Java 基础完整卷 |
