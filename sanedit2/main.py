import tkinter as tk
from tkinter import ttk
from encode import encode
import os, binascii
from tkinter import font, messagebox
import uuid

# pyinstaller --onefile --hidden-import=encode main.py
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

def open_batch_edit_window(tree):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("警告", "请先选择要批量修改的武将")
        return

    batch_edit_window = tk.Toplevel()
    batch_edit_window.title("批量修改武将属性")
    batch_edit_window.geometry("400x900")

    # 获取属性列表
    columns = list(ec.properties_savedata.keys())
    column_names = [ec.properties_savedata[col]["trl"] for col in columns]
    
    # 创建输入框和标签
    entries = {}
    for i, (col, name) in enumerate(zip(columns, column_names)):
        if col == "idx":  # 跳过编号
            continue
        ttk.Label(batch_edit_window, text=f"{name}:").grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entry = ttk.Entry(batch_edit_window, width=30)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[col] = entry

    # 保存按钮
    def apply_changes():
        for col, entry in entries.items():
            new_value = entry.get().strip()
            if new_value:  # 仅处理非空输入
                for item in selected_items:
                    values = list(tree.item(item, "values"))
                    col_index = columns.index(col)
                    values[col_index] = new_value
                    tree.item(item, values=values)
                    
                    # 更新warriors数据
                    warrior_index = warriors.index(next(w for w in warriors if w["idx"] == tree.item(item, "values")[0]))
                    warriors[warrior_index][col] = new_value
                    
                    # 调整列宽
                    font_obj = font.nametofont("TkDefaultFont")
                    text_width = font_obj.measure(new_value + "  ")
                    current_width = tree.column(column_names[col_index], "width")
                    if text_width > current_width:
                        tree.column(column_names[col_index], width=text_width)
        
        messagebox.showinfo("成功", "批量修改已应用")
        batch_edit_window.destroy()

    ttk.Button(batch_edit_window, text="应用修改", command=apply_changes).grid(row=len(columns), column=0, columnspan=2, pady=10)

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

    # 创建表格框架，设置内边距以略小于root
    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=(10, 50))  # 底部留空间给按钮

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
    tree.grid(row=0, column=0, sticky="nsew")  # 使用grid确保布局
    scrollbar.grid(row=0, column=1, sticky="ns")  # 滚动条紧贴表格右侧

    # 配置tree_frame的网格权重
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    # 表格滚动条
    v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    tree.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar.grid(row=1, column=0, sticky="ew")
    
    # 配置tree_frame的网格权重
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)



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
    # 右键菜单
    def show_context_menu(event):
        selected_items = tree.selection()
        if selected_items:
            context_menu.post(event.x_root, event.y_root)
    context_menu = tk.Menu(tree, tearoff=0)
    context_menu.add_command(label="批量修改", command=lambda: open_batch_edit_window(tree))
    tree.bind("<Double-1>", on_double_click)
    tree.bind("<Button-3>", show_context_menu)
    return root

if __name__ == "__main__":
    window = create_main_window()
    window.mainloop()