# Spring · 卡片速记

<!-- NAV:START -->
> **只背要点。** 原理 → [详解](./Spring高频面试题与知识点.md) · 怎么说 → [面渣](./Spring面渣级口述.md)
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md) · [路径](./路径-Java后端.md)
>
<!-- NAV:END -->

> 用法：遮住 **A**，只看 **Q** 回忆；卡壳回详解。

---

## 1. IOC？

**A:** 控制反转：对象创建装配交给容器。

## 2. DI？

**A:** 依赖注入：构造/setter/字段注入依赖。

## 3. Bean 作用域？

**A:** 默认单例；prototype/request/session 等。

## 4. 循环依赖？

**A:** 单例三级缓存可解构造器循环仍难。

## 5. AOP 用途？

**A:** 日志、事务、鉴权等横切，代理实现。

## 6. JDK 动态代理 vs CGLIB？

**A:** 接口 vs 子类。

## 7. @Transactional 失效？

**A:** 自调用、非 public、异常被吞、错误传播。

## 8. Spring Boot 自动配置？

**A:** 条件注解 + starter + spring.factories/AutoConfiguration.imports。

## 9. Bean 生命周期要点？

**A:** 实例化→属性→Aware→初始化前后→销毁。

## 10. 过滤器 vs 拦截器？

**A:** Servlet 滤 vs Spring MVC 拦。

---

详解：[Spring高频面试题与知识点.md](./Spring高频面试题与知识点.md) · 面渣：[Spring面渣级口述.md](./Spring面渣级口述.md)
