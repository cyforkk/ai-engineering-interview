# Spring / Spring Boot · 面渣级长口述

<!-- NAV:START -->
> **导航串联**
>
> **系列：Java 后端主线**（12/46）
> - 上一篇：[Spring·知识点](./Spring高频面试题与知识点.md)
> - 下一篇：[设计模式·知识点](./设计模式高频面试题与知识点.md)
>
> **配对知识点：** [Spring·知识点](./Spring高频面试题与知识点.md)
>
> **返回：** [总索引](./README.md) · [串联地图](./学习地图-串联.md) · [路线图](./学习路线图-4到8周.md) · [架构图](./架构图集.md)
>
<!-- NAV:END -->

> 配套：[Spring高频面试题与知识点.md](./Spring高频面试题与知识点.md)  
> 每题 2～4 分钟

---

## P0 长口述

### 1. 什么是 IoC 和 DI

**口述：**

> IoC 是控制反转：对象该谁创建、依赖谁，不由业务代码自己 new 来控制，而是交给 Spring 容器。  
> DI 是依赖注入：容器把依赖通过构造器、setter 或字段塞进来。我更推荐**构造器注入**，依赖不可变、方便单测、避免循环依赖时的一些坑。  
> 好处是解耦：换实现只改配置或换 Bean，不用改一堆 new；对象生命周期统一管理，单例默认节省资源。  
> 没有 IoC 时，组件互相硬编码依赖，系统难测难换。

---

### 2. 什么是 AOP？和动态代理关系

**口述：**

> AOP 面向切面，把日志、事务、权限、限流这些横切逻辑从业务方法里抽出来，避免每个方法复制粘贴。  
> Spring AOP 运行时主要靠**动态代理**：目标方法前后插入增强。  
> 有接口时可以用 JDK 动态代理，基于接口生成代理对象；没有接口就用 CGLIB 生成子类。Spring Boot 2 以后默认更常走 CGLIB，但可以配置。  
> 通知类型有前置、后置、环绕、异常、最终。事务就是典型环绕增强。  
> 重要坑：**同类内部自调用**走的是 this，不是代理，切面不生效，事务也会失效。

---

### 3. JDK 动态代理和 CGLIB 区别

**口述：**

> JDK 代理要求目标实现接口，代理类实现同一接口，调用走 InvocationHandler。  
> CGLIB 通过继承目标类生成子类，拦截父类方法；所以 final 类或 final 方法拦不了。  
> 性能上各版本不同，现代差异没那么绝对，选型主要看有没有接口、类是否 final。  
> Spring 会根据情况选择，Boot 默认策略要了解，避免「为什么没走接口代理」的困惑。

---

### 4. @Transactional 失效场景（核心长答）

**口述：**

> Spring 事务本质是 AOP 代理：方法前开事务或加入事务，方法成功提交，异常回滚。底层通过事务管理器绑定连接。  
>
> 失效常见原因我按频率说：  
> **第一，同类自调用**：A 方法没加事务，内部 this.B()，B 有注解，不会走代理，事务不生效。解决：拆到另一个 Bean、注入自己、或用 AopContext。  
> **第二，方法不是 public**：Spring 默认基于代理，非 public 可能不加事务。  
> **第三，异常被吃掉**：自己 catch 了不抛，事务以为成功就提交。  
> **第四，抛的是受检异常**：默认只对 RuntimeException 和 Error 回滚，受检异常要配 rollbackFor=Exception.class。  
> **第五，数据库引擎不支持**，比如误用 MyISAM。  
> **第六，Bean 不是 Spring 管的**，自己 new 出来没有代理。  
> **第七，传播行为**配成不支持事务。  
> **第八，异步线程**：子线程拿不到主线程事务上下文。  
>
> 传播行为常考 REQUIRED：有事务就加入，没有就新建；REQUIRES_NEW：挂起当前，新开一个，适合日志这种「主事务回滚我也要记」的场景。

---

### 5. 三级缓存如何解决循环依赖

**口述：**

> 假设 A 依赖 B，B 依赖 A，都是单例字段或 setter 注入。  
> Spring 创建 A，实例化后还没填完属性，就先把 A 的早期引用放进三级缓存（ObjectFactory）。  
> 然后填充 A 的属性，发现需要 B，就去创建 B。  
> 创建 B 时要注入 A，此时一级二级还没有成品 A，就从三级缓存拿到 A 的早期引用（如果需要代理，会通过 ObjectFactory 生成），放进二级，B 注入这个 A。  
> B 创建完成进一级，回到 A 继续注入 B，A 完成进一级。  
>
> 为什么要三级？因为可能要注入的是**代理对象**，三级放工厂可以延迟生成正确的早期引用。  
> **构造器循环依赖解决不了**：A 构造需要 B 实例，B 构造又需要 A，创建阶段就卡死。只能改设计、@Lazy、或避免双向构造依赖。  
> prototype 作用域循环也不支持。

---

## P1 长口述

### 6. Bean 生命周期

**口述：**

> 我按顺序说：  
> 先实例化，再属性填充也就是依赖注入；  
> 然后各种 Aware 回调，让 Bean 感知容器；  
> 接着 BeanPostProcessor 前置处理；  
> 再初始化：@PostConstruct、InitializingBean、自定义 init-method；  
> 然后 BeanPostProcessor 后置，**AOP 代理常常在这里生成**；  
> 之后 Bean 就绪可使用；  
> 容器关闭时销毁：@PreDestroy、DisposableBean、destroy-method。  
>
> 单例在容器启动时创建（默认），原型每次 getBean 新建。  
> 单例 Bean 如果有可变状态，线程不安全要自己处理，容器不保证业务线程安全。

---

### 7. Spring MVC 处理一次请求

**口述：**

> 请求进 DispatcherServlet 前端控制器。  
> 它找 HandlerMapping 根据 URL 映射到 Controller 方法；  
> HandlerAdapter 真正调用该方法；  
> 返回值如果是视图就走视图解析渲染，如果是 @ResponseBody 就用消息转换器写成 JSON。  
> 拦截器在 Controller 前后执行 preHandle、postHandle、afterCompletion。  
> 异常可以由异常解析器或 @ControllerAdvice 统一处理。  
> Filter 是 Servlet 规范，比 Interceptor 更靠前，两者别混。

---

### 8. Spring Boot 自动配置原理

**口述：**

> 核心思想是约定优于配置。  
> @SpringBootApplication 包含组件扫描和 @EnableAutoConfiguration。  
> 启动时加载自动配置类，以前在 spring.factories，新版本在 AutoConfiguration.imports。  
> 每个自动配置类上有大量 @ConditionalOnClass、OnProperty、OnBean 等，类路径有某个类、配置开了某个项才生效。  
> starter 把依赖和自动配置打包，你引入 spring-boot-starter-web 就带上 MVC 和内嵌 Tomcat 等相关自动配置。  
> 我们仍可用 application.yml 覆盖默认值，或排除某个自动配置。

---

### 9. @Autowired 和 @Resource

**口述：**

> Autowired 是 Spring 注解，默认按类型注入，多个实现要 @Qualifier 或 @Primary。  
> Resource 是 JSR-250，默认按名称。  
> 我个人项目里更推荐构造器注入 + 必要的时候 Qualifier，依赖关系清晰。

---

## 场景口述

### 事务没回滚

> 先确认异常类型有没有抛出、是不是自调用、方法是否 public、是不是同一个库事务管理器。按失效清单逐项排查，比盲目加注解有用。

### 启动报循环依赖

> 看是否构造器循环；改成 setter/@Lazy 或拆模块。长期应用该解耦，而不是只靠三级缓存硬抗设计问题。

---

## 考前骨架

```text
IoC 容器管对象；AOP 代理横切
事务：代理+失效八条；REQUIRED vs REQUIRES_NEW
循环依赖：三级缓存；构造器不行
生命周期：实例化→注入→初始化→后置代理→销毁
Boot：条件装配+starter
MVC：DispatcherServlet 一条龙
```

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-20 | 面渣级长口述初版 |
