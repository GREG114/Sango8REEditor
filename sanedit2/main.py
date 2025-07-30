import tkinter as tk
from tkinter import ttk
from encode import encode
import os, binascii
from tkinter import font
import uuid

# 定义bin文件目录
path = os.path.join(os.environ['USERPROFILE'], 'Documents', 'KoeiTecmo', 'SAN8R', 'SAVE_DATA', 'edit_personSC.bin')
if not os.path.exists(path):
    raise FileNotFoundError(f"路径不存在：{path}")

ec = encode()
warriors = None

def warriorsload(tree):
    global warriors
    warriors = ec.decode_bin_file(path)
    # 清空现有表格
    for item in tree.get_children():
        tree.delete(item)
    # 重新插入数据
    for warrior in warriors:
        values = [warrior.get(col, "") for col in list(ec.properties_savedata.keys())]
        tree.insert("", "end", values=values, iid=str(uuid.uuid4()))

def create_main_window():
    root = tk.Tk()
    root.title("三国志8RE自建武将修改器")
    root.geometry("1280x640")

    # 创建菜单栏
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="重新加载", command=lambda: warriorsload(tree))
    menubar.add_cascade(label="文件", menu=file_menu)
    root.config(menu=menubar)

    # 创建表格框架
    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # 设置表格列
    columns = list(ec.properties_savedata.keys())
    column_names = [ec.properties_savedata[col]["trl"] for col in columns]
    tree = ttk.Treeview(tree_frame, columns=column_names, show="headings")
    
    # 设置表头并自动调整列宽
    for col, name in zip(columns, column_names):
        tree.heading(name, text=name)
        width = ec.properties_savedata[col].get("column_widths", 100)
        tree.column(name, width=width, anchor="center")

    # 初始加载数据
    warriorsload(tree)

    # 表格滚动条
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # 保存按钮
    save_button = ttk.Button(root, text="保存到文件", command=lambda: ec.save_to_bin_file(warriors, path))
    save_button.pack(pady=5)

    # 编辑功能
    def on_double_click(event):
        item = tree.selection()[0]
        col = tree.identify_column(event.x)
        col_index = int(col.replace("#", "")) - 1
        col_name = columns[col_index]
        
        current_value = tree.item(item, "values")[col_index]
        
        entry = ttk.Entry(tree)
        entry.insert(0, current_value)
        entry.place(x=event.x, y=event.y, anchor="w")
        
        def save_edit(event):
            new_value = entry.get()
            values = list(tree.item(item, "values"))
            values[col_index] = new_value
            tree.item(item, values=values)
            
            warrior_index = warriors.index(next(w for w in warriors if w["idx"] == tree.item(item, "values")[0]))
            warriors[warrior_index][col_name] = new_value
            
            font_obj = font.nametofont("TkDefaultFont")
            text_width = font_obj.measure(new_value + "  ")
            current_width = tree.column(column_names[col_index], "width")
            if text_width > current_width:
                tree.column(column_names[col_index], width=text_width)
            
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.focus()

    tree.bind("<Double-1>", on_double_click)

    return root

if __name__ == "__main__":
    window = create_main_window()
    window.mainloop()