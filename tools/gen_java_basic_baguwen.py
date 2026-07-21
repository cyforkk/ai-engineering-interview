# -*- coding: utf-8 -*-
"""Java 基础高频八股完整卷（按用户大纲 1～8 模块）。不碰面渣。"""
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def w(name, text):
    p = DOCS / name
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print(name, p.stat().st_size)


NAV = """<!-- NAV:START -->
> 📖 **Java 基础八股** · 🗣️ [面渣](./Java面渣级口述.md) · 🃏 [卡片](./Java卡片速记.md)
>
> [模块总览](./Java八股模块总览.md) · [集合/HashMap 等同文件下文](#九集合框架衔接) · [Java8+](./Java8加分项知识点.md)
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md) · [路径](./路径-Java后端.md)
>
<!-- NAV:END -->
"""

JAVA = f"""# Java 基础 · 高频八股知识点（完整卷）

{NAV}

> 大厂/中厂 **Java 基础**最高频考点。格式：**题目 + 核心知识点**，强调对比与「为什么」。  
> 练嘴 → [Java面渣级口述.md](./Java面渣级口述.md)；速记 → [Java卡片速记.md](./Java卡片速记.md)。

### 面试回答技巧（先记住）

1. **先结论后展开**  
2. **主动对比**（== vs equals、抽象类 vs 接口…）  
3. **能点底层/原理**（String 不可变、Integer 缓存…）  
4. **可举一行代码例子**

---

# 一、Java 语言基础与特性

## 1. JVM、JDK、JRE 的区别？

| 概念 | 是什么 | 包含关系 |
|------|--------|----------|
| **JVM** | 虚拟机，负责加载/执行字节码 | 最核心运行引擎 |
| **JRE** | 运行环境 | JVM + 核心类库 |
| **JDK** | 开发工具包 | JRE + javac、调试/工具等 |

- 跑程序要 **JRE（含 JVM）**；开发要 **JDK**。  
- 不同 OS 有不同 JVM 实现 → 配合字节码实现跨平台。

---

## 2. Java 为什么能跨平台？

- 口号：**一次编译，到处运行**。  
- 源码 → `javac` → **字节码 `.class`**（平台无关）。  
- 各平台安装对应 **JVM**，解释执行或 JIT 编译成本地代码。  
- **为什么这样设计**：业务代码不绑死某一 OS 指令集，移植成本低。

---

## 3. 字节码是什么？好处？

- **中间码**（非 x86/ARM 机器码），给 JVM 用。  
- **好处**
  - 平台无关  
  - 便于安全校验与优化  
  - 支撑跨平台与统一工具链  

---

## 4. Java 是编译型还是解释型？

- **两者兼有**（先结论）。  
  1. 先 **编译** 成字节码  
  2. JVM **解释**执行字节码  
  3. 热点代码 **JIT** 编成机器码加速  
- 别只答「解释型」——会显得不完整。

---

## 5. Java 有哪些特性？（常开口题）

- 面向对象、跨平台、自动内存管理（GC）、相对安全的沙箱模型、多线程、健壮性（异常、强类型等）。  
- 结合岗位可补：生态丰富、偏后端与企业级。

---

# 二、数据类型与运算符

## 6. 基本数据类型有哪些？各占多少字节？

| 类型 | 字节 | 说明 |
|------|------|------|
| byte | 1 | 整数 |
| short | 2 | 整数 |
| int | 4 | 默认整型 |
| long | 8 | 后缀 L |
| float | 4 | 后缀 F |
| double | 8 | 默认浮点 |
| char | 2 | Unicode 字符 |
| boolean | 未严格规定（常见实现 1） | true/false |

- 引用类型：类、接口、数组等。  

---

## 7. 自动装箱与拆箱？

- **装箱**：基本 → 包装（`Integer.valueOf`）  
- **拆箱**：包装 → 基本（`intValue`）  
- 语法糖：`Integer a = 10;` / `int b = a;`  
- **坑**：空包装拆箱 → NPE；循环里装箱产生大量对象；**缓存区间**见下题。

---

## 8. Integer 缓存机制？（必考）

- `Integer.valueOf` 对 **-128～127**（默认）返回**缓存对象**。  
- `Integer a = 127; Integer b = 127;` → `a == b` 为 **true**  
- `Integer a = 128; Integer b = 128;` → `a == b` 为 **false**  
- 比较内容用 **equals**。  
- `new Integer(127)` 不走缓存。  
- **为什么缓存**：小整数高频使用，减少对象分配。

---

## 9. & 和 && 的区别？

| | & | && |
|--|---|-----|
| 逻辑 | 两边**都算** | **短路**：左为 false 不算右 |
| 位运算 | 可按位与 | 不用于位运算语义 |

- `|` vs `||` 同理（或 / 短路或）。  
- 例：`obj != null && obj.method()` 必须用 `&&` 防 NPE。

---

## 10. 最有效率计算 2×8？

- `2 << 3`（左移 3 位 = ×8）。  
- 位运算通常比乘除指令更轻（面试常考「你会不会位运算思维」）。  
- 可读性优先时业务代码仍写 `2 * 8` 也可，面试说得出位运算即可。

---

## 11. switch 支持哪些类型？

- 传统：`byte/short/char/int` 及其包装、`enum`、**String（JDK7+）**。  
- **不支持** long（经典考点）。  
- JDK14+ switch 表达式；JDK21+ **模式匹配** switch（加分）。

---

# 三、面向对象（OOP）核心

## 12. 面向对象 vs 面向过程？

| | 面向过程 | 面向对象 |
|--|----------|----------|
| 思维 | 步骤/流程 | 对象协作 |
| 数据与行为 | 常分离 | **封装**在一起 |
| 优势 | 简单直接 | 易维护、复用、扩展 |

---

## 13. 三大特性 + 抽象？

- **封装**：隐藏实现，暴露接口。  
- **继承**：复用、is-a。  
- **多态**：同一引用，不同实现。  
- **抽象**：抽共性（抽象类/接口），常作第四特性。

---

## 14. 多态的实现条件与好处？

- **条件**：继承（或实现接口）+ **方法重写** + **父类/接口引用指向子类对象**。  
- **好处**：开闭原则——扩展新子类少改调用方；提高可维护性。  
- 绑定：实例方法多为**动态分派**（运行期）。

---

## 15. 重载 vs 重写？

| | 重载 Overload | 重写 Override |
|--|---------------|---------------|
| 位置 | 同类（可见） | 子类对父类 |
| 规则 | 同名，**参数列表不同** | 方法签名基本相同 |
| 多态 | **编译期**（静态分派） | **运行期**（动态分派） |
| 返回值 | 可不同 | 协变返回值允许 |

---

## 16. 抽象类 vs 接口？

| | 抽象类 | 接口 |
|--|--------|------|
| 构造 | 可有 | 不能实例化接口本身 |
| 成员变量 | 可有普通字段 | 多为常量 |
| 方法 | 抽象 + 普通 | JDK8 default/static；JDK9 private |
| 继承 | 单继承 | 多实现 |
| 设计意图 | is-a 模板 | can-do 能力 |

---

## 17. 访问修饰符范围？

```text
public > protected > default（包内）> private
```

| 修饰符 | 同类 | 同包 | 子类（异包） | 其他 |
|--------|------|------|--------------|------|
| private | ✓ | | | |
| default | ✓ | ✓ | | |
| protected | ✓ | ✓ | ✓ | |
| public | ✓ | ✓ | ✓ | ✓ |

---

## 18. this 与 super？

- **this**：当前对象；调本类构造 `this(...)` 必须第一行。  
- **super**：父类；`super()` / `super.method()`；调父构造也必须第一行。  
- 子类构造默认会调父类无参构造（没有则需显式 super）。

---

# 四、关键字与重要概念

## 19. final 三种用法？

- **类**：不可继承（如 String）。  
- **方法**：不可重写。  
- **变量**  
  - 基本类型：值不可变  
  - 引用类型：**引用**不可变，对象内容仍可能变  
- 空白 final：构造结束前赋值。

---

## 20. static 用法？

- 静态变量：类级别共享。  
- 静态方法：无 this，**不能直接访问**非静态成员。  
- 静态代码块：类加载时执行（初始化）。  
- 静态内部类：不持有外部类引用（对比非静态内部类）。  

---

## 21. final / finally / finalize？

| | 含义 |
|--|------|
| final | 关键字（类/方法/变量） |
| finally | try 后**通常必执行**的块（释放资源） |
| finalize | Object 方法，GC 前调用，**已废弃**，别依赖 |

---

## 22. 成员变量 vs 局部变量？

| | 成员变量 | 局部变量 |
|--|----------|----------|
| 位置 | 类中 | 方法/块内 |
| 默认值 | 有（0/null/false） | **必须先赋值再使用** |
| 修饰 | 可用访问修饰、static 等 | 基本只有 final |

---

## 23. 值传递还是引用传递？

- **只有值传递**。  
- 基本类型：拷贝值。  
- 引用类型：拷贝**地址值**（引用的副本）。  
- 方法内 `param = new X()` 不改变外部引用；`param.setY()` 可改同一对象状态。

---

# 五、String 相关（超级高频）

## 24. String 为什么不可变？（原理）

- 类 `final`；底层 `char[]`（JDK9+ 多为 `byte[]` + coder）；无暴露可改内部数组的方法。  
- **为什么这样设计**  
  1. **常量池共享**安全  
  2. **hashCode 可缓存**（适合 HashMap key）  
  3. **线程安全**、防篡改（安全敏感字符串）  

---

## 25. String / StringBuilder / StringBuffer？

| | 可变 | 线程安全 | 场景 |
|--|------|----------|------|
| String | 否 | 是（不可变） | 少量、常量 |
| StringBuilder | 是 | 否 | **单线程拼接首选** |
| StringBuffer | 是 | 是（synchronized） | 历史多线程场景 |

---

## 26. `"abc"` 与 `new String("abc")`？

- `String s1 = "abc";`：优先用**字符串常量池**中的引用。  
- `String s2 = new String("abc");`：堆上**一定新建对象**；字面量 `"abc"` 仍可能让池中有一份。  
- 对象个数题要分「池中是否已有」讨论，面试说清**池 vs 堆**即可。

---

## 27. intern() 作用？

- 尝试把字符串放入常量池，并**返回池中引用**。  
- JDK6 与 7+ 池位置/行为有差异（7+ 池在堆，了解即可）。  
- 使用场景：大量重复字符串时减少重复（谨慎，别滥用）。

---

## 28. 字符串拼接底层？

- 循环里 `+` 易产生多个临时对象（老说法）。  
- 编译器常优化为 `StringBuilder.append`（单语句/可分析的拼接）。  
- **循环拼接**请手写 `StringBuilder`，意图清晰、避免意外。

---

# 六、equals 与 hashCode（必考）

## 29. == 与 equals？

- `==`：基本比**值**；引用比**地址**。  
- `equals`：Object 默认比地址；可重写比内容。

---

## 30. 为什么重写 equals 必须重写 hashCode？

- **约定**：equals 相等 ⇒ hashCode 必须相等。  
- HashMap/HashSet：**先 hash 分桶，再 equals**。  
- 只改 equals 不改 hashCode → 相等对象不同桶 → **存取异常**。  
- hash 相同不保证 equals true（碰撞允许）。

### equals 规范（中高级加分）

- 自反、对称、传递、一致；`x.equals(null)` 为 false。  
- 参与 equals 的字段应参与 hashCode。  
- 建议用 IDE/`Objects`/`record` 生成。

---

## 31. Object 常用方法？

- `equals` / `hashCode` / `toString` / `getClass`  
- `clone`（需 Cloneable，注意深浅拷）  
- `wait` / `notify` / `notifyAll`（锁与等待）  
- `finalize`（废弃）

---

# 七、异常处理

## 32. 异常体系？

```text
Throwable
├── Error                 严重错误，通常不捕获（OOM、StackOverflow）
└── Exception
    ├── RuntimeException  运行时/非检查异常
    └── 其他 Exception    检查异常（编译期需处理或声明）
```

- **检查异常**：IOException 等，强制处理。  
- **运行时异常**：NPE、IllegalArgument 等。

---

## 33. try 里有 return，finally 还会执行吗？

- **会执行**。  
- 流程直觉：先算 return 值并**暂存** → 执行 finally → 再真正返回。  
- **finally 里 return** 会覆盖之前的返回（极不推荐）。  
- finally 里改返回的对象字段可能影响结果；改基本类型暂存值一般不影响已暂存返回值（经典笔试题）。

---

## 34. 异常处理方式？

- `try-catch-finally`  
- `throws` 声明抛出  
- `throw` 手动抛  
- try-with-resources（自动关资源，推荐）

---

## 35. 自定义异常？

- 继承 `Exception`（检查）或 `RuntimeException`（非检查）。  
- 提供有意义的 message / 错误码，便于排查。

---

# 八、其他高频基础点

## 36. 深拷贝 vs 浅拷贝？

- **浅拷贝**：复制对象壳，内部引用仍指向原对象字段。  
- **深拷贝**：递归复制内部对象，互不影响。  
- 实现：`clone`（慎用）、拷贝构造、序列化、工具库等。

---

## 37. 创建对象的方式？

1. `new`  
2. 反射（`newInstance` / Constructor）  
3. `clone`  
4. 反序列化  
5. Unsafe 等（框架底层，了解）  

---

## 38. 泛型？

- 编译期类型检查；**运行时类型擦除**。  
- `? extends T`：上界（生产者，适合 get）  
- `? super T`：下界（消费者，适合 put）  
- PECS：Producer Extends, Consumer Super。

---

## 39. 注解 Annotation？

- 元数据；不直接改逻辑，靠反射/编译处理。  
- 生命周期 `@Retention`：SOURCE / CLASS / RUNTIME  
- `@Target` 限制使用位置  
- 框架基础：Spring、JUnit 等  

---

## 40. 反射？

- 运行时获取类、方法、字段并调用。  
- **用途**：框架（Spring IOC、MyBatis 映射）。  
- **代价**：性能较低、破坏封装、安全检查。  

---

## 41. JDK8 基础新特性？（详见加分页）

- Lambda、函数式接口、Stream、Optional  
- 接口 default/static 方法  
- 新日期 API（`LocalDateTime` 等）  
- 完整笔记：[Java8加分项知识点.md](./Java8加分项知识点.md)

---

# 九、集合框架衔接

> 集合（HashMap 等）超级高频，已单独成章，见下文件同路径：  
> 若本仓库将「基础+集合」合并，HashMap 详解在：  
> **[集合部分 → 打开下文或保持下一章](#十集合框架超级高频)**

---

# 十、集合框架（超级高频，与基础常连考）

## 42. HashMap 底层（JDK7 / 8）？

- **JDK7**：数组 + 链表；头插；多线程扩容可能死循环。  
- **JDK8**：数组 + 链表 + 红黑树；尾插；链长≥8 且表长≥64 树化。  
- 默认 16、负载因子 0.75、扩容 2 倍；容量 2 的幂；`(n-1)&hash`。  
- 线程不安全 → ConcurrentHashMap。

## 43. ArrayList vs LinkedList？

- 数组随机访问 O(1) vs 链表头尾插删；实践默认 ArrayList。

## 44. HashMap vs Hashtable vs ConcurrentHashMap？

- 非线程安全 / 全表锁 / JDK8 CAS+锁节点；CHM 与 HT 一般不允许 null。

（更细 put 流程、CHM 原理见面渣与原集合扩展；需要源码级可点名加厚。）

---

# 基础模块自测清单

- [ ] JDK/JRE/JVM + 跨平台 + 编译解释兼有  
- [ ] 8 基本类型 + Integer 缓存 + &&/&&  
- [ ] 封装继承多态 + 重载重写 + 抽象类接口  
- [ ] final/static + 值传递  
- [ ] String 不可变三原因 + 三兄弟 + 池与 new  
- [ ] equals/hashCode 契约  
- [ ] 异常体系 + finally 与 return  
- [ ] 泛型擦除 + 反射用途  

**口述：** [Java面渣级口述.md](./Java面渣级口述.md)  
**卡片：** [Java卡片速记.md](./Java卡片速记.md)  
**下一模块：** [并发](./并发高频面试题与知识点.md) · [总览](./Java八股模块总览.md)

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 按「Java 基础高频八股」8 大模块完整补全 |
"""

CARDS = f"""# Java 基础 · 卡片速记

<!-- NAV:START -->
> [完整知识点](./Java高频面试题与知识点.md) · [面渣](./Java面渣级口述.md) · [总览](./Java八股模块总览.md)
<!-- NAV:END -->

> 遮住 **A** 回忆。

---

## 语言与平台

**Q1 JVM/JRE/JDK？**  
A: 执行引擎 / 运行环境=JVM+库 / 开发包=JRE+工具。

**Q2 为何跨平台？**  
A: 编译成字节码，各平台 JVM 执行。

**Q3 编译还是解释？**  
A: 先编译字节码，再解释+JIT。

## 类型与运算

**Q4 基本类型字节？**  
A: 1 2 4 8 / 4 8 / 2 / boolean 实现相关。

**Q5 Integer 缓存？**  
A: -128~127；外 false；用 equals。

**Q6 & 与 &&？**  
A: 都算 vs 短路。

**Q7 2×8 位运算？**  
A: `2<<3`。

**Q8 switch 类型？**  
A: byte/short/char/int/enum/String；非 long。

## OOP

**Q9 三大特性？**  
A: 封装继承多态（+抽象）。

**Q10 多态条件？**  
A: 继承+重写+父引用指子对象。

**Q11 重载 vs 重写？**  
A: 参数不同编译期 / 覆盖运行期。

**Q12 抽象类 vs 接口？**  
A: 单继承模板 vs 多实现能力；default 方法。

**Q13 访问范围？**  
A: public>protected>default>private。

## 关键字

**Q14 final 三种？**  
A: 类/方法/变量（引用不可变）。

**Q15 值传递？**  
A: 只有值传递；引用传地址副本。

**Q16 final/finally/finalize？**  
A: 关键字 / 必执行块 / 废弃。

## String

**Q17 不可变原因？**  
A: final+无改API；池化、hash、安全。

**Q18 三兄弟？**  
A: 不可变 / 可变非安全 / 可变安全。

**Q19 "a" vs new String("a")？**  
A: 池引用 vs 堆新建。

**Q20 intern？**  
A: 入池并返回池引用。

## equals

**Q21 == vs equals？**  
A: 地址(值) / 默认同地址可重写内容。

**Q22 为何双写 hashCode？**  
A: 相等同 hash；HashMap 正确性。

## 异常

**Q23 体系？**  
A: Error vs Exception；检查 vs 运行时。

**Q24 try return 与 finally？**  
A: finally 仍执行；可覆盖返回。

## 其他

**Q25 浅拷贝深拷贝？**  
A: 引用共享 vs 递归复制。

**Q26 泛型擦除？**  
A: 编译检查，运行擦除；extends/super。

**Q27 反射？**  
A: 运行时拿类信息；框架基础；慢。

**Q28 HashMap JDK8？**  
A: 数组+链+树；8/64；0.75。

---

完整：[Java高频面试题与知识点.md](./Java高频面试题与知识点.md)
"""


def main():
    w("Java高频面试题与知识点.md", JAVA)
    w("Java卡片速记.md", CARDS)
    # patch overview line if file exists
    ov = DOCS / "Java八股模块总览.md"
    if ov.exists():
        t = ov.read_text(encoding="utf-8")
        if "Java 基础完整卷" not in t:
            t = t.replace(
                "| 1 基础+集合 |",
                "| 1 **Java 基础完整卷**+集合 |",
            )
            # add note after priority
            note = "\n\n> **Java 基础**已按 8 大模块补全：语言特性、类型、OOP、关键字、String、equals、异常、泛型反射等。→ [Java高频面试题与知识点.md](./Java高频面试题与知识点.md)\n"
            if "Java 基础已按" not in t:
                t = t.replace(
                    "原则：**原理 + 对比 + 场景**，不要死背一句话。",
                    "原则：**原理 + 对比 + 场景**，不要死背一句话。" + note,
                )
            ov.write_text(t, encoding="utf-8")
            print("overview patched")


if __name__ == "__main__":
    main()
