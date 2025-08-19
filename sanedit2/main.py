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
tree = None
ec = encode()
warriors = ec.warriors
warrior_count_label = None  # 全局变量用于追踪武将数量Label

def update_warrior_count():
    global warrior_count_label, warriors
    if warrior_count_label:
        warrior_count_label.config(text=f"当前武将数量: {len(warriors)}")

def warriorsload():
    global warriors, tree, warrior_count_label
    if ec.decode_bin_file(path):
        warriors = ec.warriors
    # 清空现有表格
    for item in tree.get_children():
        tree.delete(item)
    # 重新插入数据
    for warrior in warriors:
        values = [warrior.get(col, "") for col in list(ec.properties_savedata.keys())]
        idx = warrior.get("idx", "")
        if not idx:
            print(f"警告：武将缺少有效 idx，跳过插入：{warrior}")
            continue
        tree.insert("", "end", values=values, iid=str(uuid.uuid4()), tags=(str(idx),))
    update_warrior_count()  # 更新武将数量

def open_batch_edit_window(tree):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("警告", "请先选择要批量修改的武将")
        return

    batch_edit_window = tk.Toplevel()
    batch_edit_window.title("批量修改武将属性")
    batch_edit_window.geometry("400x900")

    columns = list(ec.properties_savedata.keys())
    column_names = [ec.properties_savedata[col]["trl"] for col in columns]
    
    entries = {}
    for i, (col, name) in enumerate(zip(columns, column_names)):
        if col == "idx":
            continue
        ttk.Label(batch_edit_window, text=f"{name}:").grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entry = ttk.Entry(batch_edit_window, width=30)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[col] = entry

    def apply_changes():
        for col, entry in entries.items():
            new_value = entry.get().strip()
            if new_value:
                for item in selected_items:
                    values = list(tree.item(item, "values"))
                    col_index = columns.index(col)
                    values[col_index] = new_value
                    tree.item(item, values=values)
                    warrior_index = warriors.index(next(w for w in warriors if w["idx"] == tree.item(item, "values")[0]))
                    warriors[warrior_index][col] = new_value
                    font_obj = font.nametofont("TkDefaultFont")
                    text_width = font_obj.measure(new_value + "  ")
                    current_width = tree.column(column_names[col_index], "width")
                    if text_width > current_width:
                        tree.column(column_names[col_index], width=text_width)
        messagebox.showinfo("成功", "批量修改已应用")
        batch_edit_window.destroy()

    ttk.Button(batch_edit_window, text="应用修改", command=apply_changes).grid(row=len(columns), column=0, columnspan=2, pady=10)

def delete_warrior(tree):
    global warriors
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("警告", "请先选择一个武将！")
        return
    for iid in selected:
        idx = tree.item(iid, "tags")[0]
        warriors = [w for w in warriors if w["idx"] != idx]
        tree.delete(iid)
    messagebox.showinfo("成功", "已删除选中的武将！")
    update_warrior_count()  # 更新武将数量

def save():
    global warriors
    ec.warriors = warriors
    ec.save_to_bin_file(path)

def show_warrior_skills(tree):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("警告", "请先选择一个武将！")
        return
    
    first_selected = selected_items[0]
    values = tree.item(first_selected, "values")
    
    idx = None
    for warrior in warriors:
        if str(warrior.get("idx", "")) == str(values[0]):
            idx = warrior.get("idx")
            break
    
    if not idx:
        messagebox.showerror("错误", "无法找到选中的武将数据")
        return
    
    warrior = next((w for w in warriors if w["idx"] == idx), None)
    if not warrior:
        messagebox.showerror("错误", "无法找到选中的武将数据")
        return
    
    warrior_source = warrior.get('source', '')
    start_pos = ec.skill["positions"][0]
    end_pos = start_pos + ec.skill["positions"][1]
    original_skill_hex = warrior_source[start_pos:end_pos]
    
    print(f"调试信息 - 武将: {warrior.get('surname', '')}{warrior.get('firstname', '')}")
    print(f"原始技能十六进制字符串: {original_skill_hex}")
    
    skills_window = tk.Toplevel()
    skills_window.title(f"武将技能 - {warrior.get('surname', '')}{warrior.get('firstname', '')}")
    skills_window.geometry("600x500")
    
    main_frame = ttk.Frame(skills_window)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    skill_dict = warrior.get('战法', {})
    skill_entries = {}
    skill_names = list(skill_dict.keys()) if skill_dict else []
    
    ttk.Label(scrollable_frame, text="技能列表 (0=无, 1=初, 2=中, 3=极)", font=("Arial", 12, "bold")).grid(
        row=0, column=0, columnspan=8, pady=10)
    
    skills_per_column = (len(skill_names) + 3) // 4
    
    for i, skill_name in enumerate(skill_names):
        row_index = (i // 4) + 1
        col_index = (i % 4) * 2
        ttk.Label(scrollable_frame, text=skill_name).grid(row=row_index, column=col_index, sticky="w", padx=(10, 0), pady=2)
        entry = ttk.Entry(scrollable_frame, width=10)
        entry.insert(0, skill_dict.get(skill_name, "0"))
        entry.grid(row=row_index, column=col_index + 1, padx=(0, 10), pady=2)
        skill_entries[skill_name] = entry
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def save_skills():
        save_warrior_skills(warrior, skill_entries, original_skill_hex, start_pos, end_pos)
        skills_window.destroy()
    
    button_frame = ttk.Frame(skills_window)
    button_frame.pack(side="bottom", fill="x", padx=10, pady=10)
    save_button = ttk.Button(button_frame, text="保存", command=save_skills)
    save_button.pack(pady=5)

def save_warrior_skills(warrior, skill_entries, original_skill_hex, start_pos, end_pos):
    try:
        new_skills = {}
        for skill_name, entry in skill_entries.items():
            value = entry.get().strip()
            if not value.isdigit() or int(value) < 0 or int(value) > 3:
                raise ValueError(f"技能 {skill_name} 的等级必须是0-3之间的数字")
            new_skills[skill_name] = value
        skills_str_new = ec.dict_to_skill_string(new_skills)
        skills_hex_new = ec.quaternary_to_hex_战法(skills_str_new)
        warrior_source = warrior.get('source', '')
        updated_source = warrior_source[:start_pos] + skills_hex_new + warrior_source[end_pos:]
        warrior['source'] = updated_source
    except Exception as e:
        messagebox.showerror("错误", f"保存失败: {str(e)}")
        print(f"保存错误详情: {str(e)}")

def duplicate_warrior_in_tree(tree):
    global warriors
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("警告", "请先选择一个武将！")
        return
    
    selected_item = selected_items[0]
    values = tree.item(selected_item, "values")
    idx = tree.item(selected_item, "tags")[0]
    warrior = next((w for w in warriors if w["idx"] == idx), None)
    
    if not warrior:
        messagebox.showerror("错误", "无法找到选中的武将数据")
        return
    
    new_warrior = ec.duplicate_warrior(warrior)
    warriors.append(new_warrior)
    new_values = [new_warrior.get(col, "") for col in list(ec.properties_savedata.keys())]
    tree.insert("", "end", values=new_values, iid=str(uuid.uuid4()), tags=(str(new_warrior["idx"]),))
    # messagebox.showinfo("成功", f"武将已复制，新ID为: {new_warrior['idx']}")
    update_warrior_count()  # 更新武将数量

def create_new_warrior(tree):
    global warriors
    new_warrior = ec.create_new_warrior()  # 假设encode类有create_new_warrior方法
    warriors.append(new_warrior)
    new_values = [new_warrior.get(col, "") for col in list(ec.properties_savedata.keys())]
    tree.insert("", "end", values=new_values, iid=str(uuid.uuid4()), tags=(str(new_warrior["idx"]),))
    # messagebox.showinfo("成功", f"已创建新武将，ID为: {new_warrior['idx']}")
    update_warrior_count()  # 更新武将数量

def create_main_window():
    global tree, warrior_count_label
    root = tk.Tk()
    root.title("三国志8RE自建武将修改器")
    root.geometry("1280x640")
    
    menubar = tk.Menu(root)
    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=(10, 50))
    
    # 添加武将数量显示
    warrior_count_label = ttk.Label(root, text=f"当前武将数量: {len(warriors)}", font=("Arial", 12))
    warrior_count_label.pack(pady=5)
    
    columns = list(ec.properties_savedata.keys())
    column_names = [ec.properties_savedata[col]["trl"] for col in columns]
    tree = ttk.Treeview(tree_frame, columns=column_names, show="headings")
    for col, name in zip(columns, column_names):
        tree.heading(name, text=name)
        width = ec.properties_savedata[col].get("column_widths", 100)
        tree.column(name, width=width, anchor="center")
    warriorsload()

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="重新加载", command=lambda: warriorsload())
    file_menu.add_command(label="新建武将", command=lambda: create_new_warrior(tree))
    menubar.add_cascade(label="文件", menu=file_menu)
    root.config(menu=menubar)

    v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    tree.grid(row=0, column=0, sticky="nsew")
    v_scrollbar.grid(row=0, column=1, sticky="ns")
    h_scrollbar.grid(row=1, column=0, sticky="ew")
    
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    save_button = ttk.Button(root, text="保存到文件", command=lambda: save())
    save_button.pack(pady=5)

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

    def show_context_menu(event):
        selected_items = tree.selection()
        if selected_items:
            context_menu.post(event.x_root, event.y_root)

    context_menu = tk.Menu(tree, tearoff=0)
    context_menu.add_command(label="批量修改", command=lambda: open_batch_edit_window(tree))
    context_menu.add_command(label="删除武将", command=lambda: delete_warrior(tree))
    context_menu.add_command(label="查看/编辑技能", command=lambda: show_warrior_skills(tree))
    context_menu.add_command(label="复制武将", command=lambda: duplicate_warrior_in_tree(tree))
    tree.bind("<Double-1>", on_double_click)
    tree.bind("<Button-3>", show_context_menu)
    return root

if __name__ == "__main__":
    window = create_main_window()
    window.mainloop()