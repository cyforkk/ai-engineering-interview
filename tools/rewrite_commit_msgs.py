# -*- coding: utf-8 -*-
"""git filter-branch --msg-filter 用：按首行英文标题映射为中文提交说明。"""
import sys

MAPPING = {
    "Initialize interview knowledge base as git repository.": """初始化面试知识库为 Git 仓库。

纳入 docs 面试专题与 .gitignore，完成首次版本入库。
""",
    "Complete interview kit: new topics, root docs, and public-ready index.": """补齐面试题库：新增专题、根目录文档与公开就绪索引。

增加设计模式、算法、项目 STAR、微服务等指南及面渣口述；添加根 README 与 MIT 协议；刷新 docs 总索引。
""",
    "Rebrand as AI engineering interview kit and add Python plus AI app tracks.": """定位升级为 AI 工程面试库，并增加 Python 与 AI 应用轨道。

仓库定位调整为 ai-engineering-interview；补充 Python 与 AI 应用工程知识点与口述；更新根目录与 docs 多轨道索引。
""",
    "Add FastAPI async deep dive, vector DB, AI security, and split follow-ups.": """补充 FastAPI 异步深挖、向量库、AI 安全与分轨追问。

扩展 Python 异步与 FastAPI 口述；新增向量库与 Prompt 注入安全专册；追问三连拆为 Java、Python、AI 三轨；刷新索引。
""",
    "Fill remaining interview gaps: LLM basics, ops, design, and roadmap.": """补齐剩余缺口：LLM 基础、运维可观测、系统设计与路线图。

新增 LLM 常识与 Prompt 工程、Python 手写与 STAR 范例、LLMOps 与推理部署、系统设计与 Docker/K8s，以及 4～8 周学习路线图。
""",
    "Add system-design orals, MQ product books, LangGraph, behavioral, and diagrams.": """增加系统设计口述、MQ 产品专册、LangGraph、行为面试与架构图。

扩展 Feed/搜索/延时设计口述；新增 Kafka 与 RocketMQ 专册；补充 LangGraph 与自研工作流对比、HR 行为面试短册；归档旧口述并加入架构图集。
""",
    "添加 Docsify 静态站点与 Netlify 部署配置。": """添加 Docsify 静态站点与 Netlify 部署配置。

用 Docsify 将 docs 下 Markdown 渲染为可浏览站点，配置侧栏、搜索与 Mermaid；增加 netlify.toml 与 SPA 回退，便于一键部署到 Netlify。
""",
}


def main() -> None:
    msg = sys.stdin.read()
    lines = msg.strip().splitlines()
    first = lines[0] if lines else ""
    out = MAPPING.get(first, msg)
    if not out.endswith("\n"):
        out += "\n"
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
