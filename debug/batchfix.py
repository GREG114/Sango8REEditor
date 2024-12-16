from encode import encode
import os, binascii,json,random
ec = encode()
# 定义bin文件目录
directory = r"C:\Users\greg_\Documents\KoeiTecmo\SAN8R\PERSONDATA\SC"



def save_changes():
    """保存所有更改到文件"""
    for index, filename in enumerate(os.listdir(directory), start=1):
        file_path = os.path.join(directory, filename)                   
        # 读取原文件内容
        with open(file_path, 'rb') as file:
            data = file.read()
            hex_data = binascii.hexlify(data).decode('utf-8')

        # 修改文件内容
        for field, props in ec.propeties.items():
            if field == 'number' or 'positions' not in props:  # 跳过number字段和没有位置信息的字段
                continue            
            index = list(ec.propeties.keys()).index(field)   # 减1是因为我们跳过了number字段
            # if field in ['surname', 'firstname', 'midname']:
            #     value = ec.encode(values[index])
            # elif field == 'sex':
            #     value = '01' if values[index] == '女' else '00'
            # elif field in ['born', 'died']:
            #     value = ec.format_year(int(values[index]))
            # elif field == 'qy':                
            #     value = values[index]  # 情义，从int转16
            #     value = f"{int(value):02X}"
            # elif field == 'qc':                
            #     value = values[index]  # 奇才，这时候是中文，得从字典改回16x
            #     dict_r = {ec.qicai[x]:x for x in ec.qicai}
            #     value =dict_r[value] 
            # elif field in ['ty','wl','zz','zl','ml']:
            #     value = values[index]  # 武威，从int转16
            #     value = f"{int(value):02X}"       
            # else:
            #     value = values[index]  # 如果是其他字段，直接使用其值 
            value=''
            hex_data = ec.set_field(hex_data, field, value)
        # 保存修改到临时txt文件，每32个字符换行              
        
        temp_txt_path = os.path.join(directory, filename.replace('.bin', '.txt'))
        with open(temp_txt_path, 'w') as temp_file:
            for i in range(0, len(hex_data), 32):
                temp_file.write(hex_data[i:i+32] + '\n')

        # 使用提供的函数将txt转换为bin
        ec.text_to_bin(temp_txt_path, file_path)
        
        # 清理临时文件
        # os.remove(temp_txt_path)

    print("所有更改已保存")

file_path = r'D:\data\Code\dbg\sanedit\girls.json'

# 初始化一个空列表来存放 JSON 对象
json_list = []
# 打开文件并读取所有行
with open(file_path, 'r', encoding='utf-8') as file:
    json_list = json.load(file)
json_list =list(filter(lambda x:'EDEGREE' in x
                       and not '文盲' in x['EDEGREE']
                       and not '初中' in x['EDEGREE']
                       and not '初' in x['EDEGREE']
                       and not '中' in x['EDEGREE']
                       and not '小' in x['EDEGREE']
                       and not x['EDEGREE'] in ['小学','初中','学龄前儿童','初中毕业']
                       ,json_list))
info = {x['RNAME']:x for x in json_list if len(x['RNAME'])<4}
names = list(x['RNAME'] for x in json_list if len(x['RNAME'])<4)
namesUsed=[]
def getname():
    name =  random.choice(names)
    if not name in namesUsed:
        return name 
    else:
        return getname()
def generate_stats():
    count =5
    while True:
        ty = random.randint(50, 95)
        wl = random.randint(50, 95)
        zz = random.randint(50, 95)
        zl = random.randint(50, 95)
        
        # 检查总和是否不超过180
        if ty + wl + zz + zl <= 180:
            # 检查是否至少有一个属性值超过80
            if max(ty, wl, zz, zl) > 80:                
                return [ty, wl, zz, zl]
        count+=1
        if count>5:
            return [ty, wl, zz, zl]



for index, filename in enumerate(os.listdir(directory), start=1):
    file_path = os.path.join(directory, filename)
    with open(file_path, 'rb') as file:
        data = file.read()
        hex_data = binascii.hexlify(data).decode('utf-8')

        name = getname()
        age = random.randint(140, 180)
        age += int(info[name]['AGE'])
        random_key_value = random.choice(list(ec.qicai.items()))
        key = random_key_value[0]
        # 使用函数生成一组满足条件的属性值
        stats = generate_stats()
        ty = stats[0]
        wl = stats[1]
        zz = stats[2]
        zl = stats[3]
        ml=90

        # 修改文件内容


        for field, props in ec.propeties.items():
            value=''
            if field=='surname':
                s = name[0:1]
                value = ec.encode(s)
            elif field =='firstname':
                s=name[1:]
                value = ec.encode(s)
            elif field =='born':
                value = ec.format_year(age)
            elif field =='died':
                value = ec.format_year(age+random.randint(40,99))
            elif field == 'qc':   
                value = key
            elif field == 'ty':   
                value =f"{int(ty):02X}"  
            elif field == 'wl':   
                value =f"{int(wl):02X}"   
            elif field == 'zz':   
                value =f"{int(zz):02X}"   
            elif field == 'zl':   
                value =f"{int(zl):02X}"   
            elif field == 'ml':   
                value =f"{int(ml):02X}"    
            else:
                continue
            hex_data = ec.set_field(hex_data, field, value)
        # print(hex_data) 


    
        print(name)
        temp_txt_path = os.path.join(directory, filename.replace('.bin', '.txt'))
        with open(temp_txt_path, 'w') as temp_file:
            for i in range(0, len(hex_data), 32):
                temp_file.write(hex_data[i:i+32] + '\n')

        # 使用提供的函数将txt转换为bin
        ec.text_to_bin(temp_txt_path, file_path)
        os.remove(temp_txt_path)
        







