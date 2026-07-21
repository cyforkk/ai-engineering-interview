# Java 基础 · 卡片速记

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
