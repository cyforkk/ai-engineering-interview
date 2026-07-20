# Spring / Spring Boot · 高频面试

<!-- NAV:START -->
> **导航串联**
>
> **系列：Java 后端主线**（11/46）
> - 上一篇：[Redis·面渣](./Redis面渣级口述.md)
> - 下一篇：[Spring·面渣](./Spring面渣级口述.md)
>
> **配对面渣：** [Spring·面渣](./Spring面渣级口述.md)
>
> **相关专题：** [设计模式](./设计模式高频面试题与知识点.md) · [MySQL](./MySQL高频面试题与知识点.md)
>
> **返回：** [总索引](./README.md) · [串联地图](./学习地图-串联.md) · [路线图](./学习路线图-4到8周.md) · [架构图](./架构图集.md)
>
<!-- NAV:END -->

> **专题序：6 / 权重 P0**  
> 主线：IoC/AOP → **事务失效** → **三级缓存** → Bean 生命周期 → MVC/Boot  
> **面渣级长口述：** [Spring面渣级口述.md](./Spring面渣级口述.md)  
> 总索引：[README.md](./README.md)

---

## 一、优先级总览

| 级 | 模块 | 频率 |
|----|------|------|
| **P0** | IoC/DI、AOP/动态代理 | 极高 |
| **P0** | @Transactional 失效场景 | 极高 |
| **P0** | 循环依赖与三级缓存 | 极高 |
| **P1** | Bean 生命周期、MVC 流程 | 高 |
| **P1** | Boot 自动配置 | 高 |
| **P2** | 注解细节、Cloud 组件 | 中（按简历） |

---

## 二、P0 必会

### 2.1 IoC / DI / AOP

| 概念 | 一句话 |
|------|--------|
| IoC | 创建与依赖交给容器 |
| DI | 构造器/setter/字段注入（**推荐构造器**） |
| AOP | 横切（事务/日志/鉴权），运行时代理 |

**代理：** 有接口可 JDK；类代理 CGLIB。Boot2+ 常默认 CGLIB。  
**自调用：** 同类内部调用**不走代理** → 事务/AOP 失效。

**高频题：** IoC/AOP 是什么？JDK vs CGLIB？

---

### 2.2 事务失效（第一优先级背清单）

1. 非 public  
2. **同类自调用**  
3. 异常被吞  
4. 受检异常未 `rollbackFor`  
5. 引擎不支持事务  
6. 没走 Spring 代理（自己 new）  
7. 传播行为导致不开启  
8. 子线程无事务上下文  

**原理口述：** AOP 代理 + TransactionManager + 连接绑定线程。

**传播：** REQUIRED（默认）/ REQUIRES_NEW（常考对比）。

**高频题：** 失效场景？如何修自调用？REQUIRED vs REQUIRES_NEW？

---

### 2.3 三级缓存与循环依赖

| 级 | 内容 |
|----|------|
| 一 | 成品单例 |
| 二 | 早期对象 |
| 三 | ObjectFactory（可暴露代理早期引用） |

| 能解决 | 不能 |
|--------|------|
| 单例 + setter/字段循环 | **构造器循环**、prototype 循环 |

**高频题：** 三级缓存？为何要三级？构造器循环怎么办？

**口述：**  
> 半成品提前暴露破循环；构造器创建时就要对方，解不了，靠拆设计或 @Lazy。

---

## 三、P1 常考

### 3.1 Bean 生命周期（顺序）

```text
实例化 → 属性填充 → Aware
→ PostProcessor 前置 → 初始化(@PostConstruct等)
→ PostProcessor 后置(AOP) → 使用 → 销毁
```

作用域：singleton 默认；prototype 每次新。  
单例 Bean **不自动**线程安全。

### 3.2 MVC 一次请求

```text
DispatcherServlet → HandlerMapping → HandlerAdapter
→ Controller → 返回值处理（视图/JSON）
```

Filter（Servlet）更靠前；Interceptor 在 Spring MVC。

### 3.3 Boot 自动配置

- `@SpringBootApplication`  
- 自动配置类 + `@Conditional*`  
- starter = 依赖 + 自动配置  

**高频题：** 自动配置原理？starter？Bean 生命周期？MVC 流程？

### 3.4 注入注解

@Autowired（byType，Spring）vs @Resource（byName，JSR-250）。

---

## 四、P2 加分

| 点 | 一句话 |
|----|--------|
| @Async 失效 | 同类自调用、未 Enable |
| 设计模式 | 工厂、单例、代理、模板、观察者… |
| BeanFactory vs ApplicationContext | 后者更强（事件、国际等） |
| Cloud | 注册/配置/网关/限流（按简历） |

---

## 五、场景题

| 场景 | 查 |
|------|-----|
| 事务没回滚 | 失效清单 |
| 启动循环依赖报错 | 构造器？改注入 |
| 异步不生效 | 代理/@EnableAsync |

---

## 六、自测清单

### P0

- [ ] IoC/DI/AOP  
- [ ] 事务失效 5 条以上  
- [ ] 三级缓存能解决/不能解决  
- [ ] JDK vs CGLIB  

### P1

- [ ] Bean 生命周期顺序  
- [ ] MVC 流程  
- [ ] Boot 自动配置  
- [ ] Autowired vs Resource  

### P2

- [ ] @Async  
- [ ] 简历上的 Cloud 组件  

---

## 七、关联

[MySQL](./MySQL高频面试题与知识点.md) 隔离 · [并发](./并发高频面试题与知识点.md) · [Spring面渣](./Spring面渣级口述.md) · [README](./README.md)

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-20 | 初版 |
| 2026-07-20 | **事务失效+三级缓存置顶** |
