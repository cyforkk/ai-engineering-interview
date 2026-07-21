# -*- coding: utf-8 -*-
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"

REDIRECT = {
    "算法高频面试题与知识点.md": (
        "精简页",
        "算法面渣级口述.md",
        "算法高频30题代码册.md",
        "算法以面渣+30题代码册为准",
    ),
    "行为面试高频题与知识点.md": (
        "精简页",
        "行为面试面渣级口述.md",
        None,
        "请先读行为面渣口述",
    ),
    "RocketMQ高频面试题与知识点.md": (
        "精简页",
        "MQ高频面试题与知识点.md",
        "RocketMQ面渣级口述.md",
        "正文见 MQ 完整卷 + RocketMQ 面渣",
    ),
    "项目面试STAR高频题与知识点.md": (
        "精简页",
        "项目面试面渣级口述.md",
        "项目STAR范例-Java.md",
        "请先读项目面渣与 STAR 范例",
    ),
    "推理部署高频面试题与知识点.md": (
        "精简页",
        "推理部署面渣级口述.md",
        "AI-Agent高频面试题与知识点.md",
        "请先读面渣；体系见 AI 完整卷",
    ),
    "Kafka高频面试题与知识点.md": (
        "精简页",
        "MQ高频面试题与知识点.md",
        "Kafka面渣级口述.md",
        "正文见 MQ 完整卷 + Kafka 面渣",
    ),
    "Docker与K8s高频面试题与知识点.md": (
        "精简页",
        "Docker与K8s面渣级口述.md",
        None,
        "请先读 Docker/K8s 面渣",
    ),
    "LLMOps与可观测高频面试题与知识点.md": (
        "精简页",
        "LLMOps与可观测面渣级口述.md",
        "AI-Agent高频面试题与知识点.md",
        "请先读面渣；体系见 AI 完整卷",
    ),
    "AI评测金标SOP高频面试题与知识点.md": (
        "精简页",
        "AI评测金标SOP面渣级口述.md",
        "AI-Agent高频面试题与知识点.md",
        "请先读面渣；评估见 AI 完整卷",
    ),
    "Prompt工程高频面试题与知识点.md": (
        "精简页",
        "Prompt工程面渣级口述.md",
        "AI-Agent高频面试题与知识点.md",
        "请先读面渣；完整卷见 AI-Agent",
    ),
    "Agent高频面试题与知识点.md": (
        "入口页",
        "AI-Agent高频面试题与知识点.md",
        "Agent面渣级口述.md",
        "完整正文在 AI-Agent 完整卷",
    ),
    "LangGraph与自研工作流高频面试题与知识点.md": (
        "精简页",
        "LangGraph与自研工作流面渣级口述.md",
        "AI-Agent高频面试题与知识点.md",
        "请先读面渣；编排见 AI 完整卷",
    ),
    "Prompt注入与AI安全高频面试题与知识点.md": (
        "精简页",
        "Prompt注入与AI安全面渣级口述.md",
        "AI-Agent高频面试题与知识点.md",
        "请先读安全面渣",
    ),
    "向量库高频面试题与知识点.md": (
        "精简页",
        "向量库面渣级口述.md",
        "AI-Agent高频面试题与知识点.md",
        "请先读面渣；RAG 见 AI 完整卷",
    ),
    "AI应用工程高频面试题与知识点.md": (
        "精简页",
        "AI应用工程面渣级口述.md",
        "AI-Agent高频面试题与知识点.md",
        "请先读面渣",
    ),
    "MyBatis高频面试题与知识点.md": (
        "精简页",
        "MySQL高频面试题与知识点.md",
        None,
        "MyBatis 精简；SQL/事务深挖见 MySQL 完整卷",
    ),
    "设计模式高频面试题与知识点.md": (
        "精简页",
        "设计模式面渣级口述.md",
        "Spring高频面试题与知识点.md",
        "请先读面渣；Spring 中的模式见 Spring 卷",
    ),
    "微服务与分布式高频面试题与知识点.md": (
        "精简页",
        "微服务与分布式面渣级口述.md",
        "MQ高频面试题与知识点.md",
        "请先读面渣；消息可靠见 MQ 完整卷",
    ),
    "LLM基础常识高频面试题与知识点.md": (
        "精简页",
        "LLM基础常识面渣级口述.md",
        "AI-Agent高频面试题与知识点.md",
        "请先读面渣；体系见 AI-Agent 完整卷",
    ),
    "Elasticsearch高频面试题与知识点.md": (
        "精简页",
        "其他中间件八股频率排序.md",
        "MQ高频面试题与知识点.md",
        "ES 提纲；检索/中间件地图见链接",
    ),
    "Nginx高频面试题与知识点.md": (
        "精简页",
        "其他中间件八股频率排序.md",
        "计算机网络高频面试题与知识点.md",
        "Nginx 提纲；网络与中间件地图见链接",
    ),
    "Zookeeper高频面试题与知识点.md": (
        "精简页",
        "其他中间件八股频率排序.md",
        "微服务与分布式面渣级口述.md",
        "ZK 提纲；分布式面渣与中间件地图见链接",
    ),
}


def main():
    for name, (label, main, sec, tip) in REDIRECT.items():
        p = DOCS / name
        if not p.exists():
            print("missing", name)
            continue
        t = p.read_text(encoding="utf-8")
        if "本文是精简页" in t or "本文是入口页" in t:
            print("skip", name)
            continue
        main_title = main.replace(".md", "")
        sec_part = ""
        if sec:
            sec_title = sec.replace(".md", "")
            sec_part = f" · 另见：[{sec_title}](./{sec})"
        banner = (
            f"> ⚠️ **本文是{label}** — {tip}  \n"
            f"> 👉 主读：[{main_title}](./{main}){sec_part}\n\n"
        )
        if "<!-- NAV:END -->" in t:
            t = t.replace("<!-- NAV:END -->", "<!-- NAV:END -->\n\n" + banner, 1)
        else:
            lines = t.splitlines()
            if lines and lines[0].startswith("#"):
                t = lines[0] + "\n\n" + banner + "\n".join(lines[1:])
                if not t.endswith("\n"):
                    t += "\n"
            else:
                t = banner + t
        p.write_text(t, encoding="utf-8")
        print("banner", name)


if __name__ == "__main__":
    main()
