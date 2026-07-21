# Spring / Spring Boot · 高频八股知识点

<!-- NAV:START -->
> 📖 **八股知识点** · 🗣️ [面渣](./Spring面渣级口述.md) · 🃏 [卡片](./Spring卡片速记.md)
>
> [首页](./README.md) · [如何使用](./如何使用本仓库.md) · [Java路径](./路径-Java后端.md) · [模块总览](./Java八股模块总览.md)
>
<!-- NAV:END -->


> 中小厂高频，大厂也问原理。口语 → [面渣](./Spring面渣级口述.md)。

---

## 1. IoC / DI？BeanFactory vs ApplicationContext？

- **IoC**：控制反转，创建装配交给容器。  
- **DI**：依赖注入（构造器推荐 / setter / 字段）。  
- **BeanFactory**：容器基础接口，偏懒加载。  
- **ApplicationContext**：更完整（事件、国际、AOP 等），企业开发常用。

---

## 2. Bean 生命周期？（要能串）

主干（口述顺序）：

1. 实例化  
2. 属性填充（依赖注入）  
3. Aware 回调（BeanName/BeanFactory/ApplicationContext…）  
4. BeanPostProcessor **前置**  
5. InitializingBean / `@PostConstruct` / init-method  
6. BeanPostProcessor **后置**（AOP 代理常在此阶段完成）  
7. 使用中  
8. `@PreDestroy` / DisposableBean / destroy-method  

---

## 3. AOP 原理？JDK 动态代理 vs CGLIB？

- 横切：事务、日志、鉴权。  
- **JDK 动态代理**：基于接口。  
- **CGLIB**：基于子类（无接口时）。  
- Spring Boot 2.x 起常默认偏向 CGLIB（可配置）。  
- **自调用**不走代理 → 事务/AOP 失效。

---

## 4. 事务传播行为？失效场景？

### 常用传播

| 传播 | 含义 |
|------|------|
| REQUIRED（默认） | 有事务加入，无则新建 |
| REQUIRES_NEW | 挂起当前，新建事务 |
| NESTED | 嵌套（保存点） |
| SUPPORTS / NOT_SUPPORTED / MANDATORY / NEVER | 了解 |

### 失效常见原因

- 同类内部调用（无代理）  
- 方法非 public  
- 异常被吞未抛出  
- 抛检查异常默认不回滚（需 `rollbackFor`）  
- 传播/只读配置理解错误  

---

## 5. Spring Boot 自动配置原理？

- `@SpringBootApplication` 含 `@EnableAutoConfiguration`。  
- 加载自动配置类：  
  - 旧：`META-INF/spring.factories`  
  - 新：`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`  
- **条件注解**（`@ConditionalOnClass` 等）决定是否生效。  
- starter 聚合依赖 + 自动配置。

---

## 6. @Autowired vs @Resource？

| | @Autowired | @Resource |
|--|------------|-----------|
| 来源 | Spring | JSR-250 |
| 默认 | 按类型 | 按名称 |
| 必填 | required 可调 | — |

---

## 7. 循环依赖？三级缓存？（高频）

- 单例 **字段/setter** 注入：三级缓存可解决。  
  - 提前暴露「早期引用」，打断环。  
- **构造器循环依赖**：创建都完不成，**通常无法解决**。  
- 原型 bean 循环依赖也不支持同样机制。  
- 面试：说清「为何能解 / 不能解」比背字段名更重要。

---

## 8. 过滤器 vs 拦截器？

- Filter：Servlet 规范，更靠前。  
- Interceptor：Spring MVC，可访问 Handler 信息。

---

# 自测

- [ ] Bean 生命周期主干  
- [ ] 事务失效 4 条  
- [ ] 自动配置加载位置  
- [ ] 循环依赖边界  

**口述：** [Spring面渣级口述.md](./Spring面渣级口述.md) · **卡片：** [Spring卡片速记.md](./Spring卡片速记.md)
