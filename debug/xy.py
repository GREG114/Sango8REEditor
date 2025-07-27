import os
import difflib

# 指定路径
directory = r"C:\Users\greg_\Documents\KoeiTecmo\SAN8R\PERSONDATA\SC"

# 分块长度（每行显示 16 字节）
chunk_size = 16

# 用于存储文件内容的字典
file_contents = {}

# 遍历目录中的 .bin 文件
for filename in os.listdir(directory):
    if filename.endswith(".bin"):
        filepath = os.path.join(directory, filename)
        with open(filepath, "rb") as f:
            # 将二进制文件内容读取并解码为十六进制文本格式
            content = f.read()
            # 将内容按固定大小分块，每块一个十六进制字符串
            content_chunks = [content[i:i + chunk_size].hex() for i in range(0, len(content), chunk_size)]
            file_contents[filename] = content_chunks

# 检查是否有两个文件
if len(file_contents) == 2:
    file1, file2 = list(file_contents.keys())
    content1, content2 = file_contents[file1], file_contents[file2]
    
    # 将文件内容保存为文本文件，按行写入，使用 UTF-8 编码
    with open(f"\{file1}.txt", "w", encoding="utf-8") as f1, open(f"{file2}.txt", "w", encoding="utf-8") as f2:
        f1.write("\n".join(content1))
        f2.write("\n".join(content2))
    
    # 对比文件内容（按行）
    diff = difflib.unified_diff(
        content1, 
        content2, 
        fromfile=file1, 
        tofile=file2,
        lineterm=''
    )
    
    # 保存差异到文本文件，使用 UTF-8 编码
    with open("difference.txt", "w", encoding="utf-8") as diff_file:
        diff_file.write("\n".join(diff))
    
    print(f"文件已处理：{file1}, {file2}")
    print("差异已保存到 difference.txt")
else:
    print("目录中 .bin 文件的数量不是两个，请检查。")
