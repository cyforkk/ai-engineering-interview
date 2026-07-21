# Python · 卡片速记

<!-- NAV:START -->
> [完整卷](./Python高频面试题与知识点.md) · [频率](./Python八股频率排序.md) · [面渣](./Python面渣级口述.md)
<!-- NAV:END -->

> 遮住 A。**先 P0。**

---

## 数据类型

**Q1 list vs tuple？** A: 可变序列 vs 不可变；tuple 可作键（元素可哈希）。

**Q2 dict 底层？** A: 哈希表；键须可哈希。

**Q3 可变不可变？** A: list/dict/set vs int/str/tuple。

**Q4 默认参数坑？** A: 可变默认只创建一次；用 None。

**Q5 浅拷贝深拷贝？** A: 内层共享 vs 递归复制。

## 函数

**Q6 *args **kwargs？** A: 位置元组 / 关键字字典。

**Q7 装饰器？** A: 函数包函数；@ 语法糖；wraps。

**Q8 闭包？** A: 内函数引用外变量并返回。

**Q9 yield？** A: 生成器惰性产出。

**Q10 列表推导 vs 生成器表达式？** A: 全量 list vs 惰性。

## OOP / 并发

**Q11 __new__ vs __init__？** A: 创建 vs 初始化。

**Q12 classmethod vs staticmethod？** A: 收 cls / 无强制实例。

**Q13 GIL？** A: 同进程同时一线程跑字节码；CPU用进程。

**Q14 线程进程协程？** A: IO / CPU / 高并发IO。

**Q15 GC？** A: 引用计数+循环检测+分代。

## 其他

**Q16 is vs ==？** A: 同一对象 vs 相等。

**Q17 with？** A: enter/exit 保证清理。

**Q18 LEGB？** A: Local Enclosing Global Builtin。

**Q19 字符串拼接？** A: join 优于循环 +。

**Q20 asyncio 禁忌？** A: 协程里阻塞调用。

---

详解：[Python高频面试题与知识点.md](./Python高频面试题与知识点.md) · 手写：[Python手写题.md](./Python手写题.md)
