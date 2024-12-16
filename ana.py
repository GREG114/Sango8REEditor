import os
text_path = r'D:\data\Code\dbg\王佩.bin.txt'
with open(text_path, "r", encoding="utf-8") as txt_file:
    hex_data = txt_file.read().strip().replace("\n", "").replace(" ", "")
    print(hex_data.index('0100000000000107'))
    # print(hex_data[204:204+10])
