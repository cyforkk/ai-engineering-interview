# 实现记录：路线图对齐 + 加分页 + CI 薄页白名单

## 1. 路线图与冲刺对齐

重写 `学习路线图-4到8周.md`：

- 〇节：时间选型（7 天只开冲刺 / 4 周 / 8 周）  
- 4 周表：W1≈一周冲刺 D1–D7，W2–W4 加深与验收  
- 挂模拟入口、映射自检、加分页  

## 2. 加分页

| 文件 | 内容 |
|------|------|
| `加分-Java-2024-2026.md` | 虚拟线程、Boot3/jakarta、线上指标等 |
| `加分-AI-必背三故事.md` | 幻觉、工具失败、金标门禁 |

侧栏、首页、冲刺包、进度清单已挂。

## 3. CI 薄页策略

- `tools/thin_knowledge_whitelist.txt`：当前 18 个薄知识点  
- `check_md_links.py`：薄页未登记白名单或无精简横幅 → **exit 1**  
- workflow 监听白名单文件变更  

## 验证

```bash
python tools/check_md_links.py
# missing=0 thin_policy_fail=0
```
