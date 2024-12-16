import tkinter as tk
from tkinter import ttk, messagebox
import binascii,os
from encode import encode

ec = encode()
path = r'C:\Users\greg_\Documents\KoeiTecmo\SAN8R\SAVE_DATA\edit_personSC.bin'
path = os.path.join(os.environ['USERPROFILE'],  'KoeiTecmo', 'SAN8R', 'SAVE_DATA','edit_personSC.bin')

def create_editable_treeview(frame, columns, data):
    tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="extended")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    
    for item in data:
        tree.insert("", "end", values=tuple(item[col] for col in columns))
    
    # 双击事件处理函数
    def on_double_click(event):
        item = tree.selection()[0]
        column = tree.identify_column(event.x)
        col_index = int(column[1:]) - 1  # 获取列索引
        value = tree.item(item, "values")[col_index]
        
        # 创建一个Entry来编辑
        entry = ttk.Entry(tree)        
        def save_edit(event):
            new_value = entry.get()
            # 这里可以添加数据验证逻辑
            tree.set(item, column=column, value=new_value)
            entry.destroy()

        entry.insert(0, value)
        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: save_edit(e))
        entry.place(x=event.x, y=event.y, anchor='nw', width=tree.column(column, 'width'))
        entry.focus_set()
        entry.selection_range(0, tk.END)

    # 绑定双击事件
    tree.bind("<Double-1>", on_double_click)
    
    # 右键菜单
    def show_context_menu(event):
        selected_items = tree.selection()
        if selected_items:
            context_menu.post(event.x_root, event.y_root)

    context_menu = tk.Menu(tree, tearoff=0)
    context_menu.add_command(label="批量修改", command=lambda: open_batch_edit_window(tree))

    tree.bind("<Button-3>", show_context_menu)
    
    return tree

def open_batch_edit_window(tree):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("警告", "请先选择要批量修改的武将")
        return

    batch_edit_window = tk.Toplevel()
    batch_edit_window.title("批量修改武将属性")
    batch_edit_window.geometry("400x300")

    frame = ttk.Frame(batch_edit_window, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    columns = tree["columns"]
    batch_data = {}

    for col in columns:
        col_trl = ec.properties_savedata[col]['trl']
        ttk.Label(frame, text=col_trl).grid(row=columns.index(col), column=0, sticky="w", pady=5)
        entry = ttk.Entry(frame)
        entry.grid(row=columns.index(col), column=1, sticky="ew", pady=5)
        batch_data[col] = entry

    def apply_batch_edit():
        for item in selected_items:
            for col in columns:
                new_value = batch_data[col].get()
                if new_value:
                    tree.set(item, column=col, value=new_value)
        batch_edit_window.destroy()

    ttk.Button(frame, text="确定", command=apply_batch_edit).grid(row=len(columns), column=0, columnspan=2, pady=10)

    frame.columnconfigure(1, weight=1)

def open_save_editor():
    save_editor = tk.Toplevel()
    save_editor.title("存档武将修改")
    save_editor.geometry("1152x832")  # 设置窗口大小
    
    frame = ttk.Frame(save_editor, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # 读取并解析二进制文件
    warriors = ec.decode_bin_file(path)
    
    # 创建Treeview控件，动态列
    columns = list(ec.properties_savedata.keys())
 
    # 创建可编辑的Treeview
    tree = create_editable_treeview(frame, columns, warriors)
    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # 保存按钮
    def save_data():
        # 从Treeview中获取所有修改后的数据
        modified_warriors = []
        for item in tree.get_children():
            warrior_data = {}
            for col in columns:
                warrior_data[col] = tree.item(item, 'values')[columns.index(col)]
            # 从原始的warriors列表中获取original_position
            for original_warrior in warriors:
                if original_warrior['idx'] == warrior_data['idx']:
                    warrior_data['original_position'] = original_warrior['original_position']
                    warrior_data['original_length'] = original_warrior['original_length']
                    break
            modified_warriors.append(warrior_data)
        # 保存数据到文件
        ec.save_to_bin_file(modified_warriors, path)
        print("所有更改已保存")
    
    ttk.Button(frame, text="保存修改", command=save_data).grid(row=1, column=0, pady=10)
    
    # 确保窗口可以调整大小
    save_editor.rowconfigure(0, weight=1)
    save_editor.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    
    save_editor.mainloop()
