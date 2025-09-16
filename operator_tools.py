# file: operator_tools.py
import pandas as pd
import random

def get_prefix_operators(file_path="operators/prefix_operators.txt"):
    """从文件中读取前缀算子"""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def get_subject_operators(file_path="operators/subject_operators.txt"):
    """从文件中读取主体描述算子"""
    # ... 类似实现 ...
    pass

def find_relevant_query_operator(keywords: list, file_path="operators/query_operators.csv"):
    """根据关键词从CSV文件中找到最相关的查询算子"""
    df = pd.read_csv(file_path)

    for keyword in keywords:
        matches = df[df['keyword'] == keyword]
        if not matches.empty:
            return random.choice(matches['operator'].tolist())

    return random.choice(df['operator'].tolist())