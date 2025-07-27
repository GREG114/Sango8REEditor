import binascii
# 尝试解码名字（根据不同编码方式）
def decode_name(data):
    encodings = ["gbk", "utf-8", "utf-16le"]  # 尝试常见的编码
    for encoding in encodings:
        try:
            decoded = data.decode(encoding).strip('\x00')
            print(f"Decoded as {encoding}: {decoded}")
        except UnicodeDecodeError:
            print(f"Cannot decode as {encoding}")

encoding = 'utf-16le'
def encode(data):    
    try:
        encoded = data.encode('utf-16le').hex()     
        print(f"Encoded as {encoding}: {encoded}")
        return encoded
    except UnicodeDecodeError:
        print(f"Cannot encode as {encoding}")

def decode(data):
    try:
        byte= bytes.fromhex(data)
        decoded = byte.decode(encoding)
        print(f"Decoded as {encoding}: {decoded}")
        return decoded
    except UnicodeDecodeError:
        print(f"Cannot decode as {encoding}")
# str1 = '爆炸'
# print(encode(str1))
# str1 = '164eba4e5e8d7651e5620967007a'
# print(decode(str1))
# str1 = '164e'
# print(decode(str1))


decode_name(bytes.fromhex('7051'))
