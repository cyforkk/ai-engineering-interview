# Java 基础 · 卡片速记

<!-- NAV:START -->
> [完整卷](./Java高频面试题与知识点.md) · [频率](./Java基础八股频率排序.md) · [面渣](./Java面渣级口述.md)
<!-- NAV:END -->

> 遮住 A。**先 P0。** 集合见 [集合卡](./Java集合卡片速记.md)。

---

## OOP

**Q1 四大特性？** A: 封装继承多态抽象。

**Q2 重载 vs 重写？** A: 参数不同编译期 / 覆盖运行期。

**Q3 抽象类 vs 接口？** A: 单继承模板 vs 多实现能力。

**Q4 访问范围？** A: public>protected>default>private。

**Q5 多态条件？** A: 继承+重写+父引用指子对象。

## equals

**Q6 == vs equals？** A: 地址(值) / 可重写比内容。

**Q7 必须双写 hashCode？** A: 相等同 hash；HashMap 正确性。

**Q8 默认 equals？** A: 比引用 this==obj。

## String

**Q9 三兄弟？** A: 不可变 / 可变非安全 / 可变安全。

**Q10 为何不可变？** A: final+无改API；池化、hash、安全。

**Q11 "a" vs new？** A: 池引用 vs 堆新建。

**Q12 拼接？** A: 循环用 StringBuilder。

## 包装 / 异常

**Q13 Integer 缓存？** A: -128~127；外用 equals。

**Q14 异常分类？** A: Error/Exception；检查 vs 运行时。

**Q15 finally？** A: 通常执行；return 先暂存再 finally。

## 高频

**Q16 final/finally/finalize？** A: 关键字/必执行块/废弃。

**Q17 值传递？** A: 只有值传递；引用传副本。

**Q18 浅拷贝深拷贝？** A: 共享内部 vs 递归复制。

**Q19 泛型擦除？** A: 运行时擦除；编译期检查。

**Q20 PECS？** A: extends 产；super 消。

**Q21 Optional？** A: 显式可空；防 NPE。

**Q22 反射？** A: 运行时拿类信息；框架用；慢。

---

详解：[Java高频面试题与知识点.md](./Java高频面试题与知识点.md)
