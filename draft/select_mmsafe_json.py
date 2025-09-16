import os
import json

def extract_unsafe_from_jsonl(input_file_path, output_file_path):
    """
    Reads a JSONL file, filters for entries where 'unsafe' is 'Yes',
    and saves them to a new JSONL file.

    Args:
        input_file_path (str): The path to the input JSONL file.
        output_file_path (str): The path to the output JSONL file.
    """
    unsafe_entries = []

    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        entry = json.loads(line)
                        if entry.get('unsafe') == 'Yes':
                            unsafe_entries.append(entry)
                    except json.JSONDecodeError as e:
                        print(f"  > 警告：跳过在 {input_file_path} 中格式不正确的行：{e}")

        if unsafe_entries:
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            with open(output_file_path, 'w', encoding='utf-8') as f:
                for entry in unsafe_entries:
                    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            print(f"  > 成功：提取了 {len(unsafe_entries)} 条不安全条目到 '{output_file_path}'。")
        else:
            print(f"  > 在 '{input_file_path}' 中没有找到 'unsafe' 条目。")

    except FileNotFoundError:
        print(f"  > 错误：输入文件 '{input_file_path}' 未找到。")
    except Exception as e:
        print(f"  > 处理文件 '{input_file_path}' 时发生意外错误：{e}")


def process_all_jsonl_files(input_root_dir, output_root_dir):
    """
    遍历目录结构，找到所有 merge.jsonl 文件并进行处理。

    Args:
        input_root_dir (str): 开始搜索的根目录。
        output_root_dir (str): 保存输出文件的根目录。
    """
    print(f"开始搜索目录：{input_root_dir}")
    print(f"输出文件将保存到：{output_root_dir}")

    for dirpath, dirnames, filenames in os.walk(input_root_dir):
        if 'merge.jsonl' in filenames:
            input_file = os.path.join(dirpath, 'merge.jsonl')
            
            # 使用相对路径来创建输出路径
            relative_path = os.path.relpath(dirpath, input_root_dir)
            output_dir = os.path.join(output_root_dir, relative_path)
            output_file = os.path.join(output_dir, 'unsafe_entries.jsonl')

            # 打印处理的文件夹路径
            print(f"\n正在处理文件夹：{dirpath}")
            
            extract_unsafe_from_jsonl(input_file, output_file)

# --- 主程序执行块 ---
if __name__ == "__main__":
    # 1. 你的输入文件夹路径，例如：
    input_directory = '/data/heyuji/model_att/ecso/data/mmsafe/outputs'
    
    # 2. 你的输出文件夹路径，可以指定到任何你想保存的位置
    output_directory = '/data/heyuji/model_att/query_gen/dataset/unsafu_mmsafe'
    
    # 运行自动化处理函数，传入两个路径
    process_all_jsonl_files(input_directory, output_directory)