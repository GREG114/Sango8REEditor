import tkinter as tk
from tkinter import ttk
import os,binascii
from encode import encode
ec = encode()
from tkinter import font
# 用于保存文件路径和表格行号的映射
file_path_to_row = {}
def create_window():
    # 创建主窗口
    root = tk.Tk()
    # 设置窗口标题
    root.title("三国志导出武将修改器")    
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
    tree = ttk.Treeview(frame, columns=("number","surname", "firstname", "born","died","sex"), show="headings")
    
    # 设置列标题
    tree.heading("number", text="序号")
    tree.heading("surname", text="姓")
    tree.heading("firstname", text="名")
    tree.heading("born", text="生年")
    tree.heading("died", text="卒年")
    tree.heading("sex", text="性别")
    
    # 设置列宽
    tree.column("number", width=50, minwidth=50, stretch=tk.NO)
    tree.column("surname", width=100, minwidth=100)
    tree.column("firstname", width=100, minwidth=100)
    tree.column("born", width=70, minwidth=70, stretch=tk.NO)
    tree.column("died", width=70, minwidth=70, stretch=tk.NO)
    tree.column("sex", width=50, minwidth=50, stretch=tk.NO)

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

    # 定义bin文件目录
    directory = r"C:\Users\greg_\Documents\KoeiTecmo\SAN8R\PERSONDATA\SC"

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
                    # 解析姓氏
                    surname = hex_data[48:56]  # 姓（两个汉字）
                    surname_cn = ec.decode(surname)
                    firstname = hex_data[92:100] # 名（两个汉字）
                    firstname_cn = ec.decode(firstname)    
                    sex = hex_data[152:154] # 性别（1 是女）
                    if(sex=='01'):
                        sex_str ='女'
                    else:
                        sex_str = '男'
                    # 解析生年和卒年
                    born = ec.parse_year(hex_data, 152)
                    died = ec.parse_year(hex_data, 160)
                    # 插入数据到表格中
                    tree.insert("", "end", values=(index, surname_cn, firstname_cn, born, died, sex_str), text=filename[:-4])  # text属性保存文件名
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
    directory = r"C:\Users\greg_\Documents\KoeiTecmo\SAN8R\PERSONDATA\SC"

    for item in tree.get_children():
        values = tree.item(item, "values")
        filename = tree.item(item, "text") + ".bin"  # 假设文件名是Treeview的item ID加上.bin
        file_path = os.path.join(directory, filename)

        # 收集修改后的数据
        surname = ec.encode(values[1])
        firstname = ec.encode(values[2])

        def format_year(year):
            if year < 256:
                return format(year, '04x')
            else:
                high = year // 256
                low = year % 256
            return format(high, '02x') + format(low, '02x')

        born = format_year(int(values[3]))
        died = format_year(int(values[4]))
        sex = '01' if values[4] == '女' else '00'

        # 读取原文件内容
        with open(file_path, 'rb') as file:
            data = file.read()
            hex_data = binascii.hexlify(data).decode('utf-8')

        # 修改文件内容
        hex_data = hex_data[:48] + surname + hex_data[56:92] + firstname + hex_data[100:152] + sex + hex_data[154:158] + born + hex_data[162:166] + died + hex_data[170:]

 
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

    # 获取当前选中行的数据
    values = tree.item(item, "values")

    # 创建编辑字段
    tk.Label(edit_win, text="姓:").grid(row=0, column=0)
    surname_var = tk.StringVar(value=values[1])
    surname_entry = tk.Entry(edit_win, textvariable=surname_var, validate="key", validatecommand=(edit_win.register(ec.validate_length), '%P'))
    surname_entry.grid(row=0, column=1)

    tk.Label(edit_win, text="名:").grid(row=1, column=0)
    name_var = tk.StringVar(value=values[2])
    name_entry = tk.Entry(edit_win, textvariable=name_var, validate="key", validatecommand=(edit_win.register(ec.validate_length), '%P'))
    name_entry.grid(row=1, column=1)

    tk.Label(edit_win, text="生年:").grid(row=2, column=0)
    born_var = tk.IntVar(value=values[3])
    born_entry = tk.Entry(edit_win, textvariable=born_var, validate="key", validatecommand=(edit_win.register(ec.validate_year), '%P', 'born'))
    born_entry.grid(row=2, column=1)

    tk.Label(edit_win, text="卒年:").grid(row=3, column=0)
    died_var = tk.IntVar(value=values[4])
    died_entry = tk.Entry(edit_win, textvariable=died_var, validate="key", validatecommand=(edit_win.register(ec.validate_year), '%P', 'died'))
    died_entry.grid(row=3, column=1)

    tk.Label(edit_win, text="性别:").grid(row=4, column=0)
    sex_var = tk.StringVar(value=values[5])
    sex_menu = ttk.Combobox(edit_win, textvariable=sex_var, values=["男", "女"], state="readonly")
    sex_menu.grid(row=4, column=1)

    # 保存按钮
    def save_edit():
        tree.set(item, column="surname", value=surname_var.get())
        tree.set(item, column="firstname", value=name_var.get())
        tree.set(item, column="born", value=born_var.get())
        tree.set(item, column="died", value=died_var.get())
        tree.set(item, column="sex", value=sex_var.get())
        edit_win.destroy()

    ttk.Button(edit_win, text="保存", command=save_edit).grid(row=5, columnspan=2)
# 调用函数创建窗口
create_window()
