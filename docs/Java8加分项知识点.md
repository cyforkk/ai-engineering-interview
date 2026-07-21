# Java 8+ 与常见加分项 · 知识点

<!-- NAV:START -->
> 📖 **八股知识点** · 🗣️ [面渣](./Java面渣级口述.md) · 🃏 [卡片](./Java卡片速记.md)
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md) · [Java路径](./路径-Java后端.md) · [模块总览](./Java八股模块总览.md)
>
<!-- NAV:END -->


> 基础模块的补充页：Lambda / Stream / 异步 / 日期。完整口语仍可并入 Java/并发面渣。

---

## 1. Lambda / 函数式接口？

- 匿名函数写法；目标类型为函数式接口（单一抽象方法）。  
- 例：`Runnable`、`Comparator`、自定义 `@FunctionalInterface`。

---

## 2. Stream？

- 声明式处理集合：`filter/map/reduce/collect`。  
- 惰性求值；可 parallel（注意线程安全与场景）。  
- 不要为炫技滥用难读链式。

---

## 3. Optional？

- 显式表达「可能为空」，减少 NPE。  
- `of/ofNullable/map/orElse/orElseGet`。  
- 不要滥用 Optional 做字段类型（看团队规范）。

---

## 4. CompletableFuture？

- 异步编排：`supplyAsync`、`thenApply`、`thenCombine`、`exceptionally`。  
- 自定义线程池，避免共用公共 ForkJoinPool 踩坑。

---

## 5. 新日期 API？

- `LocalDate/LocalDateTime/Instant/ZoneId`。  
- 不可变、线程安全；替代 `Date/Calendar` 老坑。

---

## 6. 其他加分

- 接口 default 方法。  
- 方法引用。  
- Java 11/17/21 LTS：var、Records、模式匹配、**虚拟线程**（见并发篇）。

---

**返回：** [Java 基础+集合](./Java高频面试题与知识点.md) · [并发](./并发高频面试题与知识点.md)
