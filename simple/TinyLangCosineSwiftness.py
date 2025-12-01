import json
import os
import math
from typing import List
from time import time
import sqlite3

# 第三方或自定义模块按需导入
if not os.path.exists('../dataset.db'):
    import compressDatasetSqlite

import dbconnect
questions, answers = dbconnect.questions, dbconnect.answers

# 初始化 tokenizer
if not os.path.exists('tokenizer.json'):
    import wordFrequency
    freq_list = wordFrequency.frequency_as_string(questions + answers)
    start = time()
    chartoidx = {char: idx for idx, (char, _) in enumerate(freq_list)}
    print(f"✅ 构建 tokenizer.json 耗时: {time() - start:.4f}s")
    with open('tokenizer.json', 'w', encoding='utf8') as f:
        json.dump(chartoidx, f, ensure_ascii=False)
else:
    with open('tokenizer.json', 'r', encoding='utf8') as f:
        chartoidx = json.load(f)

idxtochar = {idx: char for char, idx in chartoidx.items()}

# 缓存 tokenized questions 向量
_tokenized_questions = None


def pad_sequence(text: str, seq_len: int = 64) -> str:
    """Pad or truncate a sequence to a fixed length."""
    if len(text) > seq_len:
        return text[:seq_len]
    else:
        return text + " " * (seq_len - len(text))


def tokenize(text: str, seq_len: int = 64) -> List[int]:
    padded_text = pad_sequence(text, seq_len)
    tokens = []
    for char in padded_text:
        if char in chartoidx:
            tokens.append(chartoidx[char])
        else:
            # 对于未知字符可以选择跳过或者使用默认 token（比如 <UNK>）
            pass
    return tokens


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))

    if norm_a == 0 or norm_b == 0:
        return 0.0  # 安全处理零向量情况

    return dot_product / (norm_a * norm_b)


def get_cached_tokenized_questions():
    global _tokenized_questions
    if _tokenized_questions is None:
        _tokenized_questions = [tokenize(q) for q in questions]
    return _tokenized_questions


def answer_extremely_fast(user_question: str) -> str:
    user_question_vector = tokenize(user_question)
    best_match = None
    best_score = -1
    cached_questions_vectors = get_cached_tokenized_questions()

    for i, question_vector in enumerate(cached_questions_vectors):
        score = cosine_similarity(user_question_vector, question_vector)
        if score > best_score:
            best_score = score
            best_match = answers[i]

    return best_match


if __name__ == '__main__':
    print('TinyLangCosine-Sqlite-Swiftness 测试')
    print('数据集: https://modelscope.cn/datasets/qiaojiedongfeng/qiaojiedongfeng')
    try:
        while True:
            q = input('请输入问题: ')
            start = time()
            result = answer_extremely_fast(q)
            print("→", result)
            print(f"✅ 耗时: {time() - start:.4f}s")
    except (KeyboardInterrupt, EOFError):
        print("\n👋 再见！")