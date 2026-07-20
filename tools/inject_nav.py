# -*- coding: utf-8 -*-
"""注入简洁导航：只挂一条主路径的上一步/下一步 + 配对链接。"""
from __future__ import annotations

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"

# 主路径：每个文件只属于一条（避免多系列混乱）
# 格式：有序 (文件名, 显示名)
PATH_AI: list[tuple[str, str]] = [
    ("LLM基础常识高频面试题与知识点.md", "1.LLM基础·知"),
    ("LLM基础常识面渣级口述.md", "1.LLM基础·述"),
    ("Prompt工程高频面试题与知识点.md", "2.Prompt·知"),
    ("Prompt工程面渣级口述.md", "2.Prompt·述"),
    ("AI应用工程高频面试题与知识点.md", "3.AI应用·知"),
    ("AI应用工程面渣级口述.md", "3.AI应用·述"),
    ("AI评测金标SOP高频面试题与知识点.md", "4.评测·知"),
    ("AI评测金标SOP面渣级口述.md", "4.评测·述"),
    ("向量库高频面试题与知识点.md", "5.向量库·知"),
    ("向量库面渣级口述.md", "5.向量库·述"),
    ("Prompt注入与AI安全高频面试题与知识点.md", "6.安全·知"),
    ("Prompt注入与AI安全面渣级口述.md", "6.安全·述"),
    ("Agent高频面试题与知识点.md", "7.Agent·知"),
    ("Agent面渣级口述.md", "7.Agent·述"),
    ("LangGraph与自研工作流高频面试题与知识点.md", "8.LangGraph·知"),
    ("LangGraph与自研工作流面渣级口述.md", "8.LangGraph·述"),
    ("LLMOps与可观测高频面试题与知识点.md", "9.LLMOps·知"),
    ("LLMOps与可观测面渣级口述.md", "9.LLMOps·述"),
    ("推理部署高频面试题与知识点.md", "10.推理·知"),
    ("推理部署面渣级口述.md", "10.推理·述"),
    ("Docker与K8s高频面试题与知识点.md", "11.K8s·知"),
    ("Docker与K8s面渣级口述.md", "11.K8s·述"),
    ("项目STAR范例-AI.md", "12.STAR·AI"),
    ("行为面试面渣级口述.md", "13.行为面·述"),
]

PATH_JAVA: list[tuple[str, str]] = [
    ("Java高频面试题与知识点.md", "1.Java·知"),
    ("Java面渣级口述.md", "1.Java·述"),
    ("并发高频面试题与知识点.md", "2.并发·知"),
    ("并发面渣级口述.md", "2.并发·述"),
    ("JVM高频面试题与知识点.md", "3.JVM·知"),
    ("JVM面渣级口述.md", "3.JVM·述"),
    ("MySQL高频面试题与知识点.md", "4.MySQL·知"),
    ("MySQL面渣级口述.md", "4.MySQL·述"),
    ("Redis高频面试题与知识点.md", "5.Redis·知"),
    ("Redis面渣级口述.md", "5.Redis·述"),
    ("Spring高频面试题与知识点.md", "6.Spring·知"),
    ("Spring面渣级口述.md", "6.Spring·述"),
    ("设计模式高频面试题与知识点.md", "7.设计模式·知"),
    ("设计模式面渣级口述.md", "7.设计模式·述"),
    ("MQ高频面试题与知识点.md", "8.MQ·知"),
    ("Kafka高频面试题与知识点.md", "8b.Kafka·知"),
    ("RocketMQ高频面试题与知识点.md", "8c.RocketMQ·知"),
    ("微服务与分布式高频面试题与知识点.md", "9.微服务·知"),
    ("计算机网络面渣级口述.md", "10.网络·述"),
    ("操作系统面渣级口述.md", "11.OS·述"),
    ("算法高频30题代码册.md", "12.算法代码"),
    ("后端系统设计面渣级口述.md", "13.系统设计"),
    ("系统设计口述-Feed流.md", "13a.Feed"),
    ("系统设计口述-搜索.md", "13b.搜索"),
    ("系统设计口述-延时消息.md", "13c.延时"),
    ("系统设计口述-IM即时通讯.md", "13d.IM"),
    ("系统设计口述-支付与幂等.md", "13e.支付"),
    ("项目STAR范例-Java.md", "14.STAR·Java"),
    ("行为面试面渣级口述.md", "15.行为面·述"),
]

PATH_PYTHON: list[tuple[str, str]] = [
    ("Python高频面试题与知识点.md", "1.Python·知"),
    ("Python面渣级口述.md", "1.Python·述"),
    ("Python异步与FastAPI面渣级口述.md", "2.FastAPI·述"),
    ("Python手写题.md", "3.手写"),
    ("追问三连-Python.md", "4.追问"),
    ("计算机网络面渣级口述.md", "5.网络·述"),
    ("AI应用工程高频面试题与知识点.md", "6.AI应用·知"),
    ("项目STAR范例-AI.md", "7.STAR·AI"),
    ("行为面试面渣级口述.md", "8.行为面·述"),
]

PATHS = {
    "AI工程": (PATH_AI, "路径-AI工程.md"),
    "Java后端": (PATH_JAVA, "路径-Java后端.md"),
    "Python": (PATH_PYTHON, "路径-Python.md"),
}

# 文件 → 主路径名（先登记的优先，避免多路径打架）
PRIMARY: dict[str, str] = {}
for path_name, (steps, _) in PATHS.items():
    for fname, _ in steps:
        if fname not in PRIMARY:
            PRIMARY[fname] = path_name

PAIRS = {
    "LLM基础常识高频面试题与知识点.md": "LLM基础常识面渣级口述.md",
    "Prompt工程高频面试题与知识点.md": "Prompt工程面渣级口述.md",
    "AI应用工程高频面试题与知识点.md": "AI应用工程面渣级口述.md",
    "AI评测金标SOP高频面试题与知识点.md": "AI评测金标SOP面渣级口述.md",
    "Agent高频面试题与知识点.md": "Agent面渣级口述.md",
    "向量库高频面试题与知识点.md": "向量库面渣级口述.md",
    "Prompt注入与AI安全高频面试题与知识点.md": "Prompt注入与AI安全面渣级口述.md",
    "LLMOps与可观测高频面试题与知识点.md": "LLMOps与可观测面渣级口述.md",
    "推理部署高频面试题与知识点.md": "推理部署面渣级口述.md",
    "LangGraph与自研工作流高频面试题与知识点.md": "LangGraph与自研工作流面渣级口述.md",
    "Python高频面试题与知识点.md": "Python面渣级口述.md",
    "Java高频面试题与知识点.md": "Java面渣级口述.md",
    "并发高频面试题与知识点.md": "并发面渣级口述.md",
    "JVM高频面试题与知识点.md": "JVM面渣级口述.md",
    "MySQL高频面试题与知识点.md": "MySQL面渣级口述.md",
    "Redis高频面试题与知识点.md": "Redis面渣级口述.md",
    "Spring高频面试题与知识点.md": "Spring面渣级口述.md",
    "设计模式高频面试题与知识点.md": "设计模式面渣级口述.md",
    "MQ高频面试题与知识点.md": "MQ面渣级口述.md",
    "Kafka高频面试题与知识点.md": "Kafka面渣级口述.md",
    "RocketMQ高频面试题与知识点.md": "RocketMQ面渣级口述.md",
    "微服务与分布式高频面试题与知识点.md": "微服务与分布式面渣级口述.md",
    "计算机网络高频面试题与知识点.md": "计算机网络面渣级口述.md",
    "操作系统高频面试题与知识点.md": "操作系统面渣级口述.md",
    "算法高频面试题与知识点.md": "算法面渣级口述.md",
    "后端系统设计高频面试题与知识点.md": "后端系统设计面渣级口述.md",
    "Docker与K8s高频面试题与知识点.md": "Docker与K8s面渣级口述.md",
    "项目面试STAR高频题与知识点.md": "项目面试面渣级口述.md",
    "行为面试高频题与知识点.md": "行为面试面渣级口述.md",
}
PAIR_REV = {v: k for k, v in PAIRS.items()}

NAV_START = "<!-- NAV:START -->"
NAV_END = "<!-- NAV:END -->"
NAV_RE = re.compile(
    re.escape(NAV_START) + r".*?" + re.escape(NAV_END) + r"\n*",
    re.DOTALL,
)


def build_nav(fname: str) -> str | None:
    path_name = PRIMARY.get(fname)
    lines = ["> **导航**"]

    if path_name:
        steps, path_file = PATHS[path_name]
        files = [f for f, _ in steps]
        labels = {f: lab for f, lab in steps}
        i = files.index(fname)
        prev_f = files[i - 1] if i > 0 else None
        next_f = files[i + 1] if i + 1 < len(files) else None
        lines.append(f">")
        lines.append(f"> 📍 **{path_name}** · 第 {i + 1}/{len(files)} 步 · [完整路径](./{path_file})")
        if prev_f:
            lines.append(f"> ← [{labels[prev_f]}](./{prev_f})")
        if next_f:
            lines.append(f"> → [{labels[next_f]}](./{next_f})")
        else:
            lines.append(f"> → 本路径结束 · [回首页](./README.md)")

    if fname in PAIRS:
        lines.append(f">")
        lines.append(f"> 🎙 [面渣口述](./{PAIRS[fname]})")
    elif fname in PAIR_REV:
        lines.append(f">")
        lines.append(f"> 📘 [知识点](./{PAIR_REV[fname]})")

    lines.append(f">")
    lines.append(f"> [首页](./README.md) · [AI路径](./路径-AI工程.md) · [Java路径](./路径-Java后端.md) · [Python路径](./路径-Python.md)")
    lines.append(">")

    # 无路径也无配对的也生成极简导航
    if not path_name and fname not in PAIRS and fname not in PAIR_REV:
        if fname in (
            "README.md",
            "路径-AI工程.md",
            "路径-Java后端.md",
            "路径-Python.md",
            "学习路线图-4到8周.md",
            "学习地图-串联.md",
            "架构图集.md",
        ):
            return (
                NAV_START
                + "\n"
                + "> **导航**\n"
                + ">\n"
                + "> [首页](./README.md) · [AI路径](./路径-AI工程.md) · [Java路径](./路径-Java后端.md) · [Python路径](./路径-Python.md) · [路线图](./学习路线图-4到8周.md)\n"
                + ">\n"
                + NAV_END
                + "\n\n"
            )
        return None

    return NAV_START + "\n" + "\n".join(lines) + "\n" + NAV_END + "\n\n"


def inject(path: Path, fname: str) -> bool:
    nav = build_nav(fname)
    if not nav:
        # 清除旧的复杂导航
        text = path.read_text(encoding="utf-8")
        if NAV_START in text:
            new_text = NAV_RE.sub("", text, count=1)
            if new_text != text:
                with path.open("w", encoding="utf-8", newline="\n") as f:
                    f.write(new_text)
                return True
        return False

    text = path.read_text(encoding="utf-8")
    if NAV_START in text:
        new_text = NAV_RE.sub(nav, text, count=1)
    else:
        m = re.search(r"^# .+$", text, re.M)
        if not m:
            new_text = nav + text
        else:
            insert_at = m.end()
            new_text = text[:insert_at] + "\n\n" + nav + text[insert_at:].lstrip("\n")

    if new_text != text:
        with path.open("w", encoding="utf-8", newline="\n") as f:
            f.write(new_text)
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(DOCS.rglob("*.md")):
        if "archive" in path.parts:
            continue
        rel = path.relative_to(DOCS).as_posix()
        if path.name.startswith("_"):
            continue
        if inject(path, path.name if "/" not in rel else path.name):
            # use path.name only for top-level
            pass
    # only top-level md in docs/
    for path in sorted(DOCS.glob("*.md")):
        if path.name.startswith("_"):
            continue
        if inject(path, path.name):
            changed += 1
            print("ok", path.name)
    print("changed", changed)


if __name__ == "__main__":
    main()
