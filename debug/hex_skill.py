def skill_decode(hex_string):
    # 转换十六进制字符串为十进制整数
    decimal_num = int(hex_string, 16)    
    if decimal_num == 0:
        # 如果输入是全0，则返回与输入长度相对应的全0四进制字符串
        return '0' * (len(hex_string) * 2)    
    quaternary = ""
    while decimal_num > 0:
        decimal_num, remainder = divmod(decimal_num, 4)
        quaternary = str(remainder) + quaternary    
    # 确保返回的四进制字符串长度为十六进制输入长度的两倍
    required_length = len(hex_string) * 2
    quaternary = quaternary.zfill(required_length)  

    if(len(quaternary)%4 !=0):
        raise ValueError("长度不是4的倍数")
    # 每四个字符分组
    gps = [quaternary[i:i+4] for i in range(0,len(quaternary),4)]
    # 每组倒叙
    rgps = [gp[::-1] for gp in gps]
    #拼接
    result = ''.join(rgps)  
    return result

# 示例使用 33333333333333333333333333333333333333333333333333333333

# ffffffffffffffff 33333333333333333333333333333333

# 前32个技能可用当前方式， 后面紧跟着两位直接解析回4进制 比如 39  解析回 321  在倒序 123  就是 33 到 35这三个技能的等级
hex_string = "4aaa0600204a490802"

print(skill_decode(hex_string)) 



# def skill_encode(quaternary_string):
#     # 检查输入字符串长度是否为4的倍数
#     if len(quaternary_string) % 4 != 0:
#         raise ValueError("输入字符串长度不是4的倍数")
    
#     # 每四个字符分组并反转
#     gps = [quaternary_string[i:i+4] for i in range(0, len(quaternary_string), 4)]
#     rgps = [gp[::-1] for gp in gps]
#     quaternary = ''.join(rgps)
    
#     # 将四进制字符串转换为十进制
#     decimal_num = 0
#     for digit in quaternary:
#         decimal_num = decimal_num * 4 + int(digit)
    
#     # 将十进制转换为十六进制字符串
#     hex_string = hex(decimal_num)[2:]  # [2:] 去掉 '0x' 前缀
    
#     # 确保返回的十六进制字符串长度为输入长度的一半
#     required_length = len(quaternary_string) // 2
#     hex_string = hex_string.zfill(required_length)

#     return hex_string

# # 示例使用
# quaternary_string = "3333333333333333"
# print(skill_encode(quaternary_string))
