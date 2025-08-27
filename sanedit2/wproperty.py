from value_dict import *
import random
from encode import encode

class wproperty:

    def __init__(self,ec):
        ec = ec
        self.properties_savedata = ec.properties_savedata
    def get_random_value(self, field_name):
        wproperty=self.properties_savedata[field_name]
        type_value = wproperty['type']
        if(type_value=='dict'):
            return random.choice(wproperty['dict'])
        if(type_value=='int'):
            min = wproperty['range'][0]
            max = wproperty['range'][1]
            if wproperty['format']=="02d":
                return f"{random.randint(min, max):02d}"
            if wproperty['format']=="int(str)":
                return f"{random.randint(min, max)}"  
    def get_random_name(self):
        surname=random.choice(surnames)
        mid = random.choice(mid_names_f)
        first = random.choice(first_names_f)
        if random.random() < 0.45:  # 30% 概率只返回后一个字
            mid=''
        lastname = mid+first
        return surname,lastname

    def get_surname(self):
        return random.choice(surnames)