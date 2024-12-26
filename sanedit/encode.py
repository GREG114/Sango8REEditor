import binascii,re
class encode:
    
    def __init__(self):        
        self.encoding = 'utf-16le'
        self.qicai = {
            '01': '大德',
            '02': '义心',
            '03': '万人敌',
            '04': '一身胆',
            '05': '锦马超',
            '06': '老当益壮',
            '07': '卧龙',
            '08': '凤雏',
            '09': '麒麟儿',
            '0a': '超世之杰',
            '0b': '王佐',
            '0c': '不屈不挠',
            '0d': '狼顾',
            '0e': '兵贵神速',
            '0f': '辽来辽来',
            '10': '金刚不坏',
            '11': '伪书疑心',
            '12': '山道强袭',
            '13': '江东猛虎',
            '14': '小霸王',
            '15': '用材',
            '16': '火神',
            '17': '冷炎',
            '18': '刮目',
            '19': '铃甘宁',
            '1a': '深谋远虑',
            '1b': '天下无双',
            '1c': '闭月羞花',
            '1d': '名门望族',
            '1e': '恶逆无道'
        }
        self.propeties={
         
        "number": {
            "column_widths": 50,
            "trl": "编号"
        }   ,
        "surname": {
            "positions": [48, 8],
            "column_widths": 100,
            "trl": "姓"
        },
        "firstname": {
            "positions": [92, 8],
            "column_widths": 100,
            "trl": "名"
        },
        "midname": {
            "positions": [136, 8],
            "column_widths": 100,
            "trl": "字"
        },
        "sex": {
            "positions": [152, 2],
            "column_widths": 50,
            "trl": "性别"
        },
        "born": {
            "positions": [154, 4],
            "column_widths": 70,
            "trl": "生年"
        },
        "died": {
            "positions": [158, 4],
            "column_widths": 70,
            "trl": "卒年"
        },
        "ty": {
            "positions": [204, 2],
            "column_widths": 70,
            "trl": "统御"
        },
        "wl": {
            "positions": [206, 2],
            "column_widths": 70,
            "trl": "武力"
        },
        "zl": {
            "positions": [208, 2],
            "column_widths": 70,
            "trl": "智力"
        },
        "zz": {
            "positions": [210, 2],
            "column_widths": 70,
            "trl": "政治"
        },
        "ml": {
            "positions": [212, 2],
            "column_widths": 70,
            "trl": "魅力"
        },
        "qy": {
            "positions": [514, 2],
            "column_widths": 70,
            "trl": "情义"
        },
        "qc": {
            "positions": [500, 2],
            "column_widths": 70,
            "trl": "奇才"
        }
        }

        self.properties_savedata = {
            "idx": {
                "positions": [0, 4],
                "column_widths": 100,
                "trl": "编号"
            },
            "surname": {
                "positions": [8, 8],
                "column_widths": 100,
                "trl": "姓"
            },
            "firstname": {
                "positions": [52, 8],
                "column_widths": 100,
                "trl": "名"
            },
            "headshot": {
                "positions": [108, 4],
                "column_widths": 100,
                "trl": "立绘编号"
            },
            "sex": {
                "positions": [112, 2],
                "column_widths": 50,
                "trl": "性别"
            },
            "born": {
                "positions": [114, 4],
                "column_widths": 70,
                "trl": "生年"
            },
            "died": {
                "positions": [118,4 ],
                "column_widths": 70,
                "trl": "卒年"
            },
            "ty": {
                "positions": [164,2 ],
                "column_widths": 70,
                "trl": "统御"
            },
            "wl": {
                "positions": [166, 2],
                "column_widths": 70,
                "trl": "武力"
            },
            "zl": {
                "positions": [168, 2],
                "column_widths": 70,
                "trl": "智力"
            },
            "zz": {
                "positions": [170, 2],
                "column_widths": 70,
                "trl": "政治"
            },
            "ml": {
                "positions": [172, 2],
                "column_widths": 70,
                "trl": "魅力"
            },
            "qy": {
                "positions": [474, 2],
                "column_widths": 70,
                "trl": "情义"
            },
            "qc": {
                "positions": [460, 2],
                "column_widths": 70,
                "trl": "奇才"
            }
            # 你可以在这里添加更多的字段
        }
    
    
    
    def encode_warrior(self, warrior_data, original_warrior_hex):
        # original_warrior_hex 是读取文件时得到的原始十六进制字符串
        modified_hex = original_warrior_hex  # 开始时使用原始数据
        
        for field, props in self.properties_savedata.items():
            if 'positions' in props:
                start, length = props['positions']
                v = warrior_data.get(field, '')
                if field in ['firstname', 'surname']:   
                    value = self.encode(v)
                elif field in ['born', 'died']:
                    value = self.format_year(int(warrior_data.get(field, '')))
                elif field in ['sex']:                    
                    if v=='男':
                        value = '00'
                    else:
                        value = '01'
                elif field == 'headshot':
                    if len(v)<=2:
                        value = format(int(v) + 87, '02x')+'1b'
                    else:                        
                        value =  hex(int(v))[2:].zfill(4)                       
                elif field in ['ty','wl','zz','zl','ml']:                    
                    value =  hex(int(v))[2:]
                elif field == 'qy':                
                    # value =  hex(int(v))[2:]
                    value =   f"{int(v):02X}"
                    ss=0
                elif field == 'qc':   
                    dict_r = {self.qicai[x]:x for x in self.qicai}
                    value =dict_r[v] 
                else:
                    value = warrior_data.get(field, '')                
                # 确保value的长度与预期的长度匹配
                if len(value) < length:
                    value += '0' * (length - len(value))
                elif len(value) > length:
                    value = value[:length]
                
                # 替换修改后的数据
                modified_hex = modified_hex[:start] + value + modified_hex[start+length:]
        
        return modified_hex
        
        
    def save_to_bin_file(self, warriors, path):
        with open(path, 'r+b') as file:  # 以读写模式打开文件
            file_content = file.read()  # 读取整个文件内容
            
            for warrior in warriors:
                original_position = warrior['original_position']
                original_length = warrior['original_length']
                
                # 提取原始的武将数据块
                original_warrior_hex = file_content[original_position // 2:(original_position + original_length) // 2].hex()
                
                # 编码修改后的武将数据
                encoded_data = self.encode_warrior(warrior, original_warrior_hex)
                newlength = len(encoded_data)
                # 确保编码后的数据长度与原始数据长度相同
                if len(encoded_data) != original_length  and len(encoded_data)< 3000:  
                    raise ValueError(f"修改后的武将数据长度与原始数据长度不匹配：{warrior['firstname']}")

                # 将修改后的数据写回文件
                file.seek(original_position // 2)
                file.write(binascii.unhexlify(encoded_data))


    def decode_bin_file(self, path):
        with open(path, 'rb') as file:
            hex_string = binascii.hexlify(file.read()).decode('utf-8')
        
        warriors = []
        i = 0
        while i < len(hex_string):
            match = re.search(r'([0-9a-f]{2})0b0903', hex_string[i:])
            hexidx=hex_string[i:]
            if match:
                warrior_start = i + match.start()
                warrior_data = {'original_position': warrior_start}
                
                # 查找下一个武将数据块的开始位置或文件末尾
                # next_warrior_start = hex_string.find('0903', warrior_start+6)-4  # 6是因为 '0b0903' 是6个字符
                next_warrior_start = hex_string.find('0b0903', warrior_start+6) - 6

                if next_warrior_start == -1:
                    next_warrior_start = len(hex_string)
                
                # 计算当前武将数据块的长度
                warrior_length = next_warrior_start - warrior_start
                warrior_data['original_length'] = warrior_length
                
                for field, props in self.properties_savedata.items():
                    if 'positions' in props:
                        start = props['positions'][0]
                        end = start + props['positions'][1]
                        value_hex = hex_string[warrior_start+start:warrior_start+end]
                        if field in ['firstname', 'surname']:
                            value = bytes.fromhex(value_hex).decode('utf-16le')
                        elif field in ['born', 'died']:
                            value = self.parse_year(value_hex)
                        elif field in ['sex']:
                            if value_hex =='00':
                                value = '男'
                            else: 
                                value = '女'
                        elif field == 'headshot':
                            if '1b' in value_hex:
                                warrior_data['headself']=True
                                value = int(value_hex[:2], 16)-87
                            else:
                                value = int(value_hex,16)
                        elif field in ['ty','wl','zz','zl','ml']:                            
                            value = int(value_hex,16)
                        elif field =='qc':
                            value = self.qicai[value_hex]
                        elif field =='qy':
                            value = int(value_hex,16)
                        else:
                            value = value_hex  # 其他字段可能需要不同的处理方式
                        warrior_data[field] = value
                
                warriors.append(warrior_data)
                i = next_warrior_start
            else:
                break
        
        return warriors



    def decode(self,data):
        try:
            byte= bytes.fromhex(data)
            decoded = byte.decode(self.encoding)
            # print(f"Decoded as {self.encoding}: {decoded}")
            return decoded
        except UnicodeDecodeError:
            print(f"Cannot decode as {self.encoding}")
            
    def encode(self, data):
        try:
            # 首先将字符串转换为utf-16le编码的字节
            encoded_bytes = data.encode('utf-16le')
            
            # 如果是单字，确保编码后的长度为4字节
            if len(data) == 1:
                encoded_bytes += b'\x00\x00'
            # 如果长度为奇数，补齐一个空字符
            elif len(encoded_bytes) % 2 != 0:
                encoded_bytes += b'\x00'
            
            # 去除前导空格并重新编码
            encoded_data = encoded_bytes.decode('utf-16le').lstrip(' ').encode('utf-16le')
            
            # 如果编码后的数据长度小于原始数据长度，补齐空字符
            if len(encoded_data) < len(encoded_bytes):
                encoded_data += b'\x00' * (len(encoded_bytes) - len(encoded_data))
            
            encoded = encoded_data.hex()
            # print(f"Encoded as {self.encoding}: {encoded}")
            return encoded
        except UnicodeDecodeError:
            print(f"Cannot encode as {self.encoding}")

    def text_to_bin(self,text_path, bin_path):
        try:
            # 打开文本文件并读取十六进制内容
            with open(text_path, "r", encoding="utf-8") as txt_file:
                hex_data = txt_file.read().strip().replace("\n", "").replace(" ", "")
            # print(hex_data)            
            # 将十六进制字符串转换为二进制数据
            bin_data = bytes.fromhex(hex_data)

            # 保存到二进制文件
            with open(bin_path, "wb") as bin_file:
                bin_file.write(bin_data)
            
            # print(f"二进制文件已保存到: {bin_path}")
        except Exception as e:
            print(f"转换失败: {e}")

    def parse_year(self,hex_r):
        """
        解析年份数据    
        :param hex_data: 16进制字符串
        :param start_index: 开始解析的索引位置
        :return: 解析后的年份
        """
        hex_data = hex_r[2:4]+hex_r[0:2]

        # year_hex = hex_data[start_index:start_index+4]
        year = int(hex_data, 16)      
        return year

    def validate_length(self,new_value):
        """限制姓和名只能输入两个汉字"""
        return len(new_value) <= 2

    def validate_year(self,new_value, field):
        """限制生年和卒年的范围"""
        if not new_value:  # 允许删除所有内容
            return True
        try:
            year = int(new_value)
            if field == 'born':
                return 151 <= year <= 250
            elif field == 'died':
                return 251 <= year <= 349
        except ValueError:
            return False
        return True
    
    def validate_int(self,new_value, field):
        """限制生年和卒年的范围"""
        if not new_value:  # 允许删除所有内容
            return True
        try:
            res = int(new_value)
            return 0<res<=99
        except ValueError:
            return False
        
    def validate_int_16(self,new_value, field):
        """限制生年和卒年的范围"""
        if not new_value:  # 允许删除所有内容
            return True
        try:
            res = int(new_value)
            return 0<res<=15
        except ValueError:
            return False
    def get_field(self, hex_data, field):
        start, length = self.propeties[field]['positions']
        return hex_data[start:start+length]

    def set_field(self, hex_data, field, value):
        # print(f"{field}修改为:{value},位置:{self.propeties[field]['positions']}")
        start, length = self.propeties[field]['positions']
        return hex_data[:start] + value + hex_data[start+length:]

    def format_year(self, year):
        hex_r = format(year, '04x')
        hex_data = hex_r[2:4]+hex_r[0:2]
        return hex_data
        # return format(year, '04x')
        # if year < 256:
        #     return format(year, '04x')
        # else:
        #     high = year // 256
        #     low = year % 256
        #     return format(high, '02x') + format(low, '02x')