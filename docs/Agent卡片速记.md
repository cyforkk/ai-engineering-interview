# Agent / AI · 卡片速记

<!-- NAV:START -->
> [完整卷](./AI-Agent高频面试题与知识点.md) · [频率](./AI-Agent八股频率排序.md) · [面渣](./Agent面渣级口述.md)
<!-- NAV:END -->

> 遮住 A。**先 P0。**

---

## Agent

**Q1 Agent vs Chat？** A: 多步目标+工具行动 vs 单次生成。

**Q2 公式？** A: LLM+规划+记忆+工具+护栏。

**Q3 vs Workflow？** A: 动态选型 vs 步骤写死。

**Q4 ReAct？** A: Thought→Action→Observation。

**Q5 防死循环？** A: max_steps、去重、超时、熔断、HITL。

**Q6 谁执行工具？** A: 服务端；模型只出意图。

## RAG

**Q7 RAG 流程？** A: 切→嵌→存→检索→(重排)→生成。

**Q8 为何切？** A: 窗口与噪声；overlap 防切断。

**Q9 稠密 vs 稀疏？** A: 语义 vs 关键词精确。

**Q10 Rerank？** A: 粗召回后精排提质。

**Q11 防幻觉？** A: 引用、拒答、阈值、评测。

**Q12 Hybrid？** A: 向量+关键词通常更好。

## 工具 / 记忆 / 工程

**Q13 好 Tool？** A: 清晰名描述+严格 Schema。

**Q14 MCP？** A: 模型-工具上下文标准协议。

**Q15 记忆分层？** A: 短时窗口/工作状态/长期外存。

**Q16 评估 Agent？** A: 成功率、步数、成本、幻觉率。

**Q17 LangGraph？** A: 状态机循环、HITL、可恢复。

**Q18 成本优化？** A: 路由小模型、缓存、并行工具。

**Q19 Injection？** A: 最小权限、校验、审批、不信文档指令。

**Q20 微调 vs RAG？** A: 风格格式 vs 知识常变。

---

详解：[AI-Agent高频面试题与知识点.md](./AI-Agent高频面试题与知识点.md)

---

## P0 口述骨架（考前必背）

**Agent vs Chat vs Workflow（30 秒）：**  
Agent = 目标驱动多步 + 工具；Chat 主生成；Workflow 步骤写死更可控。  
**ReAct：** Thought→Action→Observation；max_steps/去重/熔断/HITL 防死循环。  
**RAG 防幻觉：** 切→嵌→检索→(重排)→生成；引用 + 低分拒答 + 金标。  
**工具：** Schema + 服务端鉴权；模型不可信。  
**易错：** 把 Agent 说成「多聊两句」；只靠 Prompt 防注入。

**链：** [完整卷](./AI-Agent高频面试题与知识点.md) · [面渣](./Agent面渣级口述.md) · [三故事](./加分-AI-必背三故事.md) · [结构图](./核心结构图.md)
