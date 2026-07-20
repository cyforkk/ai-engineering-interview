# -*- coding: utf-8 -*-
"""为 docs 下 Markdown 注入/更新「导航串联」块，实现专题逻辑串联。"""
from __future__ import annotations

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"

# 每个系列：有序文件名列表（相对于 docs/）
SERIES: dict[str, list[str]] = {
    "AI 工程主线": [
        "LLM基础常识高频面试题与知识点.md",
        "LLM基础常识面渣级口述.md",
        "Prompt工程高频面试题与知识点.md",
        "Prompt工程面渣级口述.md",
        "AI应用工程高频面试题与知识点.md",
        "AI应用工程面渣级口述.md",
        "AI评测金标SOP高频面试题与知识点.md",
        "AI评测金标SOP面渣级口述.md",
        "向量库高频面试题与知识点.md",
        "向量库面渣级口述.md",
        "Prompt注入与AI安全高频面试题与知识点.md",
        "Prompt注入与AI安全面渣级口述.md",
        "Agent高频面试题与知识点.md",
        "Agent面渣级口述.md",
        "LangGraph与自研工作流高频面试题与知识点.md",
        "LangGraph与自研工作流面渣级口述.md",
        "LLMOps与可观测高频面试题与知识点.md",
        "LLMOps与可观测面渣级口述.md",
        "推理部署高频面试题与知识点.md",
        "推理部署面渣级口述.md",
        "Docker与K8s高频面试题与知识点.md",
        "Docker与K8s面渣级口述.md",
    ],
    "Python 主线": [
        "Python高频面试题与知识点.md",
        "Python面渣级口述.md",
        "Python异步与FastAPI面渣级口述.md",
        "Python手写题.md",
        "追问三连-Python.md",
        "计算机网络高频面试题与知识点.md",
        "计算机网络面渣级口述.md",
        "AI应用工程高频面试题与知识点.md",
        "项目STAR范例-AI.md",
        "行为面试高频题与知识点.md",
    ],
    "Java 后端主线": [
        "Java高频面试题与知识点.md",
        "Java面渣级口述.md",
        "并发高频面试题与知识点.md",
        "并发面渣级口述.md",
        "JVM高频面试题与知识点.md",
        "JVM面渣级口述.md",
        "MySQL高频面试题与知识点.md",
        "MySQL面渣级口述.md",
        "Redis高频面试题与知识点.md",
        "Redis面渣级口述.md",
        "Spring高频面试题与知识点.md",
        "Spring面渣级口述.md",
        "设计模式高频面试题与知识点.md",
        "设计模式面渣级口述.md",
        "MQ高频面试题与知识点.md",
        "MQ面渣级口述.md",
        "Kafka高频面试题与知识点.md",
        "Kafka面渣级口述.md",
        "RocketMQ高频面试题与知识点.md",
        "RocketMQ面渣级口述.md",
        "微服务与分布式高频面试题与知识点.md",
        "微服务与分布式面渣级口述.md",
        "计算机网络高频面试题与知识点.md",
        "计算机网络面渣级口述.md",
        "操作系统高频面试题与知识点.md",
        "操作系统面渣级口述.md",
        "算法高频面试题与知识点.md",
        "算法面渣级口述.md",
        "算法高频30题代码册.md",
        "后端系统设计高频面试题与知识点.md",
        "后端系统设计面渣级口述.md",
        "系统设计口述-Feed流.md",
        "系统设计口述-搜索.md",
        "系统设计口述-延时消息.md",
        "系统设计口述-IM即时通讯.md",
        "系统设计口述-支付与幂等.md",
        "系统设计口述-配置中心.md",
        "Docker与K8s高频面试题与知识点.md",
        "Docker与K8s面渣级口述.md",
        "项目面试STAR高频题与知识点.md",
        "项目面试面渣级口述.md",
        "项目STAR范例-Java.md",
        "行为面试高频题与知识点.md",
        "行为面试面渣级口述.md",
        "追问三连-Java.md",
        "Java面试追问与手写题.md",
    ],
    "系统设计加长": [
        "后端系统设计高频面试题与知识点.md",
        "后端系统设计面渣级口述.md",
        "系统设计口述-Feed流.md",
        "系统设计口述-搜索.md",
        "系统设计口述-延时消息.md",
        "系统设计口述-IM即时通讯.md",
        "系统设计口述-支付与幂等.md",
        "系统设计口述-配置中心.md",
        "架构图集.md",
    ],
    "算法专项": [
        "算法高频面试题与知识点.md",
        "算法面渣级口述.md",
        "算法高频30题代码册.md",
        "Java面试追问与手写题.md",
        "Python手写题.md",
    ],
    "项目与软技能": [
        "项目面试STAR高频题与知识点.md",
        "项目面试面渣级口述.md",
        "项目STAR范例-AI.md",
        "项目STAR范例-Java.md",
        "行为面试高频题与知识点.md",
        "行为面试面渣级口述.md",
        "追问三连-AI.md",
        "学习路线图-4到8周.md",
        "学习地图-串联.md",
    ],
}

# 知识点 ↔ 面渣 配对（同目录相对链接）
PAIRS: list[tuple[str, str]] = [
    ("LLM基础常识高频面试题与知识点.md", "LLM基础常识面渣级口述.md"),
    ("Prompt工程高频面试题与知识点.md", "Prompt工程面渣级口述.md"),
    ("AI应用工程高频面试题与知识点.md", "AI应用工程面渣级口述.md"),
    ("AI评测金标SOP高频面试题与知识点.md", "AI评测金标SOP面渣级口述.md"),
    ("Agent高频面试题与知识点.md", "Agent面渣级口述.md"),
    ("向量库高频面试题与知识点.md", "向量库面渣级口述.md"),
    ("Prompt注入与AI安全高频面试题与知识点.md", "Prompt注入与AI安全面渣级口述.md"),
    ("LLMOps与可观测高频面试题与知识点.md", "LLMOps与可观测面渣级口述.md"),
    ("推理部署高频面试题与知识点.md", "推理部署面渣级口述.md"),
    ("LangGraph与自研工作流高频面试题与知识点.md", "LangGraph与自研工作流面渣级口述.md"),
    ("Python高频面试题与知识点.md", "Python面渣级口述.md"),
    ("Java高频面试题与知识点.md", "Java面渣级口述.md"),
    ("并发高频面试题与知识点.md", "并发面渣级口述.md"),
    ("JVM高频面试题与知识点.md", "JVM面渣级口述.md"),
    ("MySQL高频面试题与知识点.md", "MySQL面渣级口述.md"),
    ("Redis高频面试题与知识点.md", "Redis面渣级口述.md"),
    ("Spring高频面试题与知识点.md", "Spring面渣级口述.md"),
    ("设计模式高频面试题与知识点.md", "设计模式面渣级口述.md"),
    ("MQ高频面试题与知识点.md", "MQ面渣级口述.md"),
    ("Kafka高频面试题与知识点.md", "Kafka面渣级口述.md"),
    ("RocketMQ高频面试题与知识点.md", "RocketMQ面渣级口述.md"),
    ("微服务与分布式高频面试题与知识点.md", "微服务与分布式面渣级口述.md"),
    ("计算机网络高频面试题与知识点.md", "计算机网络面渣级口述.md"),
    ("操作系统高频面试题与知识点.md", "操作系统面渣级口述.md"),
    ("算法高频面试题与知识点.md", "算法面渣级口述.md"),
    ("后端系统设计高频面试题与知识点.md", "后端系统设计面渣级口述.md"),
    ("Docker与K8s高频面试题与知识点.md", "Docker与K8s面渣级口述.md"),
    ("项目面试STAR高频题与知识点.md", "项目面试面渣级口述.md"),
    ("行为面试高频题与知识点.md", "行为面试面渣级口述.md"),
]

# 额外相关链接（文件名 → [(标题, 文件), ...]）
RELATED: dict[str, list[tuple[str, str]]] = {
    "AI应用工程高频面试题与知识点.md": [
        ("向量库", "向量库高频面试题与知识点.md"),
        ("评测 SOP", "AI评测金标SOP高频面试题与知识点.md"),
        ("Agent", "Agent高频面试题与知识点.md"),
        ("安全", "Prompt注入与AI安全高频面试题与知识点.md"),
    ],
    "Agent高频面试题与知识点.md": [
        ("LangGraph 选型", "LangGraph与自研工作流高频面试题与知识点.md"),
        ("AI 应用工程", "AI应用工程高频面试题与知识点.md"),
        ("安全", "Prompt注入与AI安全高频面试题与知识点.md"),
    ],
    "向量库高频面试题与知识点.md": [
        ("AI 应用工程", "AI应用工程高频面试题与知识点.md"),
        ("搜索系统设计", "系统设计口述-搜索.md"),
    ],
    "JVM高频面试题与知识点.md": [
        ("并发", "并发高频面试题与知识点.md"),
        ("Docker/K8s", "Docker与K8s高频面试题与知识点.md"),
    ],
    "并发高频面试题与知识点.md": [
        ("JVM", "JVM高频面试题与知识点.md"),
        ("Java 基础", "Java高频面试题与知识点.md"),
    ],
    "Redis高频面试题与知识点.md": [
        ("MySQL", "MySQL高频面试题与知识点.md"),
        ("延时消息设计", "系统设计口述-延时消息.md"),
        ("支付幂等", "系统设计口述-支付与幂等.md"),
    ],
    "MySQL高频面试题与知识点.md": [
        ("Redis", "Redis高频面试题与知识点.md"),
        ("Spring 事务", "Spring高频面试题与知识点.md"),
    ],
    "Spring高频面试题与知识点.md": [
        ("设计模式", "设计模式高频面试题与知识点.md"),
        ("MySQL", "MySQL高频面试题与知识点.md"),
    ],
    "MQ高频面试题与知识点.md": [
        ("Kafka", "Kafka高频面试题与知识点.md"),
        ("RocketMQ", "RocketMQ高频面试题与知识点.md"),
        ("延时消息", "系统设计口述-延时消息.md"),
    ],
    "Kafka高频面试题与知识点.md": [
        ("MQ 通用", "MQ高频面试题与知识点.md"),
        ("RocketMQ", "RocketMQ高频面试题与知识点.md"),
    ],
    "RocketMQ高频面试题与知识点.md": [
        ("MQ 通用", "MQ高频面试题与知识点.md"),
        ("Kafka", "Kafka高频面试题与知识点.md"),
        ("支付", "系统设计口述-支付与幂等.md"),
    ],
    "Python异步与FastAPI面渣级口述.md": [
        ("Python 基础", "Python高频面试题与知识点.md"),
        ("AI 应用", "AI应用工程高频面试题与知识点.md"),
        ("LLMOps", "LLMOps与可观测高频面试题与知识点.md"),
    ],
    "计算机网络面渣级口述.md": [
        ("知识点", "计算机网络高频面试题与知识点.md"),
        ("OS·epoll", "操作系统面渣级口述.md"),
        ("Docker/K8s", "Docker与K8s高频面试题与知识点.md"),
    ],
    "操作系统面渣级口述.md": [
        ("知识点", "操作系统高频面试题与知识点.md"),
        ("网络·面渣", "计算机网络面渣级口述.md"),
        ("并发", "并发高频面试题与知识点.md"),
    ],
    "推理部署高频面试题与知识点.md": [
        ("Docker/K8s", "Docker与K8s高频面试题与知识点.md"),
        ("LLMOps", "LLMOps与可观测高频面试题与知识点.md"),
    ],
    "项目STAR范例-AI.md": [
        ("STAR 模板", "项目面试STAR高频题与知识点.md"),
        ("AI 应用", "AI应用工程高频面试题与知识点.md"),
    ],
    "项目STAR范例-Java.md": [
        ("STAR 模板", "项目面试STAR高频题与知识点.md"),
        ("JVM 排查", "JVM面渣级口述.md"),
    ],
    "学习路线图-4到8周.md": [
        ("串联地图", "学习地图-串联.md"),
        ("总索引", "README.md"),
    ],
    "README.md": [
        ("串联地图", "学习地图-串联.md"),
        ("路线图", "学习路线图-4到8周.md"),
        ("架构图集", "架构图集.md"),
    ],
}

NAV_START = "<!-- NAV:START -->"
NAV_END = "<!-- NAV:END -->"
NAV_RE = re.compile(
    re.escape(NAV_START) + r".*?" + re.escape(NAV_END) + r"\n*",
    re.DOTALL,
)


def title_of(filename: str) -> str:
    t = filename.replace(".md", "")
    t = t.replace("高频面试题与知识点", "·知识点")
    t = t.replace("面渣级长口述", "·面渣")
    t = t.replace("面渣级口述", "·面渣")
    return t.strip(" ·") or filename


def pair_line(fname: str) -> str:
    for a, b in PAIRS:
        if fname == a:
            return f"**配对面渣：** [{title_of(b)}](./{b})"
        if fname == b:
            return f"**配对知识点：** [{title_of(a)}](./{a})"
    return ""


def build_nav(fname: str) -> str:
    """为文件生成导航块（可属于多个系列时都列出）。"""
    blocks: list[str] = []
    for series_name, files in SERIES.items():
        if fname not in files:
            continue
        i = files.index(fname)
        prev_f = files[i - 1] if i > 0 else None
        next_f = files[i + 1] if i + 1 < len(files) else None
        step = f"{i + 1}/{len(files)}"
        lines = [
            f"**系列：{series_name}**（{step}）",
        ]
        if prev_f:
            lines.append(f"- 上一篇：[{title_of(prev_f)}](./{prev_f})")
        else:
            lines.append("- 上一篇：无（本系列起点）")
        if next_f:
            lines.append(f"- 下一篇：[{title_of(next_f)}](./{next_f})")
        else:
            lines.append("- 下一篇：无（本系列终点）→ 可回 [总索引](./README.md)")
        blocks.append("\n".join(lines))

    pair = pair_line(fname)
    rel = RELATED.get(fname, [])
    rel_parts = [f"[{t}](./{f})" for t, f in rel]

    body: list[str] = ["> **导航串联**"]
    if blocks:
        body.append(">")
        for bi, b in enumerate(blocks):
            for line in b.splitlines():
                body.append(f"> {line}")
            if bi < len(blocks) - 1:
                body.append(">")
    if pair:
        body.append(">")
        body.append(f"> {pair}")
    if rel_parts:
        body.append(">")
        body.append(f"> **相关专题：** {' · '.join(rel_parts)}")
    body.append(">")
    body.append(
        "> **返回：** [总索引](./README.md) · [串联地图](./学习地图-串联.md) · [路线图](./学习路线图-4到8周.md) · [架构图](./架构图集.md)"
    )
    body.append(">")

    return NAV_START + "\n" + "\n".join(body) + "\n" + NAV_END + "\n\n"


def inject_file(path: Path, fname: str) -> bool:
    text = path.read_text(encoding="utf-8")
    nav = build_nav(fname)
    # 不在串联系列且无配对/相关，跳过（除了地图自身）
    if (
        fname not in {f for files in SERIES.values() for f in files}
        and fname not in RELATED
        and not pair_line(fname)
    ):
        return False

    if NAV_START in text:
        new_text = NAV_RE.sub(nav, text, count=1)
    else:
        # 插在第一个一级标题之后
        m = re.search(r"^# .+$", text, re.M)
        if not m:
            new_text = nav + text
        else:
            insert_at = m.end()
            # 跳过标题后空行
            rest = text[insert_at:]
            new_text = text[:insert_at] + "\n\n" + nav + rest.lstrip("\n")
            if not new_text.startswith(text[:insert_at]):
                pass

    if new_text != text:
        with path.open("w", encoding="utf-8", newline="\n") as f:
            f.write(new_text)
        return True
    return False


def main() -> None:
    changed = 0
    # 所有 SERIES + RELATED + PAIRS 中的文件
    names = set()
    for files in SERIES.values():
        names.update(files)
    names.update(RELATED.keys())
    for a, b in PAIRS:
        names.add(a)
        names.add(b)

    for fname in sorted(names):
        path = DOCS / fname
        if not path.is_file():
            print("missing:", fname)
            continue
        if inject_file(path, fname):
            changed += 1
            print("updated:", fname)
    print(f"done, changed={changed}")


if __name__ == "__main__":
    main()
