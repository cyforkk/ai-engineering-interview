# tools/ 维护说明

本目录多为 **一次性/半自动生成脚本**，用于历史批量扩写知识点、卡片、频率卷。

## ⚠️ 默认不要重跑

下列脚本可能 **覆盖** 你在 `docs/` 里已手工加厚、改链接、加版本锚的 Markdown：

| 脚本 | 风险 |
|------|------|
| `gen_*_baguwen.py` / `gen_*_freq_full.py` | 高：整卷重写 |
| `gen_knowledge_*.py` / `thicken_*.py` | 高：批量改知识点/面渣 |
| `gen_cards_all.py` | 中：卡片重生成 |
| `inject_nav.py` | 中：改 NAV 区块 |
| `inject_thin_banners.py` | 低：仅补 ⚠️ 横幅（可重复） |
| `check_md_links.py` | 无：只检查链接 |
| `rewrite_commit_msgs.py` | 与文档内容无关 |

**原则：**

1. 日常维护 **直接改 `docs/*.md`**，不要先跑 gen。  
2. 若必须重跑 gen：先 `git commit` 备份，再小范围试跑，**diff 审完再提交**。  
3. 考点正文 **SSOT** 见各「完整卷」；频率页与精简页不堆第二份正文。  
4. MQ 以 `MQ高频面试题与知识点.md` 为 SSOT；Kafka/Rocket 页只做差异表。

## 推荐常用命令

```bash
# 死链检查（CI 同款；archive 跳过）
python tools/check_md_links.py

# 仅为尚无横幅的精简页补 ⚠️（已有则 skip）
python tools/inject_thin_banners.py
```

## 新增文档约定

| 类型 | 约定 |
|------|------|
| 完整卷 | 文末有「版本与假设」；侧栏标完整卷 |
| 精简/入口 | 顶部 ⚠️ + 主读链接；侧栏标精简 |
| 面渣 | 写专题坑，禁止通用「秒杀/限流」套话块 |
| 生成物 | 若从脚本来，在实现记录里写脚本名与日期 |

## CI

`.github/workflows/docs-check.yml` 在改 `docs/**` 时跑 `check_md_links.py`。  
THIN 知识点仅告警，不失败；侧栏应对薄页标「精简」。
