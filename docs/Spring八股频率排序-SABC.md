# Spring / Spring Boot · 频率导航（2025–2026）

> **频率页只做索引。** 正文以链接的「完整卷」为准，避免重复维护。

> **完整卷：** [Spring高频面试题与知识点.md](./Spring高频面试题与知识点.md)  
> **面渣：** [Spring面渣级口述.md](./Spring面渣级口述.md) · **卡片：** [Spring卡片速记.md](./Spring卡片速记.md)  
> **全库主线：** [四档 P0](./Java后端面试频率-四档.md)

---

## 专项时间

| 优先级 | 模块 | 时间 |
|--------|------|:----:|
| P0 | IoC/AOP + 循环依赖 + 生命周期 + 自动装配 + 事务 | **50%** |
| P1 | 作用域 + MVC + 设计模式 | 25% |
| P2 | 传播隔离 + Filter/Interceptor + Async | 15% |
| P3 | 源码 + Starter + Conditional | 10% |

**说明**：中小厂问 Spring 多；大厂更爱结合项目深挖原理。

---

## 一、超高频

| # | 主题 | 入口 |
|---|------|------|
| 1 | IoC/DI（注入方式、Autowired/Resource、组件注解） | [§1](./Spring高频面试题与知识点.md) |
| 2 | AOP（概念、JDK/CGLIB、通知、场景） | [§2](./Spring高频面试题与知识点.md) |
| 3 | Bean 生命周期 + BPP + Aware | [§3](./Spring高频面试题与知识点.md) |
| 4 | 循环依赖三级缓存 | [§4](./Spring高频面试题与知识点.md) |
| 5 | Boot 自动装配 + Starter + 启动 | [§5](./Spring高频面试题与知识点.md) |
| 6 | @Transactional 原理/失效/传播/回滚 | [§6](./Spring高频面试题与知识点.md) |

---

## 二、高频

Bean 作用域与线程安全 · FactoryBean · MVC 流程 · 设计模式 · Filter/Interceptor · @Async · 定时任务 · Cache  

---

## 三、中频

Conditional · 配置优先级 · Profile · 事件 · BeanDefinition · BFPP vs BPP · 优雅停机  

---

## 四、低频加分

refresh · 三级缓存源码 · Boot3 · Configuration full/lite · 自定义 Conditional  

---

## 必须画图的三块

```text
1. Bean 生命周期
2. 三级缓存解决循环依赖
3. 自动装配链路
```

---

## 点名

`三级缓存` · `自动装配` · `事务失效` · `生命周期` · `MVC流程`

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 对齐超高中低频大纲重写频率导航 |
