# Spring / Spring Boot · 高频八股知识点（完整卷）

<!-- NAV:START -->
> 📖 **Spring 完整卷** · 🗣️ [面渣](./Spring面渣级口述.md) · 🃏 [卡片](./Spring卡片速记.md) · 🔥 [频率导航](./Spring八股频率排序-SABC.md)
>
> [四档主线](./Java后端面试频率-四档.md) · [设计模式](./设计模式高频面试题与知识点.md)
>
<!-- NAV:END -->

> 结构图：[三级缓存](./核心结构图.md#3-spring-三级缓存循环依赖)



> 中小厂问得较多；大厂更爱结合项目深挖原理。  
> 超高频：**IoC/AOP + 生命周期 + 三级缓存 + 自动装配 + 事务**。

### 专项时间占比

| 优先级 | 模块 | 时间 |
|--------|------|:----:|
| **P0** | IoC/DI + AOP + 循环依赖 + 生命周期 + 自动装配 + @Transactional | **50%** |
| **P1** | 作用域/线程安全 + MVC + 设计模式 | **25%** |
| **P2** | 传播/隔离 + Filter/Interceptor + @Async | **15%** |
| **P3** | 源码细节 + 自定义 Starter + 条件注解 | **10%** |

### 高效准备

1. 每点四层：**是什么 + 为什么 + 怎么实现 + 项目怎么用**  
2. 循环依赖、自动装配、生命周期 **能画图**  
3. 事务失效准备 **5～6 个例子** + 踩坑  
4. 项目有事务/AOP/Starter/缓存 → 能展开讲  

---

# 一、超高频（几乎必问）

## 1. IoC / DI

### 1.1 什么是 IoC？什么是 DI？关系？

| 术语 | 含义 |
|------|------|
| **IoC** | 控制反转：对象创建与依赖关系的控制权交给容器 |
| **DI** | 依赖注入：容器把依赖「注入」到对象中 |

- **关系**：DI 是实现 IoC 的一种主要方式。  
- 没有容器时：业务自己 `new` 依赖 → 高层绑死低层。

### 1.2 IoC 解决了什么？如何降耦合？

- **解决**：对象创建、组装、生命周期管理散落在业务里，难测难换。  
- **降耦合**：面向接口；实现类由配置/扫描决定；单测可注入 Mock。  
- 扩展时改配置/换实现，少改调用方。

### 1.3 三种注入方式？官方推荐？

| 方式 | 优点 | 缺点 |
|------|------|------|
| **构造器** | 依赖必填、不可变、易测 | 参数多时臃肿 |
| Setter | 可选依赖灵活 | 可能半初始化 |
| 字段 `@Autowired` | 写着短 | 难测、隐藏依赖 |

- **推荐构造器注入**（Spring 团队与 IDEA 默认建议）。  
- 循环依赖时字段/setter 更「好写」，但构造器环更暴露设计问题。

### 1.4 @Autowired vs @Resource？

| | @Autowired | @Resource |
|--|------------|-----------|
| 来源 | Spring | JSR-250 |
| 默认 | **按类型** type | **按名称** name |
| 补充 | `@Qualifier` 指定名 | name 找不到可再按类型 |

### 1.5 @Component / @Service / @Repository / @Controller？

- 都是组件扫描的 stereotype，**功能上都能注册 Bean**。  
- 语义分工：  
  - `@Component`：通用  
  - `@Service`：业务层  
  - `@Repository`：持久层（可翻译数据访问异常）  
  - `@Controller` / `@RestController`：Web 层  

### 1.6 @Bean vs @Component？

| | @Component 等 | @Bean |
|--|---------------|-------|
| 位置 | 类上 | `@Configuration` 方法上 |
| 场景 | 自己写的类 | **第三方类**、需定制创建逻辑 |

---

## 2. AOP

### 2.1 核心概念？

| 概念 | 含义 |
|------|------|
| Aspect 切面 | 横切逻辑的模块（类） |
| Pointcut 切点 | 匹配哪些连接点 |
| Advice 通知 | 具体增强代码（何时执行） |
| JoinPoint 连接点 | 可被拦截的点（方法调用等） |
| Weaving 织入 | 把切面应用到目标对象 |

### 2.2 Spring AOP 实现原理？

- **运行时动态代理**（不是编译期改字节码为主）。  
- 容器为 Bean 创建代理；调用走代理 → 通知链 → 目标方法。

### 2.3 JDK 动态代理 vs CGLIB？

| | JDK | CGLIB |
|--|-----|-------|
| 原理 | 实现接口 | 继承类生成子类 |
| 条件 | **必须有接口** | 类非 final |
| Spring 选择 | 有接口可用 JDK | 无接口用 CGLIB |
| Boot 2.x+ | 常默认 `proxyTargetClass=true` 倾向 **CGLIB** | 可配置 |

### 2.4 通知类型？

| 注解 | 时机 |
|------|------|
| @Before | 方法前 |
| @After | 方法后（类似 finally） |
| @AfterReturning | 正常返回后 |
| @AfterThrowing | 抛异常后 |
| **@Around** | 环绕，最灵活 |

### 2.5 常见场景？

事务、日志、权限、缓存、耗时监控、幂等/限流切面等。

### 2.6 AspectJ vs Spring AOP？

| | Spring AOP | AspectJ |
|--|------------|---------|
| 能力 | 方法级、Bean 代理 | 更强（字段、构造等，编译/加载织入） |
| 复杂度 | 与 Spring 集成简单 | 更重 |
| 使用 | 企业应用够用 | 需要更强织入时 |

---

## 3. Bean 生命周期

### 3.1 完整流程（必须能背）

```text
1. 实例化 Instantiation
2. 属性填充 Populate（DI）
3. Aware 回调
4. BeanPostProcessor.postProcessBeforeInitialization
5. 初始化：
   · @PostConstruct
   · InitializingBean.afterPropertiesSet
   · 自定义 init-method
6. BeanPostProcessor.postProcessAfterInitialization
   · （AOP 代理常在此后置完成）
7. 使用中
8. 销毁：
   · @PreDestroy
   · DisposableBean.destroy
   · 自定义 destroy-method
```

### 3.2 BeanPostProcessor？

- 对 Bean **初始化前后**做扩展（包装、代理、注解处理）。  
- Spring 自身大量使用；AOP 与注解驱动依赖它。

### 3.3 初始化/销毁顺序（单例常规）

```text
@PostConstruct → afterPropertiesSet → init-method
...
@PreDestroy → destroy → destroy-method
```

（细节以版本与是否实现接口为准，面试按上述顺序说即可。）

### 3.4 常见 Aware？

| 接口 | 注入内容 |
|------|----------|
| BeanNameAware | Bean 名称 |
| BeanFactoryAware | BeanFactory |
| ApplicationContextAware | 应用上下文 |
| EnvironmentAware | Environment |
| EmbeddedValueResolverAware | 解析占位符等 |

---

## 4. 循环依赖（三级缓存）

### 4.1 三级缓存是什么？

| 级 | 名字 | 存什么 |
|----|------|--------|
| 一级 | singletonObjects | **成品**单例 |
| 二级 | earlySingletonObjects | **早期暴露**对象（可能未填完属性） |
| 三级 | singletonFactories | **ObjectFactory**，可生成早期引用（含代理） |

### 4.2 解决流程直觉（A→B→A）

1. 创建 A，把 A 的工厂放入**三级**  
2. 填充 A 需要 B → 创建 B  
3. B 需要 A → 从三级拿到 A 早期引用（必要时代理进二级）  
4. B 完成 → 一级  
5. A 完成 → 一级  

### 4.3 为什么要三级而不是两级？

- 循环依赖时才决定暴露 **原始对象还是 AOP 代理**。  
- 三级工厂延迟生成，避免「代理与否」不一致。  
- 一句话：**三级为了在循环依赖时正确暴露早期引用（尤其代理场景）**。

### 4.4 哪些解决不了？

- **构造器循环依赖**  
- **prototype** 作用域循环  
- 某些场景 + **@Async** 等提前代理/异步代理组合（易踩坑，面试提「构造器、原型不可解」为主）  
- 非单例环  

### 4.5 避免方式

- 重构依赖、构造器注入理清环、`@Lazy` 延迟一侧  

---

## 5. Spring Boot 自动装配

### 5.1 原理链路

```text
@SpringBootApplication
  └─ @EnableAutoConfiguration
       └─ AutoConfigurationImportSelector
            └─ 读取配置名单
                 · 旧：META-INF/spring.factories
                 · 新：META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
            └─ @ConditionalOnXXX 过滤
            └─ 注册自动配置 Bean
```

### 5.2 @SpringBootApplication 组成？

- `@SpringBootConfiguration`（本质 `@Configuration`）  
- `@EnableAutoConfiguration`  
- `@ComponentScan`  

### 5.3 自定义 Starter？

1. 自动配置类 + `@ConfigurationProperties`  
2. `@ConditionalOn...`  
3. 写入 `AutoConfiguration.imports`（或旧 factories）  
4. 可选 starter 模块只聚合依赖  

### 5.4 启动核心流程（抓主干）

```text
SpringApplication.run
 → 准备 Environment（配置）
 → 创建 ApplicationContext
 → 加载 Bean 定义 + 自动配置
 → refresh 容器
 → 启动内嵌 WebServer（Web 应用）
 → ApplicationRunner / CommandLineRunner
```

---

## 6. 事务管理

### 6.1 @Transactional 原理？

- **AOP 代理**：调用进入代理 → 开启/加入事务 → 执行方法 → 提交/回滚。  
- 同类 `this.xxx()` **不走代理** → 失效。

### 6.2 失效场景（至少 5～6 个）

| 场景 | 原因 |
|------|------|
| 方法非 public | 代理规则默认不管 |
| 同类内部调用 | 无代理 |
| 异常被 catch 吞掉 | 事务管理器看不到 |
| 检查异常默认不回滚 | 需 `rollbackFor` |
| 未进入 Spring 容器 | new 出来无代理 |
| 数据库引擎无事务（如误用 MyISAM） | 底层不支持 |
| 传播行为配置错误 | 语义不符预期 |
| 多线程中调用 | 事务绑定线程，子线程无事务上下文 |

### 6.3 传播行为（重点三）

| 传播 | 含义 |
|------|------|
| **REQUIRED**（默认） | 有则加入，无则新建 |
| **REQUIRES_NEW** | 挂起当前，**全新事务** |
| **NESTED** | 嵌套（保存点），与 NEW 不同 |

### 6.4 隔离级别？

- 与 DB 对应：读未提交 / 读已提交 / 可重复读 / 串行化。  
- 默认常 **跟随数据库**（MySQL InnoDB 默认 RR）。  

### 6.5 默认回滚策略？

- 默认：回滚 **RuntimeException** 与 **Error**。  
- 检查异常不回滚，除非：  
  ` @Transactional(rollbackFor = Exception.class) `  

---

# 二、高频

## 7. Bean 相关

### 7.1 作用域？

| 作用域 | 含义 |
|--------|------|
| **singleton**（默认） | 容器一个 |
| prototype | 每次 get 新实例 |
| request / session / application | Web |

### 7.2 单例是否线程安全？

- **默认不是**（若有可变成员状态）。  
- 无状态 Service 单例 OK。  
- 有状态：prototype、状态外置、并发安全结构。  

### 7.3 BeanFactory vs ApplicationContext？

| | BeanFactory | ApplicationContext |
|--|-------------|---------------------|
| 定位 | 基础容器 | 企业级上下文 |
| 加载 | 偏懒 | 启动初始化单例 |
| 功能 | 基本 IoC | 事件、AOP、国际化等 |

### 7.4 FactoryBean？

- `FactoryBean<T>`：容器 get 到的是 **`getObject()` 产物**，不是 Factory 本身。  
- 要 Factory 本身：`&beanName`。  
- 例：MyBatis `SqlSessionFactoryBean`。  

### 7.5 @Lazy？

- 延迟初始化；打破部分循环依赖；启动加速（非核心 Bean）。  

---

## 8. Spring MVC

### 8.1 完整流程

```text
请求 → DispatcherServlet
     → HandlerMapping 映射 Handler
     → 拦截器 preHandle
     → HandlerAdapter 调 Controller
     → 拦截器 postHandle
     → 返回值处理 / 视图解析 ViewResolver
     → 渲染
     → afterCompletion
```

### 8.2 三大件？

| 组件 | 作用 |
|------|------|
| HandlerMapping | URL → Handler |
| HandlerAdapter | 适配调用 Handler |
| ViewResolver | 逻辑视图 → 具体 View |

### 8.3 @RestController vs @Controller？

- `@RestController` = `@Controller` + `@ResponseBody`  
- 直接写响应体（JSON 等），不走视图名  

### 8.4 参数/返回值（了解）

- `HandlerMethodArgumentResolver` 解析参数  
- `HandlerMethodReturnValueHandler` 处理返回值  

---

## 9. 设计模式（Spring 中）

| 模式 | 体现 |
|------|------|
| 工厂 | BeanFactory |
| 单例 | 默认作用域 |
| 代理 | AOP |
| 模板方法 | JdbcTemplate、RestTemplate |
| 观察者 | ApplicationEvent |
| 策略 | Resource、多种视图等 |

---

## 10. 其他高频

### 10.1 Filter vs Interceptor

| | Filter | Interceptor |
|--|--------|-------------|
| 规范 | Servlet | Spring MVC |
| 时机 | 更靠前 | Handler 前后 |
| Bean | 需小心注入方式 | 易拿 Spring Bean |

### 10.2 @Async 为何不生效？

- 同类内部调用无代理  
- 未 `@EnableAsync`  
- 返回值/异常处理不当  
- 自行 new 对象  
- **正确**：独立 Bean + 启用异步 + 自定义线程池（别用简单默认）  

### 10.3 定时任务

- `@EnableScheduling` + `@Scheduled`（cron/fixedRate 等）  
- 集群下注意多实例重复执行（分布式锁/调度中心）  

### 10.4 Spring Cache

- `@EnableCaching` + `@Cacheable` / `@CachePut` / `@CacheEvict`  
- 抽象到 Redis/Caffeine 等  

---

# 三、中频

## 11. 条件注解

- `@ConditionalOnClass` / `OnMissingBean` / `OnProperty` 等  
- 自动装配是否生效的关键开关  

## 12. 配置优先级 + Profile

- 命令行 > 环境变量 > profile 配置 > 默认 application.yml（记「命令行最高」）  
- `spring.profiles.active`  

## 13. 事件机制

- `ApplicationEvent` + `@EventListener` / `ApplicationListener`  
- `publishEvent`；默认同步，可异步  

## 14. BeanDefinition

- Bean 的**定义元数据**（类名、作用域、依赖等）  
- 容器先注册 Definition，再实例化  

## 15. BeanFactoryPostProcessor vs BeanPostProcessor

| | BFPP | BPP |
|--|------|-----|
| 时机 | Bean **定义**加载后、实例化前 | Bean **实例**初始化前后 |
| 对象 | 改 BeanDefinition | 改/包装 Bean 实例 |

## 16. 编程式 vs 声明式事务

- 编程式：`TransactionTemplate` 代码控制  
- 声明式：`@Transactional` 代理（常用）  

## 17. 优雅停机 / 内嵌 Tomcat

- `server.shutdown=graceful` 等；等请求处理完再关  
- `ServletWebServerFactory` 创建内嵌容器  

---

# 四、低频 / 进阶加分

- `AbstractApplicationContext.refresh()` 主流程  
- 三级缓存源码细节  
- AOP 代理创建时机  
- Boot 3：Jakarta、自动配置 imports 变化  
- `@Configuration` **full**（CGLIB 增强，@Bean 方法调用走容器）vs **lite**  
- 自定义 `@Conditional`  
- 代理选择逻辑细节  

---

# 自测清单

### P0
- [ ] IoC/DI + 三种注入 + Autowired/Resource  
- [ ] AOP 概念 + JDK/CGLIB + 通知类型  
- [ ] 生命周期 8 步 + BPP  
- [ ] 三级缓存 + 不可解情况  
- [ ] 自动装配链路 + Application 三注解  
- [ ] 事务原理 + 失效 5 条 + REQUIRED/NEW/NESTED + 默认回滚  

### P1–P2
- [ ] 单例线程安全  
- [ ] MVC 流程  
- [ ] Filter vs Interceptor  
- [ ] @Async 失效  

**口述：** [Spring面渣级口述.md](./Spring面渣级口述.md)  
**卡片：** [Spring卡片速记.md](./Spring卡片速记.md)  
**频率：** [Spring八股频率排序-SABC.md](./Spring八股频率排序-SABC.md)  

---

## 点名深挖

- 三级缓存完整流程画图  
- 自动装配源码级  
- @Transactional 全部失效场景  
- Bean 生命周期完整顺序  

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 按超高/高/中/低频大纲重写 Spring 完整卷 |
