import binascii
import random
import os
from value_dict import *


class encode:

    def __init__(self, path=''):
        if not os.path.exists(path):
            raise FileNotFoundError(f"路径不存在：{path}")
        self.path = path
        self.warriors = []
        self.defaultw = '00000a03000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000323232323200ff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        self.encoding = 'utf-16le'
        self.qicai = {
            '00': '无',
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
            '1e': '恶逆无道',
            '65': '怪物',
            '66': '残兵谍报',
        }
        self.xg = {
            '01': '大胆',
            '02': '莽撞',
            '03': '温和',
            '04': '沉着',
            '05': '胆小',
        }
        self.skill = {
            "positions": [298, 18],
            "column_widths": 70,
            "trl": "技能"
        }
        self.skill_names = [
            '刚击', '乱击', '扰乱', '猛冲', '枪阵',
            '连击', '突击', '急袭', '骑射', '园阵',
            '齐射', '乱射', '火矢', '远射', '箭雨',
            '火箭', '混战', '连环', '突贯', '爆船',
            '烈火', '激流', '落石', '伏击', '相残',
            '奋起', '鼓舞', '谩骂', '治疗', '天启',
            '风变', '天变', '妖术', '幻术', '落雷'
        ]
        self.properties_savedata = {
          
            # "uk2": {
            #     "positions": [316, 2],
            #     "column_widths": 60,
            #     "trl": "未知2",
            #     "type": "str"
            # },           
            # "preference": {
            #     "positions": [452, 2],
            #     "column_widths": 100,
            #     "trl": "喜好",
            #     "type": "str"
            # },
            # "stunt": {
            #     "positions": [374, 12],
            #     "column_widths": 100,
            #     "trl": "特技",
            #     "type": "str"
            # },
            # "desire": {
            #     "positions": [450, 2],
            #     "column_widths": 60,
            #     "trl": "物欲",
            #     "type": "dict"
            # },
            # region 已知

            "idx": {
                "positions": [0, 4],
                "column_widths": 60,
                "trl": "编号",
                "type": "str"
            },
            "surname": {
                "positions": [8, 8],
                "column_widths": 60,
                "trl": "姓",
                "type": "utf-16le"
            },
            "firstname": {
                "positions": [52, 8],
                "column_widths": 60,
                "trl": "名",
                "type": "utf-16le"
            },
            "word": {
                "positions": [96, 8],
                "column_widths": 50,
                "trl": "字",
                "type": "utf-16le"
            },
            "headshot": {
                "positions": [108, 4],
                "column_widths": 60,
                "trl": "立绘编号",
                "type": "int",
                "range": (1, 35),
                "format": "int(str)"
            },
            "sex": {
                "positions": [112, 2],
                "column_widths": 50,
                "trl": "性别"
            },
            "voice": {
                "positions": [174, 4],
                "column_widths": 50,
                "trl":  "声音"
            },
            "born": {
                "positions": [114, 4],
                "column_widths": 50,
                "trl": "生年",
                "type": "int",
                "range": (165, 210),
                "format": "int(str)"
            },
            "died": {
                "positions": [118, 4],
                "column_widths": 50,
                "trl": "卒年"
            },
            "ty": {
                "positions": [164, 2],
                "column_widths": 50,
                "trl": "统御"
            },
            "wl": {
                "positions": [166, 2],
                "column_widths": 50,
                "trl": "武力"
            },
            "zl": {
                "positions": [168, 2],
                "column_widths": 50,
                "trl": "智力"
            },
            "zz": {
                "positions": [170, 2],
                "column_widths": 50,
                "trl": "政治"
            },
            "ml": {
                "positions": [172, 2],
                "column_widths": 50,
                "trl": "魅力"
            }, "xg": {
                "positions": [454, 2],
                "column_widths": 50,
                "trl": "性格"
            },
            "zlqx": {
                "positions": [456, 2],
                "column_widths": 50,
                "trl": "倾向"
            },
            "qc": {
                "positions": [460, 2],
                "column_widths": 70,
                "trl": "奇才"
            },
            "qy": {
                "positions": [474, 2],
                "column_widths": 50,
                "trl": "情义"
            },
            # "unknown": {
            #     "positions": [476, 2],
            #     "column_widths": 50,
            #     "trl": "未知"
            # },
            "wuming": {
                "positions": [478, 4],
                "column_widths": 50,
                "trl": "武名"
            },
            "wm": {
                "positions": [482, 4],
                "column_widths": 50,
                "trl": "文名"
            },
            "em": {
                "positions": [486, 4],
                "column_widths": 50,
                "trl": "恶名"
            },
            "zsms": {
                "positions": [476, 2],
                "column_widths": 70,
                "trl": "重视名声"
            },
            "js": {
                "positions": [490, 1010],
                "column_widths": 200,
                "trl": "介绍"
            }            
            # region 关系
            , "self": {  # 一个id，通常应该是自己
                "positions": [122, 4],
                "column_widths": 60,
                "trl": "相生自己",
                "type": "str"
            },
            "father": {
                "positions": [126, 4],
                "column_widths": 70,
                "trl": "父亲"
            },
            "mother": {
                "positions": [130, 4],
                "column_widths": 70,
                "trl": "母亲"
            },
            "wife1": {
                "positions": [134, 4],
                "column_widths": 70,
                "trl": "老婆1"
            },
            "wife2": {
                "positions": [138, 4],
                "column_widths": 70,
                "trl": "老婆2"
            },
            "wife3": {
                "positions": [142, 4],
                "column_widths": 70,
                "trl": "老婆3"
            },
            "brother1": {
                "positions": [146, 4],
                "column_widths": 70,
                "trl": "金兰1"
            },
            "brother2": {
                "positions": [150, 4],
                "column_widths": 70,
                "trl": "金兰2"
            },
            "brother3": {
                "positions": [154, 4],
                "column_widths": 70,
                "trl": "金兰3"
            }, "xt": {
                "positions": [158, 4],
                "column_widths": 70,
                "trl": "意气相投"
            }, 'relation': {
                "positions": [178, 36],
                "column_widths": 250,
                "trl": "其他关系",
                "type": "str"
            },
            # endregion
            # endregion
        }

    #技能相关
    def reorder_skills(self, skills_string):
        # 确保字符串长度是32
        if len(skills_string) != 32:
            raise ValueError("输入字符串长度必须为32")

        # 将字符串每4个字符分组
        groups = [skills_string[i:i+4]
                  for i in range(0, len(skills_string), 4)]

        # 对每个组进行倒序操作
        reversed_groups = [group[::-1] for group in groups]

        # 将倒序后的组拼接成一个字符串
        reordered_string = ''.join(reversed_groups)

        return reordered_string

    def hex_to_quaternary_战法(self, hex_string):
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

        if(len(quaternary) % 4 != 0):
            raise ValueError("长度不是4的倍数")
        # 每四个字符分组
        gps = [quaternary[i:i+4] for i in range(0, len(quaternary), 4)]
        # 每组倒叙
        rgps = [gp[::-1] for gp in gps]
        #拼接
        result = ''.join(rgps)
        return result[:35]

    def quaternary_to_hex_战法(self, quaternary):
        if len(quaternary) != 35:
            raise ValueError("四进制字符串长度必须为35")

        # 补齐到36位（在末尾补0）
        quaternary = quaternary + '0'

        # 按每4位分组（共9组）
        groups = [quaternary[i:i+4] for i in range(0, len(quaternary), 4)]

        # 每组倒序
        reversed_groups = [group[::-1] for group in groups]

        # 拼接
        full_quaternary = ''.join(reversed_groups)

        # 转换为十六进制
        decimal = 0
        for i, digit in enumerate(full_quaternary[::-1]):
            decimal += int(digit) * (4 ** i)

        # 转十六进制，补齐18位
        hex_result = format(decimal, 'x').zfill(18)
        return hex_result[:18]

    def parse_skills_to_dict(self, ordered_skills):
        # 定义技能名称列表，按照图片从左到右，从上到下的顺序
        skill_names = self.skill_names
        # 检查输入字符串长度是否为32
        if len(ordered_skills) != 35:
            raise ValueError("输入字符串长度必须为35")
        # 创建一个字典来保存技能和等级
        skills_dict = {}
        # 遍历技能名称和对应的等级
        for i, skill_name in enumerate(skill_names):
            skills_dict[skill_name] = ordered_skills[i]
        return skills_dict

    def dict_to_skill_string(self, skills_dict):
        if len(skills_dict) != 35:
            raise ValueError("技能字典必须包含35个技能")
        return ''.join(skills_dict.get(name, '0') for name in self.skill_names)

    def encode_warrior(self, warrior_data, original_warrior_hex=''):
        # original_warrior_hex 是读取文件时得到的原始十六进制字符串
        modified_hex = warrior_data['source']
        firstname = warrior_data.get('firstname', '')
        if firstname == '00000000':
            return modified_hex
        for field, props in self.properties_savedata.items():
            if 'positions' in props:
                start, length = props['positions']
                v = warrior_data.get(field, '')
                if field in ['firstname', 'surname', 'word', 'js']:
                    value = self.encode(v, True)
                    if field == 'js':
                        value = value.ljust(1010, '0')
                        pass
                elif field in ['born', 'died']:
                    value = self.format_year(int(warrior_data.get(field, '')))
                elif field in ['sex']:
                    if v == '男':
                        value = '00'
                    else:
                        value = '01'
                elif field == 'headshot':
                    if len(str(v)) <= 2:
                        value = format(int(v) + 87, '02x')+'1b'
                    else:
                        value = hex(int(v))[2:].zfill(4)
                elif field in ['ty', 'wl', 'zz', 'zl', 'ml']:
                    value = f"{int(v):02x}"
                elif field == 'qy':
                    value = f"{int(v):02x}"
                elif field == 'qc':
                    dict_r = {self.qicai[x]: x for x in self.qicai}
                    value = dict_r[v]
                elif field == 'xg':
                    dict_r = {self.xg[x]: x for x in self.xg}
                    value = dict_r[v]
                # 确保value的长度与预期的长度匹配
                # elif field =='em':
                #     v=str(v)
                #     value =  f"{int(v):04x}"
                #     value=value[2:4]+value[0:2]

                elif field in ['wm', 'wuming', 'em']:
                    v = str(v)
                    value = f"{int(v):04x}"
                    value = value[2:4]+value[0:2]
                else:
                    value = warrior_data.get(field, '')

                # if len(value) < length:
                #     value += '0' * (length - len(value))
                # elif len(value) > length:
                #     value = value[:length]

                # 替换修改后的数据
                modified_hex = modified_hex[:start] + \
                    value + modified_hex[start+length:]
                # if(warrior_data['idx']=='bc0b' and field=='wuming'):
                #     print(warrior_data['surname'],warrior_data['firstname'],modified_hex[474:490])
        return modified_hex

    def get_next_id(self, current_id):
        """
        根据当前编号返回下一位编号，处理反序和进位逻辑。
        :param current_id: 当前编号，如 'b90b'
        :return: 下一位编号，如 'ba0b'
        """
        # 将反序编号转换为正常顺序
        reversed_id = current_id[2:4] + current_id[0:2]
        # 转换为十进制
        num = int(reversed_id, 16)
        # 递增
        num += 1
        # 转换回十六进制，补齐4位
        next_id = format(num, '04x')
        # 变回反序
        return next_id[2:4] + next_id[0:2]

    def find_next_available_position(self):
        """
        查找下一个可用的武将位置
        :return: (position, id) 下一个可用位置和对应的ID
        """
        # 获取当前所有已存在的ID列表
        existing_ids = [w['idx'] for w in self.warriors]

        # 默认起始ID为'b90b'
        current_id = 'b90b'

        # 遍历位置，从0开始
        for position in range(150):  # 最多150个武将
            # 检查当前ID是否已存在
            if current_id not in existing_ids:
                return (position * 2294, current_id)
            # 获取下一个ID
            current_id = self.get_next_id(current_id)

        # 如果没有找到可用位置，返回None
        return (None, None)

    def duplicate_warrior(self, warrior_data, messagebox=None):
        """
        复制武将数据并生成新的唯一ID
        :param warrior_data: 要复制的武将数据
        :return: 新的武将数据
        """
        # 创建新武将数据副本
        new_warrior = warrior_data.copy()
        # 查找下一个可用位置和ID
        position, new_id = self.find_next_available_position()

        if position is None or new_id is None:
            if messagebox:
                messagebox.showerror("错误", "没有可用的武将位置")
            return None

        # 更新新武将的ID
        new_warrior['idx'] = new_id

        # 查找新武将的存储位置
        # 从'b90b'开始尝试查找空位
        target_id = 'b90b'
        target_position = 0

        # 创建一个已存在ID到位置的映射
        id_to_position = {w['idx']: w['original_position']
                          for w in self.warriors}

        # 查找第一个空位
        while target_id in id_to_position:
            target_id = self.get_next_id(target_id)
            target_position += 2294

        # 设置新武将的存储位置
        new_warrior['original_position'] = target_position
        new_warrior['original_length'] = 2294
        new_warrior['self'] = new_id
        # 重新编码整个武将数据
        new_warrior['source'] = self.encode_warrior(new_warrior)

        return new_warrior

    def create_new_warrior(self):
        """
        使用默认武将数据创建一个新的武将
        :return: 新的武将数据
        """
        # 查找下一个可用位置和ID
        position, new_id = self.find_next_available_position()

        if position is None or new_id is None:
            raise Exception("没有可用的武将位置")

        # 使用默认数据创建新武将
        new_warrior_data = self.warrior_read_fromstr(self.defaultw, {})

        if new_warrior_data is not None:
            # 更新ID和位置信息
            new_warrior_data['idx'] = new_id
            new_warrior_data['original_position'] = position
            new_warrior_data['original_length'] = 2294
            # 确保source是完整的默认数据
            new_warrior_data['source'] = self.defaultw
        else:
            # 如果解析失败，创建一个基本的武将数据结构
            new_warrior_data = {
                'idx': new_id,
                'original_position': position,
                'original_length': 2294,
                'source': self.defaultw,
                'surname': '',
                'firstname': '',
                'word': '',
                'headshot': 0,
                'sex': '男',
                'born': 180,
                'died': 250,
                'father': '0000',
                'mother': '0000',
                'wife1': '0000',
                'wife2': '0000',
                'wife3': '0000',
                'ty': 50,
                'xt': 50,
                'wl': 50,
                'zl': 50,
                'zz': 50,
                'ml': 50,
                'qy': 0,
                'qc': '大德',
                'js': ''
            }

        # 重新编码整个武将数据，确保ID被正确设置
        encoded_source = self.encode_warrior(new_warrior_data)
        new_warrior_data['source'] = encoded_source

        return new_warrior_data

    def save_to_bin_file(self, path):
        with open(path, 'r+b') as file:  # 以读写模式打开文件
            # 创建一个足够大的空字符串，最多150个武将位置
            file_content = '0' * (2294 * 150)
            file_content = list(file_content)  # 转换为列表以便修改

            # 将每个武将放到正确的位置
            for warrior in self.warriors:
                encoded_data = self.encode_warrior(warrior)
                position = warrior.get('original_position', 0)

                # 确保encoded_data长度正确
                if len(encoded_data) > 2294:
                    encoded_data = encoded_data[:2294]
                elif len(encoded_data) < 2294:
                    encoded_data = encoded_data.ljust(2294, '0')

                # 将数据放到正确位置
                for i, char in enumerate(encoded_data):
                    if position + i < len(file_content):
                        file_content[position + i] = char

            # 将剩余位置填充为默认武将数据
            for i in range(len(self.warriors), 150):
                position = i * 2294
                default_data = self.defaultw
                for j, char in enumerate(default_data):
                    if position + j < len(file_content):
                        file_content[position + j] = char

            # 转换回字符串并写入文件
            file_content_str = ''.join(file_content)
            file.write(bytes.fromhex(file_content_str))
            file.close()

    def introduce_decode(self, value_hex):
        try:
            # 转换为字节序列
            bytes_data = bytes.fromhex(value_hex)
            valid_length = 0
            # 按2字节步长尝试解码
            for i in range(0, len(bytes_data), 2):
                if i + 2 > len(bytes_data):  # 确保有足够字节
                    break
                try:
                    valid_length = i + 2
                except UnicodeDecodeError:
                    break
            # 返回有效部分的十六进制字符串
            result = bytes_data[:valid_length].hex()
            return result
        except ValueError as e:
            print(f"Error: Invalid hex string '{value_hex}' ({e})")
            return value_hex

    def warrior_read_fromstr(self, warrior_str, warrior_data):
        x = self.properties_savedata["firstname"]['positions'][0]
        firstname = warrior_str[x:x+8]
        if firstname == '00000000':
            return None
        for field, props in self.properties_savedata.items():
            if 'positions' in props:
                start = props['positions'][0]
                end = start + props['positions'][1]
                value_hex = warrior_str[start:end]
                if field in ['firstname', 'surname', 'word', 'js']:
                    value_hex = self.introduce_decode(value_hex)
                    value = bytes.fromhex(value_hex).decode('utf-16le')
                elif field in ['born', 'died']:
                    value = self.parse_year(value_hex)
                elif field in ['sex']:
                    if value_hex == '00':
                        value = '男'
                    else:
                        value = '女'
                elif field == 'headshot':
                    if '1b' in value_hex:
                        warrior_data['headself'] = True
                        value = int(value_hex[:2], 16)-87
                    else:
                        value = int(value_hex, 16)
                elif field in ['ty', 'wl', 'zz', 'zl', 'ml']:
                    value = int(value_hex, 16)
                elif field == 'qc':
                    value = self.qicai[value_hex]
                elif field == 'qy':
                    value = int(value_hex, 16)
                elif field == 'xg':
                    value = self.xg[value_hex]
                elif field in ['wuming', 'wm', 'em']:
                    value_hex = value_hex[2:4] + \
                        value_hex[0:2]  # 从 '07D0' 变为 'D007'
                    value = int(value_hex, 16)  # 转为整数，'D007' -> 53255
                else:
                    value = value_hex  # 其他字段可能需要不同的处理方式
                warrior_data[field] = value
        if(warrior_data['idx'] in ['bc0b','b90b']):
            print(warrior_data['surname'],warrior_data['firstname'],warrior_str[460:490])
        # properties_known = {x:properties[x] for x in properties if properties[x]['unknown']==False}
        # for x in properties_known:
        #     position = x.split('_')
        #     start = int(position[0])
        #     end = int(position[1])
        #     property = properties[x]
        #     field = property['col']
        #     value_hex = warrior_str[start:end]
        #     if field in ['firstname', 'surname', 'word', 'js']:
        #         value_hex = self.introduce_decode(value_hex)
        #         value = bytes.fromhex(value_hex).decode('utf-16le')
        #     elif field in ['born', 'died']:
        #         value = self.parse_year(value_hex)
        #     elif field in ['sex']:
        #         if value_hex == '00':
        #             value = '男'
        #         else:
        #             value = '女'
        #     elif field == 'headshot':
        #         if '1b' in value_hex:
        #             warrior_data['headself'] = True
        #             value = int(value_hex[:2], 16)-87
        #         else:
        #             value = int(value_hex, 16)
        #     elif field in ['ty', 'wl', 'zz', 'zl', 'ml']:
        #         value = int(value_hex, 16)
        #     elif field == 'qc':
        #         value = self.qicai[value_hex]
        #     elif field == 'qy':
        #         value = int(value_hex, 16)
        #     elif field == 'xg':
        #         value = self.xg[value_hex]
        #     elif field in ['wuming', 'wm', 'em']:
        #         value_hex = value_hex[2:4] + \
        #             value_hex[0:2]  # 从 '07D0' 变为 'D007'
        #         value = int(value_hex, 16)  # 转为整数，'D007' -> 53255
        #     else:
        #         value = value_hex  # 其他字段可能需要不同的处理方式
            
        #     warrior_data[field] = value



        skill_str_16 = warrior_str[self.skill["positions"][0]:self.skill["positions"][0]+self.skill["positions"][1]]
        skill_str = self.hex_to_quaternary_战法(skill_str_16)
        # self.exportFile(warrior_str,warrior_data['idx'])
        warrior_data['source'] = warrior_str
        try:
            skilldict = self.parse_skills_to_dict(skill_str)
            warrior_data['战法'] = skilldict
        except Exception as ex:
            pass
        return warrior_data

    def warrior_read(self, warrior_start, hex_string):
        warrior_data = {'original_position': warrior_start}
        warrior_data['original_length'] = 2294
        warrior_str = hex_string[warrior_start:warrior_start+2294]
        warrior_data = self.warrior_read_fromstr(warrior_str, warrior_data)
        return warrior_data

    def decode_bin_file(self):
        with open(self.path, 'rb') as file:
            hex_string = binascii.hexlify(file.read()).decode('utf-8')
        self.warriors = []
        lenth = len(hex_string)/2294
        for i in range(0, int(lenth)):
            warrior_start = i*2294
            try:
                warrior_data = self.warrior_read(warrior_start, hex_string)
                if warrior_data != None:
                    self.warriors.append(warrior_data)
            except Exception as ex:
                print(ex)
        return True

    def wrap_string(self, s, width=32):
        return '\n'.join(s[i:i+width] for i in range(0, len(s), width))

    def exportFile(self, data, idx):
        outpath = rf'warriors\{idx}.txt'
        with open(outpath, 'w', encoding='utf-8') as f:
            dataformated = self.wrap_string(data)
            f.write(dataformated)
            f.close()

    def decode(self, data):
        try:
            byte = bytes.fromhex(data)
            decoded = byte.decode(self.encoding)
            # print(f"Decoded as {self.encoding}: {decoded}")
            return decoded
        except UnicodeDecodeError:
            print(f"Cannot decode as {self.encoding}")

    def encode(self, data, utf16=False):
        try:
            # 首先将字符串转换为utf-16le编码的字节
            encoded_bytes = data.encode('utf-16le')

            # 如果是单字，确保编码后的长度为4字节
            if len(data) == 1:
                encoded_bytes += b'\x00\x00'
            # 如果长度为奇数，补齐一个空字符
            elif len(encoded_bytes) % 2 != 0:
                encoded_bytes += b'\x00'

            if utf16:
                if data == '00000000':
                    return data
            # 去除前导空格并重新编码
            encoded_data = encoded_bytes.decode(
                'utf-16le').lstrip(' ').encode('utf-16le')

            # 如果编码后的数据长度小于原始数据长度，补齐空字符
            if len(encoded_data) < len(encoded_bytes):
                encoded_data += b'\x00' * \
                    (len(encoded_bytes) - len(encoded_data))

            encoded = encoded_data.hex()
            # print(f"Encoded as {self.encoding}: {encoded}")
            return encoded
        except UnicodeDecodeError:
            print(f"Cannot encode as {self.encoding}")

    def text_to_bin(self, text_path, bin_path):
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

    def parse_year(self, hex_r):
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

    def validate_length(self, new_value):
        """限制姓和名只能输入两个汉字"""
        return len(new_value) <= 2

    def validate_year(self, new_value, field):
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

    def validate_int(self, new_value, field):
        """限制生年和卒年的范围"""
        if not new_value:  # 允许删除所有内容
            return True
        try:
            res = int(new_value)
            return 0 < res <= 99
        except ValueError:
            return False

    def validate_int_16(self, new_value, field):
        """限制生年和卒年的范围"""
        if not new_value:  # 允许删除所有内容
            return True
        try:
            res = int(new_value)
            return 0 < res <= 15
        except ValueError:
            return False

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
