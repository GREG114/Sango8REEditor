class encode:
    
    def __init__(self):        
        self.encoding = 'utf-16le'
        self.qicai = {
            '00': '大德',
            '01': '义心',
            '02': '万人敌',
            '03': '一身胆',
            '04': '锦马超',
            '05': '老当益壮',
            '06': '卧龙',
            '07': '凤雏',
            '08': '麒麟儿',
            '09': '超世之杰',
            '0a': '王佐',
            '0b': '不屈不挠',
            '0c': '狼顾',
            '0d': '兵贵神速',
            '0e': '辽来辽来',
            '0f': '金刚不坏',
            '10': '伪书疑心',
            '11': '山道强袭',
            '12': '江东猛虎',
            '13': '小霸王',
            '14': '用材',
            '15': '火神',
            '16': '冷炎',
            '17': '刮目',
            '18': '铃甘宁',
            '19': '深谋远虑',
            '1a': '天下无双',
            '1b': '闭月羞花',
            '1c': '名门望族',
            '1d': '恶逆无道'
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