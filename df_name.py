import binascii

# 原始数据：名字修改前后的对应字节
data_before = bytes.fromhex("85680000000000000000000000000000")
data_after = bytes.fromhex("0f970000000000000000000000000000")

# 尝试解码名字（根据不同编码方式）
def decode_name(data):
    encodings = ["gbk", "utf-8", "utf-16le"]  # 尝试常见的编码
    for encoding in encodings:
        try:
            decoded = data.decode(encoding).strip('\x00')
            print(f"Decoded as {encoding}: {decoded}")
        except UnicodeDecodeError:
            print(f"Cannot decode as {encoding}")

# 检查名字修改前后的内容
print("Before modification:")
decode_name(data_before)

print("\nAfter modification:")
decode_name(data_after)
