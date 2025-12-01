import json
import os
import math
from typing import List
from time import time
import sqlite3

if not os.path.exists('../dataset.db'):
    import compressDatasetSqlite

import dbconnect
questions, answers = dbconnect.questions, dbconnect.answers

# —————— Step 1: 构建或加载 tokenizer（char → index）——————
if not os.path.exists('tokenizer.json'):
    import wordFrequency
    freq_list = wordFrequency.frequency_as_string(questions+answers)
    # 按 frequency 中的顺序建立映射（高频在前，但不影响 correctness）
    start=time()
    chartoidx = {char: idx for idx, (char, _) in enumerate(freq_list)}
    print(f"✅ 构建 tokenizer.json 耗时:{time()-start:.2f}s")
    with open('tokenizer.json', 'w', encoding='utf8') as f:
        json.dump(chartoidx, f, ensure_ascii=False)
else:
    with open('tokenizer.json', 'r', encoding='utf8') as f:
        chartoidx = json.load(f)

start=time()
vocab_size = len(chartoidx)






# —————— Step 3: 文本 → 固定维度频次向量 ——————
def text_to_vector(text: str,seq_len=16) -> List[int]:
    vec = [0] * vocab_size
    for char in text:
        if char in chartoidx:
            idx = chartoidx[char]
            vec[idx] += 1  # 计数：Term Frequency
    
    return vec

# 预计算所有问题的向量（大幅提升查询速度）
print("正在预计算问题向量...")

question_vectors = [text_to_vector(q) for q in questions]

print(f"✅ 加载 {len(questions)} 个问题，词表大小: {vocab_size}")

# —————— Step 4: 余弦相似度（纯 math）——————
def cosine_similarity(v1: List[int], v2: List[int]) -> float:
    dot = 0
    norm1_sq = 0
    norm2_sq = 0
    for a, b in zip(v1, v2):
        dot += a * b
        norm1_sq += a * a
        norm2_sq += b * b
    if norm1_sq == 0 or norm2_sq == 0:
        return 0.0
    return dot / (math.sqrt(norm1_sq) * math.sqrt(norm2_sq))

# —————— Step 5: 问答主函数 ——————
def answer_fast(user_question: str) -> str:
    if not user_question.strip():
        return "请输入有效问题。"
    
    user_vec = text_to_vector(user_question)
    best_idx = 0
    max_sim = -1.0

    for i, q_vec in enumerate(question_vectors):
        sim = cosine_similarity(user_vec, q_vec)
        if sim > max_sim:
            max_sim = sim
            best_idx = i

    # 可选：设置相似度阈值避免低质量匹配
    if max_sim < 0.1:
        return "抱歉，我不太明白你的意思。"
    
    return answers[best_idx]


print(f"✅ 预处理完成，耗时:{time()-start:.2f}s")

# —————— 主程序 ——————
if __name__ == '__main__':
    print('TinyLangCosine-Sqlite 测试')
    print('数据集:https://modelscope.cn/datasets/qiaojiedongfeng/qiaojiedongfeng')
    try:
        while True:
            q = input('请输入问题: ')
            start=time()
            print("→", answer_fast(q))
            print(f"✅ 耗时:{time()-start:.2f}s")
    except (KeyboardInterrupt, EOFError):
        print("\n👋 再见！")