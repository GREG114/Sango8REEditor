path =r'D:\data\Code\dbg\eg\edit_personSC.bin.txt'
def find_all_differences(str1, str2):
    differences = []  # 存储差异的位置
    
    # 确保两个字符串长度相同
    if len(str1) != len(str2):
        raise ValueError("The lengths of the two strings must be equal for comparison.")
    
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            differences.append(i)  # 将差异位置添加到列表
    
    return differences


with open(path,mode='r') as f:
    xxx = f.read().replace('\n','')
    idx = xxx.index('09037051')
    first = xxx[idx:idx+2278]
    last = xxx[idx+8:]
    idx = last.index('09037051')
    second = last[idx:idx+2278]
    print(first)
    print("===="*3)
    print(second)

        
    differences  = find_all_differences(first, second)

    if differences:
        for idx in differences:
            print(f"Difference at index {idx}:")
            print(f"  First string: {first[idx]}")
            print(f"  Second string: {second[idx]}")
    else:
        print("The strings are identical.")