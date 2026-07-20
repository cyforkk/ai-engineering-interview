# Docker 与 Kubernetes · 高频面试

> **后端 / AI 部署 P1**  
> **面渣口述：** [Docker与K8s面渣级口述.md](./Docker与K8s面渣级口述.md)  
> 总索引：[README.md](./README.md)

---

## 一、优先级

| 级 | Docker | K8s |
|----|--------|-----|
| **P0** | 镜像/容器/Dockerfile 层缓存 | Pod、Deployment、Service |
| **P0** | 与虚拟机区别 | 探针、资源 request/limit |
| **P1** | 多阶段构建、网络、卷 | Ingress、ConfigMap/Secret、HPA |
| **P2** | 安全、镜像精简 | StatefulSet、调度、服务网格概念 |

---

## 二、Docker P0

| 概念 | 说明 |
|------|------|
| 镜像 | 只读分层模板 |
| 容器 | 镜像运行实例 |
| Dockerfile | 构建脚本；注意层缓存与 `.dockerignore` |
| 与 VM | 容器共享宿主机内核，更轻 |

### Dockerfile 实践

- 多阶段构建减小镜像  
- 非 root 用户  
- 固定基础镜像版本  
- AI：模型权重常挂卷或启动下载，不塞进巨大镜像（视策略）  

---

## 三、K8s P0/P1

| 对象 | 作用 |
|------|------|
| Pod | 最小调度单元，可多容器 |
| Deployment | 无状态副本、滚动更新 |
| Service | 稳定虚拟 IP/DNS 访问 Pod |
| Ingress | HTTP 路由入口 |
| ConfigMap/Secret | 配置与密钥 |
| PVC | 持久卷声明 |

### 探针

| 探针 | 作用 |
|------|------|
| liveness | 死了重启 |
| readiness | 没就绪不接流量 |
| startup | 慢启动保护 |

### 资源

- requests：调度保证  
- limits：上限，防打爆节点  
- AI GPU：`nvidia.com/gpu` 等资源扩展  

### HPA

按 CPU/自定义指标扩缩副本；推理可看队列长度或 QPS。

---

## 四、高频题 TOP 20

1. 容器和虚拟机区别？  
2. 镜像分层？  
3. 如何减小镜像？  
4. Pod 是什么？  
5. Service 解决什么？  
6. Deployment 滚动更新过程？  
7. 就绪探针和存活探针区别？  
8. request 和 limit？  
9. 配置如何注入？  
10. 密钥如何管理？  
11. 如何暴露服务到集群外？  
12. HPA 原理直观理解？  
13. 容器 CPU throttle？  
14. 优雅下线？  
15. 与 JVM / 内存的关系（限内存）？  
16. sidecar 是什么？  
17. 命名空间？  
18. 调度失败常见原因？  
19. GPU  Pod 注意点？  
20. 讲一次容器化踩坑  

---

## 五、与 Java / AI 交叉

| 场景 | 点 |
|------|-----|
| JVM | 容器内存感知、MaxRAMPercentage、OOMKilled |
| FastAPI | 多 worker 与多 Pod 选择 |
| 推理 | GPU 调度、模型卷、滚动更新冷启动 |

---

## 六、关联

[推理部署](./推理部署高频面试题与知识点.md) · [JVM](./JVM高频面试题与知识点.md) · [微服务](./微服务与分布式高频面试题与知识点.md)

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 初版 |
