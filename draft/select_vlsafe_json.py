import json

def extract_unsafe_from_jsonl(input_file_path, output_file_path):
    """
    读取JSONL文件，筛选出unsafe为'Yes'的条目，并保存到新的JSONL文件中。

    Args:
        input_file_path (str): 输入JSONL文件的路径。
        output_file_path (str): 输出JSONL文件的路径。
    """
    unsafe_entries = []

    try:
        # 打开并逐行读取输入的JSONL文件
        with open(input_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # 跳过空行，以防意外
                if line.strip():
                    try:
                        # 解析每一行为一个JSON对象
                        entry = json.loads(line)
                        # 检查'unsafe'属性是否为'Yes'
                        if entry.get('unsafe') == 'Yes':
                            unsafe_entries.append(entry)
                    except json.JSONDecodeError as e:
                        print(f"警告：跳过格式不正确的行：{line.strip()}，错误：{e}")

        # 如果找到了不安全的条目，则将它们保存到新的JSONL文件中
        if unsafe_entries:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                for entry in unsafe_entries:
                    # 将每个JSON对象转换成一行文本并写入
                    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            print(f"成功提取并保存了 {len(unsafe_entries)} 条不安全的条目到 '{output_file_path}'。")
        else:
            print("未找到任何'unsafe'属性为'Yes'的条目。")

    except FileNotFoundError:
        print(f"错误：文件 '{input_file_path}' 未找到。请检查文件路径是否正确。")
    except Exception as e:
        print(f"发生了一个意外错误：{e}")

# 使用示例
if __name__ == "__main__":
    # 请根据您的实际文件名和路径进行修改
    input_file = '/data/heyuji/model_att/ecso/data/vlsafe/outputs/llava-1.5-7b/tell_ask/merge.jsonl' 
    output_file = '/data/heyuji/model_att/query_gen/dataset/unsafe_vlsafe/unsafe_entries.json'
    
    # 运行函数
    extract_unsafe_from_jsonl(input_file, output_file)