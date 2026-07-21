# -*- coding: utf-8 -*-
"""Spring/Spring Boot 高频八股完整卷 + 频率排序。不碰面渣。"""
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"


def w(name, text):
    p = DOCS / name
    p.write_text(text.strip() + "\n", encoding="utf-8")
    print(name, p.stat().st_size)


NAV = """<!-- NAV:START -->
> 📖 **Spring 八股** · 🗣️ [面渣](./Spring面渣级口述.md) · 🃏 [卡片](./Spring卡片速记.md) · 🔥 [频率SABC](./Spring八股频率排序-SABC.md)
>
> [模块总览](./Java八股模块总览.md) · [后端四档](./Java后端面试频率-四档.md) · [路径](./路径-Java后端.md)
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md)
>
<!-- NAV:END -->
"""

SPRING = f"""# Spring / Spring Boot · 高频八股知识点（完整卷）

{NAV}

> 2025–2026 面试频率：S 级几乎必问。格式：**题 + 核心要点**；能背流程、会对比、懂为什么。  
> 练嘴 → [Spring面渣级口述.md](./Spring面渣级口述.md)

### 复习优先级（Spring 专项）

```text
S：自动装配 → Bean 生命周期 → 三级缓存 → IoC/DI → AOP → @Transactional 失效
A：Boot 区别、事务传播、作用域、构造器注入、MVC、启动、配置优先级
B/C：Starter、Filter/Interceptor、设计模式、源码细节…
```

---

# S 级（出现率 70%+ · 必须滚瓜烂熟）

## 1. Spring Boot 自动装配原理？（★★★★★ 排名第 1）

### 先结论

Boot 通过 **自动配置类 + 条件注解**，根据 classpath 与配置 **自动装配 Bean**，实现「约定优于配置」。

### 核心链路

```text
@SpringBootApplication
  └─ @EnableAutoConfiguration
       └─ AutoConfigurationImportSelector
            └─ 加载自动配置类名单
                 · 旧：META-INF/spring.factories
                 · 新：META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
            └─ 过滤 + @ConditionalOnXXX 判断是否生效
            └─ 生效的配置类向容器注册 Bean
```

### 关键点

| 点 | 说明 |
|----|------|
| Starter | 聚合依赖 + 常配合自动配置 |
| @ConditionalOnClass | classpath 有某类才生效 |
| @ConditionalOnMissingBean | 用户没定义才提供默认 Bean |
| @ConditionalOnProperty | 配置项满足才生效 |
| 可覆盖 | 自己定义同类型 Bean 常可覆盖默认 |

### 面试怎么答（结构）

1. 入口注解  
2. ImportSelector 导入自动配置  
3. factories/imports 列表  
4. Conditional 条件过滤  
5. 举例：有 `DataSource` 类 + 配了 url 才装配数据源  

---

## 2. Bean 生命周期？（★★★★★ 必须能背完整流程）

### 主干流程（按顺序说）

```text
1. 实例化 Instantiation（构造 / 工厂方法）
2. 属性填充 Populate（依赖注入）
3. Aware 回调
   · BeanNameAware
   · BeanFactoryAware
   · ApplicationContextAware …
4. BeanPostProcessor.postProcessBeforeInitialization
5. 初始化
   · @PostConstruct
   · InitializingBean.afterPropertiesSet
   · 自定义 init-method
6. BeanPostProcessor.postProcessAfterInitialization
   · （AOP 代理常在此后置阶段完成）
7. Bean 就绪，使用中
8. 销毁
   · @PreDestroy
   · DisposableBean.destroy
   · 自定义 destroy-method
```

### 加分

- 工厂方法 / `@Bean` 也有类似回调顺序。  
- `BeanPostProcessor` 是扩展核心（AOP、注解处理）。  
- 单例在容器启动期创建（默认）；原型每次 get 新建。

---

## 3. 循环依赖 + 三级缓存？（★★★★★）

### 什么是循环依赖

A 依赖 B，B 依赖 A（或更长环）。

### 三级缓存分别是什么

| 缓存 | 存什么 | 作用 |
|------|--------|------|
| 一级 `singletonObjects` | 完整单例 | 成品 |
| 二级 `earlySingletonObjects` | 早期暴露的半成品（已实例化，可能未填完属性） | 避免重复创建 |
| 三级 `singletonFactories` | 对象工厂（可生成早期引用，含 AOP 时生产代理） | **为循环依赖暴露引用** |

### 解决流程直觉（A→B→A）

1. 创建 A，把 A 的工厂放入 **三级缓存**  
2. 填充 A 属性需要 B → 去创建 B  
3. 创建 B，B 依赖 A → 从三级缓存拿到 A 的早期引用（必要时变代理进二级）  
4. B 完成 → 放入一级  
5. A 继续完成 → 放入一级  

### 为什么需要三级？二级不够？

- 仅二级：难优雅处理「早期对象还要不要做成 **AOP 代理**」。  
- 三级放 **ObjectFactory**：真正被循环引用时再决定暴露原始对象还是代理，保证最终注入的是一致引用。  
- 面试一句话：**三级为了在循环依赖时延迟生成早期引用（尤其代理）**。

### 哪些解决不了？

- **构造器循环依赖**（创建都完不成）→ 通常失败  
- **原型 prototype** 循环依赖 → 不支持同样机制  
- 非单例场景  

### 怎么避免

- 构造器注入打断环（设计上更清晰）  
- 重构依赖、`@Lazy` 延迟一侧  

---

## 4. IoC / DI 原理？（★★★★★）

### 概念

| 术语 | 含义 |
|------|------|
| **IoC** | 控制反转：对象创建与依赖关系交给容器，而不是业务自己 `new` |
| **DI** | 依赖注入：容器把依赖「塞进」对象 |

### 注入方式对比

| 方式 | 优点 | 缺点 |
|------|------|------|
| **构造器注入** | 依赖必填、不可变、易测、无隐藏 NPE | 参数多时构造臃肿 |
| Setter | 可选依赖灵活 | 可能半初始化 |
| 字段 `@Autowired` | 写着省事 | 难测、隐藏依赖、IDE 常警告 |

**推荐构造器注入**（Spring 团队与 IDEA 默认建议）。

### @Autowired vs @Resource

| | @Autowired | @Resource |
|--|------------|-----------|
| 来源 | Spring | JSR-250 |
| 默认 | **按类型** | **按名称** |
| 必填 | `required` 可调 | — |

---

## 5. AOP 原理？（★★★★☆）

### 是什么

面向切面：把日志、事务、权限等 **横切逻辑** 与业务解耦。

### 动态代理

| | JDK 动态代理 | CGLIB |
|--|--------------|-------|
| 原理 | 实现接口，InvocationHandler | 继承目标类，子类拦截 |
| 条件 | **必须有接口** | 类不能 final、方法最好非 final |
| Spring | 有接口时可用 JDK | 无接口用 CGLIB |

- Spring Boot 2.x 起许多场景 **默认倾向 CGLIB**（可配置 `proxyTargetClass`）。  
- **自调用**（`this.xxx()`）不走代理 → 事务/AOP 失效。

### 通知类型（了解）

Before / After / AfterReturning / AfterThrowing / Around。  
执行顺序与 `@Order`、切面优先级相关（面试提 Around 最强可控即可）。

---

## 6. @Transactional 失效场景？（★★★★☆）

| 场景 | 原因 |
|------|------|
| **同类 this 调用** | 不经过代理 |
| 方法 **非 public** | 默认代理规则可能扫不到 |
| **异常被 catch 吞掉** | 事务管理器看不到异常 |
| 默认只回滚 **RuntimeException/Error** | 检查异常需 `rollbackFor` |
| 数据库引擎不支持事务（如错误使用 MyISAM） | 存储层不支持 |
| 传播行为理解错 | 如 `NOT_SUPPORTED` 等 |
| 未进入 Spring 管理（new 出来的对象） | 无代理 |

### 标准答法

先说「本质是 AOP 代理」，再列 4～5 条失效场景 + 对应修法（抽到别的 Bean、抛出异常、rollbackFor、public 等）。

---

# A 级（出现率 40%～70%）

## 7. Spring 与 Spring Boot 的区别？

| | Spring | Spring Boot |
|--|--------|-------------|
| 配置 | XML/注解偏多，手工装配多 | **约定优于配置** |
| 依赖 | 自己选版本、排冲突 | **Starter** 管理依赖 |
| 运行 | 常外部 Tomcat | **内嵌容器**，jar 直接跑 |
| 能力 | IoC/AOP/事务等核心 | 自动配置 + 生产就绪增强 |

- Boot = Spring 生态上的 **快速开发框架**，不是替换 Spring。

---

## 8. 事务传播行为 + 隔离级别？

### 常用传播

| 传播 | 含义 |
|------|------|
| **REQUIRED**（默认） | 有事务加入，无则新建 |
| **REQUIRES_NEW** | 挂起当前，**全新事务** |
| **NESTED** | 嵌套（保存点），与 REQUIRES_NEW 不同 |
| SUPPORTS / MANDATORY / NEVER / NOT_SUPPORTED | 了解 |

### 隔离级别

- 与数据库隔离级别对应：读未提交 / 读已提交 / 可重复读 / 串行化。  
- Spring 可配置；**默认常跟随底层数据库**（MySQL InnoDB 默认 RR）。  
- 脏读、不可重复读、幻读概念能对上即可。

---

## 9. Bean 作用域 + 单例是否线程安全？

| 作用域 | 含义 |
|--------|------|
| **singleton**（默认） | 容器一个实例 |
| prototype | 每次 get 新实例 |
| request / session / application | Web 环境 |

- **单例 Bean 默认不是线程安全的**（若有可变成员状态）。  
- 有状态：改 prototype、或状态外置（ThreadLocal 慎用）、或并发安全结构。  
- 无状态 Service 单例是常态。

---

## 10. 构造器注入 vs 字段注入？

- 推荐 **构造器**：依赖不可变、强制注入、便于单测 `new Service(mock)`。  
- 字段注入：反射注入，测试麻烦，循环依赖「看起来好写」但掩盖设计问题。  
- IDEA 警告字段注入 = 推动最佳实践。

---

## 11. Spring MVC 执行流程？

```text
请求 → DispatcherServlet
     → HandlerMapping 找到 Handler
     → HandlerAdapter 执行 Controller
     → 返回 ModelAndView / 响应体
     → ViewResolver 解析视图（若需）
     → 渲染响应
```

- 过滤器 Filter 在 Servlet 前；拦截器 Interceptor 在 Handler 前后。

---

## 12. Spring Boot 启动流程？（关键步骤）

```text
SpringApplication.run()
  → 创建 SpringApplication
  → 推导应用类型（Servlet/Reactive）
  → 加载 ApplicationContextInitializer / Listener
  → 准备 Environment（配置文件）
  → 创建 ApplicationContext
  → 准备上下文（Banner、Bean 定义加载等）
  → refresh 容器（注册 Bean、自动配置生效）
  → 启动内嵌 WebServer（若 Web）
  → 发布运行事件、Runner 回调
```

- 面试抓：**Environment → 创建上下文 → refresh → 内嵌容器**。

---

## 13. 配置文件优先级 + Profile？

- 常见：命令行 > 环境变量 > `application-{{profile}}.yml` > `application.yml` 等（完整优先级表很长，记「命令行最高、profile 覆盖默认」）。  
- `spring.profiles.active=dev` 激活多环境。  
- 同 key：高优先级覆盖低优先级。

---

# B 级（25%～45%）

## 14. 自定义 Starter？

1. 建模块：自动配置类 + 属性类 `@ConfigurationProperties`  
2. 条件注解控制生效  
3. 注册：  
   - Boot 2.7+：`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`  
   - 旧：`spring.factories`  
4. 可选：再做一个 `xxx-spring-boot-starter` 只引依赖  

---

## 15. Filter、Interceptor、AOP 区别？

| | Filter | Interceptor | AOP |
|--|--------|-------------|-----|
| 规范 | Servlet | Spring MVC | Spring |
| 粒度 | 请求进出 | Controller 前后 | 方法切面 |
| 顺序 | 更靠前 | Mapping 之后 | Bean 方法调用 |

场景：鉴权/日志可用 Filter 或 Interceptor；事务/细粒度业务增强用 AOP。

---

## 16. BeanFactory vs ApplicationContext？

| | BeanFactory | ApplicationContext |
|--|-------------|---------------------|
| 定位 | 容器基础接口 | 更完整的企业级上下文 |
| 加载 | 偏懒加载 | 启动时初始化单例 |
| 功能 | 基本 IoC | 事件、国际化、AOP 集成等 |

开发几乎都用 **ApplicationContext**。

---

## 17. Spring 中的设计模式？

| 模式 | 体现 |
|------|------|
| 工厂 | BeanFactory |
| 单例 | 默认 Bean 作用域 |
| 代理 | AOP |
| 模板方法 | JdbcTemplate、RestTemplate |
| 观察者 | ApplicationEvent |
| 策略 | 多种 Resource 等 |

---

## 18. 内嵌 Tomcat 如何启动？

- Web 应用：`ServletWebServerFactory` 创建 `WebServer`  
- `refresh` 后启动 Tomcat，映射 DispatcherServlet  
- 打包成可执行 jar，`main` 直接跑  

---

## 19. Spring 事件机制？

- 定义 `ApplicationEvent` 子类  
- `ApplicationListener` 或 `@EventListener`  
- `ApplicationEventPublisher.publishEvent`  
- 默认同步；可配置异步  

---

## 20. @Component vs @Bean？

| | @Component（及 Service 等） | @Bean |
|--|------------------------------|-------|
| 位置 | 类上 | 配置类方法上 |
| 场景 | 自己写的类 | 第三方类、需定制实例化 |

---

# C 级（偶尔深挖）

- `AbstractApplicationContext.refresh()` 主流程、BeanDefinition  
- FactoryBean vs BeanFactory  
- 条件注解实现细节  
- Actuator  
- 热部署  
- Boot 3：Jakarta 命名空间、AOT/Native Image 了解  

---

# 自测清单（S 级）

- [ ] 自动装配链路 5 步能说清  
- [ ] Bean 生命周期 8 步不漏  
- [ ] 三级缓存各自作用 + 构造器环不可解  
- [ ] 构造器注入为什么更好  
- [ ] JDK 代理 vs CGLIB  
- [ ] 事务失效至少 5 条  

**口述：** [Spring面渣级口述.md](./Spring面渣级口述.md)  
**卡片：** [Spring卡片速记.md](./Spring卡片速记.md)  
**频率表：** [Spring八股频率排序-SABC.md](./Spring八股频率排序-SABC.md)  

---

## 可继续（点名）

1. S 级前 6 题 **可背诵标准答模板**  
2. 三级缓存 **源码级**  
3. 自动装配 **源码跟读**  
4. MVC / 启动流程 **逐步展开**  

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | Spring 完整卷：S/A/B/C 全覆盖 |
"""

RANK = f"""# Spring / Spring Boot · 频率排名（2026）

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
"""

CARDS = f"""# Spring · 卡片速记

<!-- NAV:START -->
> [完整卷](./Spring高频面试题与知识点.md) · [频率](./Spring八股频率排序-SABC.md) · [面渣](./Spring面渣级口述.md)
<!-- NAV:END -->

> 遮住 A。**先刷 S 级。**

---

## S 级

**Q1 自动装配链路？**  
A: EnableAutoConfiguration → ImportSelector → factories/imports → Conditional → 注册Bean。

**Q2 Bean 生命周期主干？**  
A: 实例化→属性注入→Aware→BPP前→初始化→BPP后→使用→销毁。

**Q3 三级缓存？**  
A: 一级成品；二级早期对象；三级工厂（循环时暴露，可代理）。

**Q4 构造器环？**  
A: 三级缓存解决不了构造器循环依赖。

**Q5 为何要三级？**  
A: 延迟创建早期引用，正确处理AOP代理。

**Q6 IoC/DI？**  
A: 容器管创建装配；依赖由容器注入。

**Q7 推荐哪种注入？**  
A: 构造器注入。

**Q8 @Autowired vs @Resource？**  
A: 默认按类型 vs 按名称。

**Q9 JDK代理 vs CGLIB？**  
A: 接口 vs 子类；Boot常默认CGLIB倾向。

**Q10 事务失效 4 条？**  
A: this调用、非public、吞异常、检查异常未rollbackFor。

---

## A 级

**Q11 Spring vs Boot？**  
A: Boot=约定+Starter+自动配置+内嵌容器。

**Q12 REQUIRED vs REQUIRES_NEW？**  
A: 加入已有事务 vs 新开事务。

**Q13 单例线程安全？**  
A: 默认否（有状态时）；无状态Service可单例。

**Q14 MVC 核心？**  
A: DispatcherServlet→Mapping→Adapter→ViewResolver。

**Q15 启动抓什么？**  
A: Environment→建上下文→refresh→内嵌服务器。

---

## B 级

**Q16 自定义Starter？**  
A: 自动配置类+Conditional+imports/factories。

**Q17 Filter vs Interceptor？**  
A: Servlet层 vs SpringMVC Handler前后。

**Q18 BeanFactory vs ApplicationContext？**  
A: 基础容器 vs 功能完整上下文。

**Q19 @Component vs @Bean？**  
A: 自有类注解 vs 方法声明第三方/定制Bean。

---

详解：[Spring高频面试题与知识点.md](./Spring高频面试题与知识点.md)
"""


def patch_nav():
    # overview
    ov = DOCS / "Java八股模块总览.md"
    if ov.exists():
        t = ov.read_text(encoding="utf-8")
        if "Spring八股频率" not in t:
            t = t.replace(
                "| 4 Spring | [Spring](./Spring高频面试题与知识点.md) |",
                "| 4 **Spring 完整卷** | [Spring](./Spring高频面试题与知识点.md) · [频率](./Spring八股频率排序-SABC.md) |",
            )
            ov.write_text(t, encoding="utf-8")
            print("overview")

    # path
    path = DOCS / "路径-Java后端.md"
    if path.exists():
        t = path.read_text(encoding="utf-8")
        if "Spring八股频率" not in t:
            t = t.replace(
                "[Spring八股](./Spring高频面试题与知识点.md)",
                "[Spring八股](./Spring高频面试题与知识点.md)·[频率](./Spring八股频率排序-SABC.md)",
            )
            # other pattern
            t = t.replace(
                "| [Spring](./Spring面渣级口述.md) | [Spring八股](./Spring高频面试题与知识点.md) |",
                "| [Spring](./Spring面渣级口述.md) | [Spring完整卷](./Spring高频面试题与知识点.md) · [频率](./Spring八股频率排序-SABC.md) |",
            )
            path.write_text(t, encoding="utf-8")
            print("path")

    # sidebar
    sb = DOCS / "_sidebar.md"
    if sb.exists():
        t = sb.read_text(encoding="utf-8")
        if "Spring八股频率" not in t:
            t = t.replace(
                "  * [Spring](Spring高频面试题与知识点.md) · [卡片](Spring卡片速记.md)\n",
                "  * [Spring完整卷](Spring高频面试题与知识点.md) · [频率](Spring八股频率排序-SABC.md) · [卡片](Spring卡片速记.md)\n",
            )
            sb.write_text(t, encoding="utf-8")
            print("sidebar")

    # four tier
    ft = DOCS / "Java后端面试频率-四档.md"
    if ft.exists():
        t = ft.read_text(encoding="utf-8")
        if "Spring八股频率" not in t:
            t = t.replace(
                "| [Spring](./Spring高频面试题与知识点.md) · [面渣](./Spring面渣级口述.md) |",
                "| [Spring完整卷](./Spring高频面试题与知识点.md) · [频率](./Spring八股频率排序-SABC.md) · [面渣](./Spring面渣级口述.md) |",
            )
            ft.write_text(t, encoding="utf-8")
            print("fourtier")


def main():
    w("Spring高频面试题与知识点.md", SPRING)
    w("Spring八股频率排序-SABC.md", RANK)
    w("Spring卡片速记.md", CARDS)
    patch_nav()


if __name__ == "__main__":
    main()
