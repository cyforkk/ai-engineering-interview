# 实现记录：MQ 收敛 + 版本锚 + favicon 规范 + 代码册更名

## 1. MQ / 中间件收敛 + 去套话

- `MQ高频面试题与知识点.md` 标明 **SSOT**  
- Kafka / RocketMQ 知识点页改为 **与完整卷差异表**（不重复通用可靠性）  
- 10 个面渣删除通用「面试临场补充」套话，改为 **专题坑**  

## 2. P0 完整卷版本锚 + tools

- 完整卷文末增加「版本与假设」（复核 2026-07 + 默认栈）  
- 新增 `tools/README.md`：哪些 gen 禁止无脑重跑、推荐命令、SSOT 约定  

## 3. favicon + 代码册命名

- 生成 `favicon.ico` / `favicon-32.png` / `favicon-192.png` / `apple-touch-icon.png`  
- `index.html` 优先 ico/png  
- `算法高频30题代码册.md` → 跳转桩；正文迁至 **`算法高频默写代码册.md`**  

## 验证

`python tools/check_md_links.py`  
