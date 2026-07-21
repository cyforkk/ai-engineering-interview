# Docker 与 Kubernetes · 面渣级口述（加长）

> [知识点](./Docker与K8s高频面试题与知识点.md)

---

## 一、Docker

镜像是只读分层模板，容器是镜像跑起来的进程组。  
解决「我机器能跑、你机器不行」：依赖打进镜像，环境一致。  
隔离靠 Linux Namespace 和 Cgroups，不是完整虚拟机，更轻。

---

## 二、K8s 为什么需要

容器多了要：调度到哪台机器、挂了谁拉起、如何对外服务、如何滚动发版、如何配资源限额。K8s 用声明式 API 做这些事。

---

## 三、核心对象（务必熟练）

**Pod**：最小调度单元，一个或多个容器共享网络与存储卷。  
**Deployment**：管 Pod 副本数与滚动更新、回滚。  
**Service**：给一组 Pod 稳定虚拟 IP/DNS，做负载均衡。  
**ConfigMap / Secret**：配置与密钥。  
**Ingress**：七层 HTTP 入口（常见搭配）。

**探针：**  
- liveness：死了重启  
- readiness：没准备好不接流量  

**资源：**  
- request：调度用，保证大致资源  
- limit：上限，防吵闹邻居；Java 还要考虑 cgroup 与 -Xmx 关系  

---

## 四、发布与排障

滚动更新：新版本 ready 再下旧版本。  
常见问题：ImagePullBackOff、CrashLoop（探针/启动失败）、OOMKilled（limit 或堆配置）、配置未挂载。  
排障：kubectl describe、logs、事件、资源使用。

---

## 五、和 Java 服务

容器内存 limit 限制的是进程 RSS。堆外、直接内存、元空间都算。  
只调大 -Xmx 可能仍被集群杀掉。探针接口要轻量。

---

## 收尾

面试够用：镜像容器、Pod/Deploy/Service、探针、request/limit、滚动发布；结合一次上线回滚经历。
