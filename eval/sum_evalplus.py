import os
import argparse

def get_checkpoint(folder_name, model_name):
    """从文件夹名称中提取出checkpoint的数字."""
    prefix = f"{model_name}-checkpoint-"
    if folder_name.startswith(prefix):
        checkpoint_str = folder_name[len(prefix):]
        return int(checkpoint_str)
    elif folder_name.startswith(f"{model_name}-final"):
        return 100000
    return None


def read_pass_at_1(file_path):
    """读取T0_N1_pass@k.txt文件，提取pass@1的两行数字."""
    pass_at_1_values = []
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("pass@1:"):
                    value = float(line.split("pass@1:")[1].strip())
                    pass_at_1_values.append(value)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    return pass_at_1_values

def process_directory(base_dir, model_name):
    """处理preds_humaneval或preds_mbpp文件夹下的所有文件夹."""
    model_folders = []
    
    # 获取所有以model开头的文件夹，并按checkpoint排序
    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path):
            checkpoint = get_checkpoint(folder, model_name)
            if checkpoint is not None:
                model_folders.append((folder_path, checkpoint))
    
    # 按checkpoint数字大小排序
    model_folders.sort(key=lambda x: x[1])
    # for m in model_folders:
    #     print(m[1])
    # 两个数组存储pass@1的两个值
    pass_at_1_first = []
    pass_at_1_second = []
    
    # 按顺序读取文件夹中的T0_N1_pass@k.txt
    for folder_path, checkpoint in model_folders:
        file_path = os.path.join(folder_path, "T0_N1_pass@k.txt")
        pass_at_1_values = read_pass_at_1(file_path)
        
        if len(pass_at_1_values) >= 2:
            pass_at_1_first.append(pass_at_1_values[0])
            pass_at_1_second.append(pass_at_1_values[1])
    
    return pass_at_1_first, pass_at_1_second


def print_numbers(numbers):
    for number in numbers:
        print(number)

def main():
    parser = argparse.ArgumentParser(description="处理preds_humaneval和preds_mbpp文件夹")
    parser.add_argument("--model", type=str, required=True, help="模型名称")
    
    args = parser.parse_args()
    datasets = ["humaneval", "mbpp"]
    for dataset in datasets:
        print(f"处理{dataset}文件夹...")
        pass_at_1_first, pass_at_1_second = process_directory(f"../preds_{dataset}/", args.model)
        print_numbers(pass_at_1_first)
        print_numbers(pass_at_1_second)
        

if __name__ == "__main__":
    main()
