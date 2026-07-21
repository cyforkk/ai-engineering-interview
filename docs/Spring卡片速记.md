# Spring · 卡片速记

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
