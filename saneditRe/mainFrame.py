import tkinter as tk
import os
from tkinter import ttk, messagebox
from encode import encode
path = os.path.join(os.environ['USERPROFILE'], 'Documents',  'KoeiTecmo', 'SAN8R', 'SAVE_DATA','edit_personSC.bin')
ec=encode()
def open_batch_edit_window(tree):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("警告", "请先选择要批量修改的武将")
        return

    batch_edit_window = tk.Toplevel()
    batch_edit_window.title("批量修改武将属性")
    batch_edit_window.geometry("800x600")  # 调整窗口大小

    frame = ttk.Frame(batch_edit_window, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    columns = tree["columns"]
    batch_data = {}
    col_count = len(columns)

    # 计算每列的行数
    rows_per_column = (col_count + 1) // 2  # 加1是为了处理奇数列的情况

    for i, col in enumerate(columns):
        col_trl = ec.properties_savedata[col]['trl']
        row = i % rows_per_column
        column = i // rows_per_column  # 0表示左栏，1表示右栏

        ttk.Label(frame, text=col_trl).grid(row=row, column=column*2, sticky="w", padx=5, pady=5)
        entry = ttk.Entry(frame)
        entry.grid(row=row, column=column*2+1, sticky="ew", padx=5, pady=5)
        batch_data[col] = entry

    # 配置框架的列权重，使其能自适应窗口大小
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)
    frame.grid_columnconfigure(3, weight=1)

    def apply_batch_edit():
        for item in selected_items:
            for col in columns:
                new_value = batch_data[col].get()
                if new_value:
                    tree.set(item, column=col, value=new_value)
        batch_edit_window.destroy()

    ttk.Button(frame, text="确定", command=apply_batch_edit).grid(row=len(columns), column=0, columnspan=2, pady=10)

    frame.columnconfigure(1, weight=1)
def create_editable_treeview(frame, columns, data):
    tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="extended")
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

    for col in columns:
        colname = ec.properties_savedata[col]["trl"]
        tree.heading(col, text=colname)
        tree.column(col, width=50)
    
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
def mainFrame(root):
    # 创建一个框架来包含表格和滚动条
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))  # 顶部预留空间
    # 创建Treeview控件，动态列
    columns = list(ec.properties_savedata.keys())
    warriors = ec.decode_bin_file(path)
    # 创建可编辑的Treeview
    tree = create_editable_treeview(frame, columns, warriors)
    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    # 保存按钮
    def save_data(tree):
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
    # 创建保存按钮
    save_button = ttk.Button(frame, text="保存", command=lambda: save_data(tree))
    save_button.grid(row=2, column=0, columnspan=2, pady=10)
    
