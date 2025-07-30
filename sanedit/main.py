import tkinter as tk
from tkinter import ttk
import os, binascii
from encode import encode
ec = encode()
from tkinter import font
from personsave_edit import open_save_editor
# pyinstaller --onefile --hidden-import=encode --hidden-import=personsave_edit main.py
# 定义bin文件目录

directory = os.path.join(os.environ['USERPROFILE'], 'Documents' ,'KoeiTecmo', 'SAN8R', 'PERSONDATA','SC')
if not os.path.exists(directory):
    raise FileNotFoundError(f"路径不存在：{directory}")
print(directory)
# 用于保存文件路径和表格行号的映射
file_path_to_row = {}

def create_window():
    # 创建主窗口
    root = tk.Tk()
    # 设置窗口标题
    root.title("三国志导出武将修改器") 

    # 创建菜单栏
    menubar = tk.Menu(root)
    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(label="存档武将修改", command=open_save_editor)
    menubar.add_cascade(label="编辑", menu=edit_menu)
    root.config(menu=menubar)
    # 设置窗口大小
    root.geometry("960x640")    
    # 创建一个框架，用于放置表格
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(40, 5))  # 顶部预留空间
    
    create_table(frame)
    # 运行主循环
    root.mainloop()

def create_table(frame):
    # 创建一个Treeview控件（表格）
    
    columns = list(ec.propeties.keys())
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    
    
 # 假设 `ec` 是你的 `DataHandler` 类的实例
    for col, props in ec.propeties.items():
        # 取出中文翻译作为标题
        heading = props.get('trl', col)  # 如果没有中文翻译，则使用原字段名
        width = props.get('column_widths', 100)  # 如果没有列宽信息，使用默认值100
        tree.heading(col, text=heading)
        tree.column(col, width=width, minwidth=width, stretch=tk.NO)
    # 创建垂直和水平滚动条
    v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    h_scrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
    
    tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    # 放置Treeview和滚动条
    tree.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar.grid(row=1, column=0, sticky="ew")

    # 让框架能够适应窗口大小
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)


    # 遍历目录中的bin文件
    for index, filename in enumerate(os.listdir(directory), start=1):
        if filename.endswith(".bin"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'rb') as file:
                # 读取文件内容
                data = file.read()
                # 转换为16进制字符串
                hex_data = binascii.hexlify(data).decode('utf-8')                
                # 校验文件头
                if hex_data.startswith("53414e385245444954504552534f4e"):
                    # 解析数据
                    data = {}
                    for field, props in ec.propeties.items():
                        if 'positions' in props:
                            field_value = ec.get_field(hex_data, field)
                            if field in ['surname', 'firstname', 'midname']:
                                data[field] = ec.decode(field_value)
                            elif field == 'sex':
                                data[field] = '女' if field_value == '01' else '男'
                            elif field =='qc':
                                data[field] = ec.qicai[field_value]
                            elif field in ['born', 'died']:
                                data[field] = ec.parse_year(field_value)
                            else :
                                data[field]=int(field_value,16)
                    
                    # 插入数据到表格中
                    # 这里我们先准备一个列表，包含所有应该插入的值
                    values = [index]  # 使用索引作为number列的值
                    for col in ec.propeties.keys():
                        if col != 'number':  # 跳过number字段
                            values.append(data.get(col, ''))  # 如果某个字段没有数据，使用空字符串
                    
                    tree.insert("", "end", values=values, text=filename[:-4])  # text属性保存文件名
                    file_path_to_row[file_path] = index


    # 双击事件处理
    def on_double_click(event):
        item = tree.selection()[0]
        edit_window(tree, item)

    tree.bind("<Double-1>", on_double_click)
    # 添加保存按钮
    save_button = ttk.Button(frame, text="保存", command=lambda: save_changes(tree))
    save_button.grid(row=2, column=0, columnspan=2, pady=10)

def save_changes(tree):
    """保存所有更改到文件"""

    for item in tree.get_children():
        values = tree.item(item, "values")
        filename = tree.item(item, "text") + ".bin"  # 假设文件名是Treeview的item ID加上.bin
        file_path = os.path.join(directory, filename)
        # 收集修改后的数据
        modified_data = {}
        for field, props in ec.propeties.items():
            if field == 'number':  # 跳过number字段
                continue
            if 'positions' in props:  # 只有当字段有位置信息时才处理
                index = list(ec.propeties.keys()).index(field)   # 减1是因为我们跳过了number字段
                value = values[index]
                if field in ['surname', 'firstname', 'midname']:
                    modified_data[field] = ec.encode(values[index])
                elif field == 'sex':
                    modified_data[field] = '01' if values[index] == '女' else '00'
                elif field in ['born', 'died']:
                    modified_data[field] = ec.format_year(int(values[index]))                
        # 读取原文件内容
        with open(file_path, 'rb') as file:
            data = file.read()
            hex_data = binascii.hexlify(data).decode('utf-8')

        # 修改文件内容
        for field, props in ec.propeties.items():
            if field == 'number' or 'positions' not in props:  # 跳过number字段和没有位置信息的字段
                continue            
            index = list(ec.propeties.keys()).index(field)   # 减1是因为我们跳过了number字段
            if field in ['surname', 'firstname', 'midname']:
                value = ec.encode(values[index])
            elif field == 'sex':
                value = '01' if values[index] == '女' else '00'
            elif field in ['born', 'died']:
                value = ec.format_year(int(values[index]))
            elif field == 'qy':                
                value = values[index]  # 情义，从int转16
                value = f"{int(value):02X}"
            elif field == 'qc':                
                value = values[index]  # 奇才，这时候是中文，得从字典改回16x
                dict_r = {ec.qicai[x]:x for x in ec.qicai}
                value =dict_r[value] 
            elif field in ['ty','wl','zz','zl','ml']:
                value = values[index]  # 武威，从int转16
                value = f"{int(value):02X}"       
            else:
                value = values[index]  # 如果是其他字段，直接使用其值
           
              
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

def edit_window(tree, item):
    """创建编辑窗口"""
    edit_win = tk.Toplevel()
    edit_win.title("编辑武将信息")
        # 调整窗口大小
    edit_win.geometry("640x400")  # 设置窗口大小为400x600像素
    
    entry = tk.Entry(edit_win)
    # 获取当前选中行的数据
    values = tree.item(item, "values")
    field_vars = {}
    # 使用ec.field_positions来动态创建编辑字段
    row = 0
    for field in ec.propeties:
        if field=='number':continue
        prop = ec.propeties[field]
        label_text = prop["trl"]
        if field in ["surname", "firstname","midname"]:
            # 处理姓和名
            # label_text = "姓" if field == "surname" else "名"
            tk.Label(edit_win, text=f"{label_text}:").grid(row=row, column=0)
            var = tk.StringVar(value=values[tree['columns'].index(field)])
            entry = tk.Entry(edit_win, textvariable=var, validate="key", validatecommand=(edit_win.register(ec.validate_length), '%P'))
            entry.grid(row=row, column=1)
            field_vars[field] = var
            row += 1
        elif field in ["born", "died"]:
            # 处理生年和卒年
            # label_text = "生年" if field == "born" else "卒年"
            tk.Label(edit_win, text=f"{label_text}:").grid(row=row, column=0)
            var = tk.IntVar(value=values[tree['columns'].index(field)])
            entry = tk.Entry(edit_win, textvariable=var, validate="key", validatecommand=(edit_win.register(ec.validate_year), '%P', field))
            entry.grid(row=row, column=1)
            field_vars[field] = var
            row += 1
        elif field == "sex":
        # 处理性别
            tk.Label(edit_win, text="性别:").grid(row=row, column=0)
            sex_cn = values[tree['columns'].index(field)]
            sex_var = tk.StringVar(value=sex_cn)
            sex_menu = ttk.Combobox(edit_win, textvariable=sex_var, values=["男", "女"], state="readonly")
            sex_menu.grid(row=row, column=1)
            field_vars[field] = sex_var
            row += 1
        elif field == "qc":
        # 处理性别
            tk.Label(edit_win, text=prop["trl"]).grid(row=row, column=0)
            sex_cn = values[tree['columns'].index(field)]
            sex_var = tk.StringVar(value=sex_cn)
            sex_menu = ttk.Combobox(edit_win, textvariable=sex_var, values=list(ec.qicai[x] for x in ec.qicai), state="readonly")
            sex_menu.grid(row=row, column=1)
            field_vars[field] = sex_var
            row += 1
        elif field =='qy':
            #情义
            tk.Label(edit_win, text=prop["trl"]).grid(row=row, column=0)
            var = tk.IntVar(value=values[tree['columns'].index(field)])
            entry = tk.Entry(edit_win, textvariable=var, validate="key", validatecommand=(edit_win.register(ec.validate_int_16), '%P', field))
            entry.grid(row=row, column=1)
            field_vars[field] = var
            row += 1
        else:
            #数值
            tk.Label(edit_win, text=prop["trl"]).grid(row=row, column=0)
            var = tk.IntVar(value=values[tree['columns'].index(field)])
            entry = tk.Entry(edit_win, textvariable=var, validate="key", validatecommand=(edit_win.register(ec.validate_int), '%P', field))
            entry.grid(row=row, column=1)
            field_vars[field] = var
            row += 1


    # 保存按钮
    def save_edit():
        # 保存编辑后的数据
        for field in field_vars:
            tree.set(item, column=field, value=field_vars[field].get())
        edit_win.destroy()


    
    entry.focus_set()
    ttk.Button(edit_win, text="保存", command=save_edit).grid(row=20, columnspan=2)
    # 绑定回车键到保存按钮
    edit_win.bind('<Return>', lambda event: save_edit())
    
    # 绑定ESC键到关闭窗口函数
    edit_win.bind('<Escape>', lambda event: edit_win.destroy())


# 调用函数创建窗口
create_window()
