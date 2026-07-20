# LLMOps 与可观测 · 高频面试

<!-- NAV:START -->
> **导航**
>
> 📍 **AI工程** · 第 17/24 步 · [完整路径](./路径-AI工程.md)
> ← [8.LangGraph·述](./LangGraph与自研工作流面渣级口述.md)
> → [9.LLMOps·述](./LLMOps与可观测面渣级口述.md)
>
> 🎙 [面渣口述](./LLMOps与可观测面渣级口述.md)
>
> [首页](./README.md) · [AI路径](./路径-AI工程.md) · [Java路径](./路径-Java后端.md) · [Python路径](./路径-Python.md)
>
<!-- NAV:END -->

> **AI 工程岗 P0/P1**  
> **面渣口述：** [LLMOps与可观测面渣级口述.md](./LLMOps与可观测面渣级口述.md)  
> 总索引：[README.md](./README.md)

---

## 一、优先级

| 级 | 内容 |
|----|------|
| **P0** | 日志/指标/链路；request_id；token 与费用 |
| **P0** | 分阶段耗时（检索/模型/后处理） |
| **P1** | Prompt/模型版本；评测回归；灰度 |
| **P1** | 追踪工具概念（OpenTelemetry、Langfuse 等） |
| **P2** | 平台化、成本分摊、告警策略细节 |

---

## 二、P0 三大支柱

| 支柱 | LLM 场景要记什么 |
|------|------------------|
| Logs | prompt 版本、检索 id、错误码；**脱敏** |
| Metrics | QPS、延迟分位、错误率、token in/out、费用、缓存命中、拒答率 |
| Traces | 一次请求跨网关-服务-向量库-模型 的 span |

**request_id / trace_id：** 贯穿日志与用户反馈。

### 关键指标

| 指标 | 含义 |
|------|------|
| TTFT | 首 token 时间 |
| 总延迟 | e2e |
| 输入/输出 tokens | 成本 |
| 检索空率 | 数据/召回问题 |
| 工具失败率 | Agent |
| 人工接管率 | 产品 |

### 分阶段打点

```text
auth → cache → retrieve → rerank → prompt_build → llm → postprocess
```

---

## 三、P1 工程实践

| 点 | 说明 |
|----|------|
| 版本 | model_name、prompt_version、index_version |
| 回归 | 金标集 + 发版门槛 |
| 灰度 | 按租户/流量百分比 |
| 反馈 | 点赞点踩进数据集 |
| 告警 | 错误率、P99、费用突增、429 激增 |
| 抽样 | 存完整轨迹成本高，采样+出问题提升采样率 |

### 工具名词（简历写哪个深哪个）

- OpenTelemetry  
- Langfuse / Phoenix / LangSmith  
- Prometheus + Grafana  
- 云厂商监控  

---

## 四、高频题 TOP 12

1. LLM 服务要监控哪些指标？  
2. 如何定位「变慢了」？  
3. Prompt 改坏了怎么发现？  
4. 费用突增怎么查？  
5. 日志能打完整 Prompt 吗？  
6. 如何关联用户投诉到一次调用？  
7. Agent 轨迹如何观测？  
8. 多模型路由如何度量效果？  
9. 评测与线上指标如何结合？  
10. 采样策略？  
11. 跨服务 trace 怎么串？  
12. 讲一次靠观测定位的问题  

---

## 五、关联

[AI应用工程](./AI应用工程高频面试题与知识点.md) · [推理部署](./推理部署高频面试题与知识点.md) · [项目STAR](./项目面试STAR高频题与知识点.md)

---

## 修订

| 日期 | 说明 |
|------|------|
| 2026-07-21 | 初版 |
