from PIL import Image
import json
import codecs
img = Image.open(r"D:\output\240615\ComfyUI_01729_.png")
# ComfyUI 通常把数据存在 'workflow' 或 'parameters' 字段
for key, value in img.info.items():
    print(f"Key: {key}")
    if key in ('workflow', 'prompt', 'parameters'):
        try:
            data = json.loads(value)
            pos = data['40:0']['inputs']['text_positive']
            neg = data['40:0']['inputs']['text_negative']

            # 如果 \n 是字面量（即字符串里真有反斜杠+n），就用 unicode_escape
            pos_formatted = codecs.decode(pos, 'unicode_escape')
            neg_formatted = codecs.decode(neg, 'unicode_escape')

            print("Positive prompt:")
            print(pos_formatted)
            print("\nNegative prompt:")
            print(neg_formatted)
        except:
            print("Not valid JSON:", value[:200])