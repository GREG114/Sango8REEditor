import os,re
import difflib
# # 分块长度（每行显示 16 字节）
chunk_size = 16
filename =r'C:\Users\greg_\Documents\KoeiTecmo\SAN8R\SAVE_DATA\edit_personSC.bin'
with open(filename, "rb") as f:
    # 将二进制文件内容读取并解码为十六进制文本格式
    content = f.read()
hex = content.hex()

# f796是目标要改成 691b


# 使用正则表达式找到所有匹配项
all_occurrences = [m.start() for m in re.finditer('416dba83', hex)]
count = 0
# 打印所有匹配位置
for i, occurrence in enumerate(all_occurrences):
    if i == 1: continue  # 跳过第二个匹配项
    print(f"第{i+1}次出现的位置:", occurrence)
    count += 1
    lhidx = occurrence + 56
    # # 检查是否超出范围
    if lhidx + 4 <= len(hex):
        # 将字符串转换为列表，因为列表是可变的
        hex_list = list(hex)
        
        # 修改列表中的内容
        hex_list[lhidx:lhidx+4] = '691b'        
        # hex_list[lhidx:lhidx+4] = '3602'        
        # 将列表转换回字符串
        hex = ''.join(hex_list)
        
        print("修改后的内容:", hex[lhidx:lhidx+4])
    else:
        print("超出范围，无法修改")

# 保存修改后的内容回文件
with open(filename, "wb") as f:
    # 注意：hex 字符串现在是修改后的十六进制字符串，需要转换回二进制
    modified_content = bytes.fromhex(hex)
    f.write(modified_content)

print(count)