# Spring / Spring Boot · 频率排名（2026）

> 综合 2025–2026 面经与主流资料。  
> **完整知识点：** [Spring高频面试题与知识点.md](./Spring高频面试题与知识点.md)  
> **面渣：** [Spring面渣级口述.md](./Spring面渣级口述.md) · **卡片：** [Spring卡片速记.md](./Spring卡片速记.md)

---

## S 级（几乎必问，70%+）

| 排名 | 知识点 | 核心考察点 | 入口 |
|:----:|--------|------------|------|
| 1 | Boot **自动装配** | EnableAutoConfiguration → imports/factories → Conditional | [§1](./Spring高频面试题与知识点.md) |
| 2 | **Bean 生命周期** | 实例化→注入→Aware→BPP→初始化→销毁 | [§2](./Spring高频面试题与知识点.md) |
| 3 | **循环依赖 + 三级缓存** | 为何三级、二级不够、何解不了 | [§3](./Spring高频面试题与知识点.md) |
| 4 | **IoC / DI** | 本质、三种注入、Autowired vs Resource | [§4](./Spring高频面试题与知识点.md) |
| 5 | **AOP** | JDK vs CGLIB、默认代理、通知 | [§5](./Spring高频面试题与知识点.md) |
| 6 | **@Transactional 失效** | this/非public/吞异常/检查异常… | [§6](./Spring高频面试题与知识点.md) |

### 必须滚瓜烂熟

```text
自动装配 → 生命周期 → 三级缓存 → 事务失效 → AOP 代理
```

---

## A 级（40%～70%）

| 排名 | 知识点 | 入口 |
|:----:|--------|------|
| 7 | Spring vs Spring Boot | [§7](./Spring高频面试题与知识点.md) |
| 8 | 事务传播 + 隔离 | [§8](./Spring高频面试题与知识点.md) |
| 9 | 作用域 + 单例线程安全 | [§9](./Spring高频面试题与知识点.md) |
| 10 | 构造器注入 vs 字段注入 | [§10](./Spring高频面试题与知识点.md) |
| 11 | MVC 执行流程 | [§11](./Spring高频面试题与知识点.md) |
| 12 | Boot 启动流程 | [§12](./Spring高频面试题与知识点.md) |
| 13 | 配置优先级 + Profile | [§13](./Spring高频面试题与知识点.md) |

---

## B 级（25%～45%）

14 自定义 Starter · 15 Filter/Interceptor/AOP · 16 BeanFactory vs ApplicationContext  
17 设计模式 · 18 内嵌 Tomcat · 19 事件 · 20 @Component vs @Bean  

→ 均见 [完整卷 B 级](./Spring高频面试题与知识点.md)

---

## C 级（&lt;25%）

refresh、BeanDefinition、FactoryBean、条件注解细节、Actuator、热部署、Boot 3.x 变化  

---

## 与全库关系

| 文档 | 作用 |
|------|------|
| [后端四档](./Java后端面试频率-四档.md) | P1 含 Spring |
| [Java SABC](./Java八股频率排序-SABC.md) | S7 Spring 核心 |
| [设计模式](./设计模式高频面试题与知识点.md) | Spring 中的模式 |

---

## 点名深挖

回复：`S1 自动装配` / `S3 三级缓存` / `S级可背诵模板` / `源码 refresh` 等。

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | Spring 专项频率表 2026 |
