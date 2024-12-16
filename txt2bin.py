import os

# 文本文件路径
text_file_path = r"D:\data\Code\dbg\edit_personSC.bin.txt"
# 输出的二进制文件路径
bin_file_path = text_file_path.replace(".txt", "")

bin_file_path = bin_file_path.replace('D:\\data\\Code\\dbg',r'C:\Users\greg_\Documents\KoeiTecmo\SAN8R\SAVE_DATA')

def text_to_bin(text_path, bin_path):
    try:
        # 打开文本文件并读取十六进制内容
        with open(text_path, "r", encoding="utf-8") as txt_file:
            hex_data = txt_file.read().strip().replace("\n", "").replace(" ", "")
        
        # 将十六进制字符串转换为二进制数据
        bin_data = bytes.fromhex(hex_data)
        # 保存到二进制文件
        with open(bin_path, "wb") as bin_file:
            bin_file.write(bin_data)        
        print(f"二进制文件已保存到: {bin_path}")
    except Exception as e:
        print(f"转换失败: {e}")

# 执行转换
text_to_bin(text_file_path, bin_file_path)
