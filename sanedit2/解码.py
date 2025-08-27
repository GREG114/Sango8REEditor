
from value_dict import *
class property_operator:
    def warrior_read_fromstr_dict(self,warrior_str,warrior_data):
        properties_known = {x:properties[x] for x in properties if properties[x]['unknown']==False}
        for x in properties_known:
            position = x.split('_')
            start = int(position[0])
            end = int(position[1])
            property = properties[x]
            field = property['col']
            value_hex = warrior_str[start:end]
            if field == 'firstname' and value_hex=='00000000' :return None
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
            skill_str_16 = warrior_str[self.skill["positions"][0]:self.skill["positions"][0]+self.skill["positions"][1]]
            skill_str = self.hex_to_quaternary_战法(skill_str_16)
            warrior_data['source'] = warrior_str
            # self.exportFile(warrior_str,warrior_data['idx'])
            
        try:
            skilldict = self.parse_skills_to_dict(skill_str)
            warrior_data['战法'] = skilldict
        except Exception as ex:
            raise ex
        
        return warrior_data
 