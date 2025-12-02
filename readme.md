<p align="center">
  <img src="I.png" width="200" alt="TinyLang Logo">
</p>



# TinyLang

> **极简 · 零依赖 · 可嵌入的中文对话系统家族**  

> 在树莓派上运行 AI？用标准库实现智能？欢迎来到 TinyLang —— 这里没有黑盒，只有清晰的代码与诚实的 AI。

<p align="center">
  <img src="Image_1764473287928.png" width="200" alt="666">
</p>

---

## 🌐 两大技术路线

TinyLang 并非单一模型，而是一个**双轨并行的轻量对话生态**：

### 🧠 1. 生成式分支（基于 MiniMind2-26M 微调）
> 所有模型均在 [jingyaogong/minimind](https://github.com/jingyaogong/minimind) 基座上通过 **LoRA 微调**得到，具备语言生成能力，但可能产生幻觉。

| 模型 | 状态 | 特点 | 场景 |
|------|------|------|------|
| **氯铂酸喵第四代 (NaCl-Platinum)** | ✅✅✅ **已部署上线** | 全程“喵语”，人设极致一致 | 二次元陪伴、情感交互 |
| **MiniMind2 基座** | ✅ 推荐 | 事实准确，逻辑清晰 | 知识问答、RAG 后端 |
| TinyLangLLM2 | ⚠️ 可用 | 语言自然，有共情尝试 | 开放聊天（非关键信息） |
| TinyLangLLM / DeepThinking / 氯铂酸喵 V3 | ❌ 已淘汰 | 幻觉严重 / 逻辑崩溃 / 输出碎片 | — |

> 💡 **提示**：生成式模型适合“创意”与“陪伴”，**不适合事实查询**。

---

### 🔍 2. 检索式分支（无 LLM，纯标准库）
> **不使用任何神经网络**，仅依赖 `json`、`sqlite3`、`re`、`math` 等 Python 标准库，**零幻觉、亚毫秒响应**。

| 模型 | 状态 | 特点 | 场景 |
|------|------|------|------|
| **TinyLangJaccard-C++** | ✅✅✅ **工业首选** | **<1ms 响应**，C++ 实现 | 嵌入式设备、实时客服 |
| **TinyLangJaccard** | ✅ 推荐 | 0.01s 响应，纯 Python | 教学、轻量部署 |
| **TinyLangJaccard0** | ✅ 娱乐向 | 萌系“沐雪”人设，规则拒答 | 游戏 NPC、虚拟伴侣 |
| Cosine / Cosine-Swiftness | ⚠️ 教学用 | 语义检索演示，速度慢 | NLP 教学研究 |

> 💡 **提示**：检索式模型是**真实世界部署的首选**——快、稳、可解释。

---

## 🎯 设计哲学

- **Tiny First**：除生成式分支外，**所有代码仅用 Python 标准库**，无需 `torch`、`transformers`。
- **No Magic**：无抽象封装，代码可读、可移植、可教学。
- **Honest AI**：明确标注能力边界——**不假装知道，不伪装思考**。
- **Right Tool for Right Job**：要快？用 Jaccard。要萌？用猫娘。要聊？用 LLM2。要准？用基座。

### ⚠️ 重要经验：小模型微调必须使用高纯度数据
- 氯铂酸喵第三代（12MB 噪声数据）→ 输出碎片化，无法部署  
- 氯铂酸喵第四代（263KB 纯净角色数据）→ 成功上线 AI 回复机器人  
- **教训**：对 26M–36M 模型，**100 条精心设计的样本 > 10,000 条爬取数据**

> Tiny AI 的核心不是“模型多大”，而是“数据多准”。

### 氯铂酸喵第三代（历史版本）
早期尝试，因缺乏明确角色指令，导致输出碎片化、无个性。  
**教训**：小模型必须通过强约束（如固定语气、世界观）才能发挥最大魅力。  
→ 已由第四代全面取代。



### ✨ 特别鸣谢：  

**NaCl-Platinum（氯铂酸喵第四代）** 已从 TinyLang 毕业， 

成功部署于 [米游社](https://www.miyoushe.com/)，为用户提供萌系陪伴服务！  

这标志着 TinyLang 不仅是实验平台，更是**轻量级 AI 的 launchpad**。

### 🐾 NaCl-Platinum 的“毕业证书”

> **姓名**：NaCl-Platinum（氯铂酸喵第四代）  
> **基座**：MiniMind2-26M  
> **专长**：二次元猫娘角色扮演、情感陪伴、萌系交互  
> **成就**：✅ 成功部署于米游社  
> **毕业评语**：  
> “你完美诠释了‘小模型大魅力’——不追求全能，只专注可爱。去吧，用喵呜声治愈更多用户！”

---

### 🔮 对 TinyLang 未来的启示

NaCl-Platinum 的成功为后续模型指明了方向：

1. **垂直化 > 通用化**  
   - 在 26M–36M 小模型上，**打造鲜明人设**比追求“什么都会”更有效。

2. **场景驱动微调**  
   - 部署目标决定训练策略：  
     - 客服 → 用 Jaccard-C++  
     - 虚拟女友 → 用猫娘/学姐/毒舌等角色模型

3. **TinyLang 作为“模型苗圃”**  
   - 孵化 → 测试 → 优化 → **毕业部署**  
   - 家族成员动态更新，只保留最具代表性的分支

**她不是离开了家，而是带着 TinyLang 的基因，去更大的世界发光了！** 💫





---

## 🧪 效果对比（节选）

### ✅ 检索式（可靠）
```text
Q: 中国的首都是哪里？
A: 中国的首都城市是北京。 (0.003s)
```

### 🐾 角色扮演（有趣）
```text
Q: 我考上了理想的大学！
A: 喵呜！大学学硕士真的很难考上你喵！
```

### ⚠️ 生成式（需谨慎）
```text
Q: 水的化学式是什么？
A: 水的化学式是酸性喵...本雪不喜欢喵 ❌
```

> 🔗 [查看完整测试日志与评估报告](e.md)

---

## ▶️ 快速开始

```bash
# 运行推荐版（纯 Python，零依赖）
python simple/tiny_jaccard.py

# 或直接编译 C++ 版（需 g++）
g++ -O3 -o jaccard_cpp simple/jaccard_cpp.cpp
./jaccard_cpp
```

所有代码位于 `simple/` 目录，**无第三方依赖**。

---

## 📜 开源协议

- **生成式模型**（TinyLangLLM 系列）：Apache-2.0  
- **检索式模型**（Jaccard / Cosine 系列）：The Unlicense  
- 数据集协议请参考各自来源

### 数据集
#### Apache-2.0
TinyLangLLM,TinyLangLLM2,TinyLangJaccard-Swiftness-SQLite,TinyLangJaccardC++,TinyLangCosine,TinyLangCosine-SQLite-Swiftness [数据集](https://www.modelscope.cn/datasets/qiaojiedongfeng/qiaojiedongfeng) 

TinyLangLLM-DeepThinking [数据集](https://www.modelscope.cn/datasets/liucong/Chinese-DeepSeek-R1-Distill-data-110k-SFT)

#### CC-BY-NC-4.0
TinyLangJaccard0 [数据集](https://www.modelscope.cn/datasets/Moemuu/Muice-Dataset) 


NaCl-Platinum [数据集](https://www.modelscope.cn/datasets/himzhzx/muice-dataset-train.catgirl)




---

## 🌱 未来计划

- [ ] 发布 “TinyLang in 100 Lines” 教学版
- [ ] 为 Cosine 添加倒排索引（目标：10ms 内）
- [ ] 构建统一评估脚本（自动打分 + 幻觉检测）
- [ ] 支持 ONNX 导出 Jaccard-C++ 到单片机

---

> Made with ❤️ and `import math`  
> **小即是美，诚即是强。**

