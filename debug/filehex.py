import os
import difflib

# 指定路径
directory = r"C:\Users\greg_\Documents\KoeiTecmo\SAN8R\PERSONDATA\SC"
# directory =r'C:\Users\greg_\Documents\KoeiTecmo\SAN8R\SAVE_DATA'
# # 分块长度（每行显示 16 字节）
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

for i in file_contents:
    with open(f"{i}.txt", "w", encoding="utf-8") as f1:
        f1.write("\n".join(file_contents[i]))

# path = r'C:\Users\greg_\Documents\KoeiTecmo\SAN8R\SAVE_DATA\edit_personSC.bin'
# path = r'C:\Users\greg_\Documents\KoeiTecmo\SAN8R\PERSONDATA\SC\王佩1.bin'
# with open(path, "rb") as f:
#     content = f.read()
#     content_chunks = [content[i:i + chunk_size].hex() for i in range(0, len(content), chunk_size)]



# print(content)



# # with open(f"edit_personSC.txt", "w", encoding="utf-8") as f1:
# #     f1.write("\n".join(content_chunks))
