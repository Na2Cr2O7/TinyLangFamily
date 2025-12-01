
<p align="center">
  <img src="I.png" width="200" alt="TinyLang Logo">
</p>

# TinyLang

> **极简 · 零依赖 · 可嵌入的中文对话系统家族**

TinyLang 是一系列**仅使用 Python 标准库**构建的轻量级语言模型实验项目，旨在探索在无外部依赖、低资源环境下实现可用的中文对话能力。所有非 LLM 模型均可在树莓派、微控制器或纯 Python 环境中运行。
### 2025-12-1 新成员

 - [TinyLangJaccard-C++](TinyLangJaccardC++.exe)
 - [TinyLangCosineSwiftness](simple)

<p align="center">
  <img src="Image_1764473287928.png" height="200" alt="Model Comparison">
</p>

### 开源协议:

 - TinyLangLLM在Apache-2.0许可下发布。
 - 其余在the Unlicense许可下发布。
 - 请查看每个训练集的网页以确定它们的开源协议

---

## 🧠 家族成员

| 模型 | 状态 | 类型 | 特点 | 适用场景 |
|------|------|------|------|--------|
| [TinyLangLLM](TinyLangLLM) | ⚠️ 实验性 | 36M Transformer | 能生成新句子，但存在幻觉和事实错误 | 创意聊天、生成实验 |
| [TinyLangJaccard](simple) | ✅ 推荐 | Jaccard + SQLite | **0.01s 响应**，回答规范，适合 FAQ | 嵌入式设备、客服机器人 |
| [TinyLangJaccard-C++](TinyLangJaccardC++.exe) | ✅ **高性能版** | Jaccard + SQLite (C++) | **亚毫秒响应**，Python 版的 10–100 倍加速 | 高性能嵌入式设备、实时对话系统 |
| [TinyLangJaccard0](simple) | ✅ 可用 | 角色扮演（JSON） | 萌系人设“沐雪”，娱乐性强 | 游戏 NPC、虚拟伴侣 |
| [TinyLangCosine](simple) | ⚠️ 低效 | 余弦相似度（纯 Python） | 语义略优，但**查询慢（最高 187s）** | 教学演示、语义检索研究 |
| [TinyLangCosineSwiftness](simple) | 更快 | 余弦相似度（纯 Python） | 从输出来看，它继承了 Python 版 Cosine 的“灵魂”：答非所问的艺术达到了新高度 😅。 | 教学演示、语义检索研究 |
| TinyLangLSTM / CNN / FNN | ❌ 停止维护 | — | 性能/效果不佳 | — |
| TinyLangTraditionalML | ❌ 未实现 | — | 胎死腹中 | — |

> 💡 **为什么 Jaccard 是“效果最好”？**  
> 在“速度 + 稳定性 + 零依赖”三者平衡下，Jaccard 版本表现最优，适合真实部署。

---

## 🎯 设计哲学

- **Tiny First**：除 LLM 外，所有模型**仅用 Python 标准库**（`json`, `sqlite3`, `re`, `math`）。
- **No Magic**：无黑盒依赖，代码可读、可移植、可教学。
- **Trade-off Aware**：明确区分“生成式”与“检索式”系统的优劣，不追求虚假智能。

---

## 🧪 模型效果速览

### TinyLangJaccard（推荐）
```text
Q: 中国的首都是哪里？
A: 中国的首都城市是北京。 (0.01s)

Q: 最近总是失眠，感觉好累……
A: 失眠确实很困扰人，试试冥想或听些轻音乐...
```

### TinyLangJaccard0（角色扮演）
```text
Q: 你最喜欢的食物是什么？
A: 我最喜欢吃的是棉花糖哦~

Q: 我刚和最好的朋友吵架了……
A: 能告诉咱发生了什么嘛？...我的立场是不是绝对正确的呢？
```

### TinyLangLLM（生成式，注意幻觉）
```text
Q: 中国的首都是哪里？
A: 中国的首都是西安。 ❌
```

> 🔗 [查看完整测试日志与详细评估报告](e.md)（后续更新）

---

## ▶️ 快速开始

```bash
# 运行 Jaccard 版本（需 Python 3.6+）
python simple/tiny_jaccard.py
```

所有代码位于 `simple/` 目录，无第三方依赖。

---

## 📚 未来计划

- 为 Cosine 版本添加倒排索引，提速 100 倍
- 构建统一评估脚本（自动打分）
- 发布“TinyLang in 100 Lines”教学版

---
> Made with ❤️ and `import math`
