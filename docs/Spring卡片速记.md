# Spring · 卡片速记

<!-- NAV:START -->
> [完整卷](./Spring高频面试题与知识点.md) · [频率](./Spring八股频率排序-SABC.md) · [面渣](./Spring面渣级口述.md)
<!-- NAV:END -->

> 遮住 A。**先 P0。**

---

## IoC / DI

**Q1 IoC vs DI？** A: 控制反转；DI 是实现方式之一。

**Q2 推荐注入？** A: 构造器注入。

**Q3 Autowired vs Resource？** A: 按类型 vs 按名称。

**Q4 @Bean vs @Component？** A: 方法声明第三方/定制 vs 类扫描。

**Q5 四层 stereotype？** A: Component/Service/Repository/Controller 语义分工。

## AOP

**Q6 核心概念？** A: Aspect/Pointcut/Advice/JoinPoint/Weaving。

**Q7 原理？** A: 运行时动态代理。

**Q8 JDK vs CGLIB？** A: 接口 vs 子类；Boot 常偏 CGLIB。

**Q9 通知类型？** A: Before/After/Around/AfterReturning/AfterThrowing。

## 生命周期

**Q10 主干？** A: 实例化→注入→Aware→BPP前→初始化→BPP后→使用→销毁。

**Q11 初始化顺序？** A: PostConstruct→afterPropertiesSet→init-method。

**Q12 BPP？** A: 初始化前后扩展；AOP 常用后置。

## 循环依赖

**Q13 三级缓存？** A: 成品/早期对象/工厂。

**Q14 为何三级？** A: 延迟暴露，正确处理代理。

**Q15 解不了？** A: 构造器环、prototype。

## 自动装配

**Q16 链路？** A: EnableAutoConfiguration→imports/factories→Conditional→注册。

**Q17 Application 三注解？** A: Configuration + EnableAutoConfiguration + ComponentScan。

**Q18 自定义 Starter？** A: 自动配置+属性+Conditional+imports。

## 事务

**Q19 原理？** A: AOP 代理。

**Q20 失效？** A: this调用、非public、吞异常、检查异常、无容器。

**Q21 REQUIRED vs NEW？** A: 加入已有 vs 新开。

**Q22 默认回滚？** A: RuntimeException/Error；检查异常要 rollbackFor。

## 高频

**Q23 单例线程安全？** A: 有状态不安全；无状态 Service OK。

**Q24 MVC 核心？** A: DispatcherServlet→Mapping→Adapter→View。

**Q25 RestController？** A: Controller+ResponseBody。

**Q26 Filter vs Interceptor？** A: Servlet 前 vs Handler 前后。

**Q27 @Async 失效？** A: 同类调用、未 Enable、无代理。

**Q28 BFPP vs BPP？** A: 改定义 vs 改实例。

**Q29 FactoryBean？** A: getObject 产物；& 取工厂本身。

**Q30 Spring 模式？** A: 工厂单例代理模板观察者策略。

---

详解：[Spring高频面试题与知识点.md](./Spring高频面试题与知识点.md)
