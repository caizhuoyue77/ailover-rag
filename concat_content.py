import os
import re

def split_markdown_content(content):
    """根据 # 分片并返回分片列表"""
    sections = re.split(r'\n(?=#)', content)  # 按行分割并查找以#开头的行
    return [section.strip() for section in sections]

def extract_markdown_content_and_calculate_length(root_folder, output_file, split_file):
    lengths = []  # 用于存储每个分片的内容长度

    # 正则表达式模式，用于匹配Markdown图像语法和心形符号示例
    image_pattern = re.compile(r'!\[.*?\]\(.*?\)')  # 匹配Markdown图像
    heart_example_pattern = re.compile(r'❤示例')  # 匹配形如❤示例的字符串

    with open(output_file, 'w', encoding='utf-8') as outfile, open(split_file, 'w', encoding='utf-8') as split_outfile:
        # 遍历根文件夹及其所有子文件夹
        for dirpath, dirnames, filenames in os.walk(root_folder):
            for filename in filenames:
                if filename.endswith('.md'):  # 检查文件扩展名
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()  # 读取Markdown文件内容
                        # 清洗内容，删除图像引用和心形示例
                        cleaned_content = image_pattern.sub('', content)
                        cleaned_content = heart_example_pattern.sub('', cleaned_content)

                        # 删除多余空行
                        cleaned_content_lines = [line for line in cleaned_content.splitlines() if line.strip()]  # 删除所有空行
                        cleaned_content = '\n'.join(cleaned_content_lines).strip()  # 合并非空行

                        # 根据标题进行分片
                        sections = split_markdown_content(cleaned_content)
                        
                        # 计算分片的长度
                        for section in sections:
                            file_length = len(section)  # 获取分片的内容长度
                            lengths.append(file_length)  # 添加到长度列表

                            # 处理文件名
                            base_filename = filename.split('+')[0].strip()  # 分割并取第一个元素
                            # 处理文件夹名
                            base_foldername = os.path.basename(dirpath).split('+')[0].strip()  # 获取文件夹名并分割

                            # 写入分隔符和文件名
                            outfile.write("============\n")  # 分隔符
                            outfile.write(f"# {base_foldername}/{base_filename}\n")  # 文件夹和文件名
                            outfile.write(section + '\n\n')  # 写入分片内容，并添加换行
                            
                            # 打印每个分片的长度
                            print(f"{file_path} - 分片长度: {file_length} 字符")
                            
                            # 将分片写入到 split.txt
                            split_outfile.write(section + '\n\n\n')  # 用两个空行隔开每个片

    # 计算长度信息
    if lengths:
        max_length = max(lengths)
        min_length = min(lengths)
        avg_length = sum(lengths) / len(lengths)
        
        # 在 split.txt 中写入长度统计
        with open(split_file, 'a', encoding='utf-8') as split_outfile:
            split_outfile.write(f"\n统计信息：\n")
            split_outfile.write(f"最短分片长度: {min_length} 字符\n")
            split_outfile.write(f"最长分片长度: {max_length} 字符\n")
            split_outfile.write(f"平均分片长度: {avg_length:.2f} 字符\n")
        
        # 打印长度统计信息
        print(f"\n最大长度: {max_length} 字符")
        print(f"最小长度: {min_length} 字符")
        print(f"平均长度: {avg_length:.2f} 字符")
    else:
        print("未找到任何Markdown文件。")


# 使用示例
root_folder = 'data/flowus_dir/猎人小姐请用深空bot指南！+fc8ce11a-3078-4489-a258-24011ad1701f'  # 替换为你的根文件夹路径
output_file = 'data/猎人小姐深空bot指南.txt'  # 输出文件名
split_file = 'data/猎人-split.txt'  # 分片输出文件名
extract_markdown_content_and_calculate_length(root_folder, output_file, split_file)