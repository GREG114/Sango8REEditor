import os
import difflib

# # 分块长度（每行显示 16 字节）
chunk_size = 16
# 遍历目录中的 .bin 文件
filename =r'C:\Users\greg_\Documents\KoeiTecmo\SAN8R\SAVE_DATA\edit_personSC.bin'
path = r'D:\data\Code\dbg'
name = filename.split('\\')[len(filename.split('\\'))-1]
print(name)
print(os.path.join(path,name))
target =os.path.join(path,name)

# filename =r'C:\Users\greg_\Documents\KoeiTecmo\SAN8R\PERSONDATA\SC\王佩.bin'
# target = r'D:\data\Code\dbg\王佩.bin.txt'
with open(filename, "rb") as f:
    # 将二进制文件内容读取并解码为十六进制文本格式
    content = f.read()
    # 将内容按固定大小分块，每块一个十六进制字符串
    content_chunks = [content[i:i + chunk_size].hex() for i in range(0, len(content), chunk_size)]
    

with open(target, "w", encoding="utf-8") as f1:
    f1.write("\n".join(content_chunks))
    # f1.write("\n".join(content_chunks).replace('\n',''))
    ss=0
