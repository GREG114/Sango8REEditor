import tkinter as tk
from tkinter import ttk
from encode import encode
import os, binascii,uuid
from tkinter import font, messagebox


import random
from namePick import get_name,get_surname
from wproperty import wproperty
wp=None

tree=None
warrior_count_label = None  
path = os.path.join(os.environ['USERPROFILE'], 'Documents', 'KoeiTecmo', 'SAN8R', 'SAVE_DATA', 'edit_personSC.bin')
ec = None
# 初始化编码器
def init():
    global ec,wp
    try:
        ec=encode(path)
        wp=wproperty(ec)
        if not ec.decode_bin_file():
           return "无效的武将文件！"
    except Exception as e:
        return "无效的武将文件！"
# 保存武将数据
def save():
    global warriors
    ec.warriors = warriors
    ec.save_to_bin_file(path)
# 读取武将数据
def warriorsload(reload):
    global warriors, tree, warrior_count_label
    if reload :
        ec.decode_bin_file()
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
# 表格排序方法
def sort_column(col_name, tree, reverse):
    # 找到对应的英文列名
    col = next((k for k, v in ec.properties_savedata.items() if v["trl"] == col_name), None)
    if not col:
        return  # 如果找不到对应列，直接返回
    # 获取所有行的数据
    data = [(tree.set(item, col_name), item) for item in tree.get_children()]
    # 尝试将值转换为数字进行排序，失败则按字符串排序
    try:
        data.sort(key=lambda x: float(x[0]), reverse=reverse)
    except ValueError:
        data.sort(key=lambda x: x[0], reverse=reverse)
    
    # 重新排列行
    for index, (_, item) in enumerate(data):
        tree.move(item, "", index)
    
    # 切换排序方向
    tree.heading(col_name, command=lambda: sort_column(col_name, tree, not reverse))
#更新武将数量标签
def update_warrior_count():
    global warrior_count_label, warriors
    if warrior_count_label:
        warrior_count_label.config(text=f"当前武将数量: {len(warriors)}")
# region 菜单功能
# 批量修改属性
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
        if col == 'qc':
            combo = ttk.Combobox(batch_edit_window, width=30, values=list(ec.qicai.values()))
            combo.grid(row=i, column=1, padx=5, pady=5)
            entries[col] = combo
        else:
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
        # messagebox.showinfo("成功", "批量修改已应用")
        batch_edit_window.destroy()

    ttk.Button(batch_edit_window, text="应用修改", command=apply_changes).grid(row=len(columns), column=0, columnspan=2, pady=10)
# 删除武将
def delete_warrior(tree):
    global warriors,ec
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("警告", "请先选择一个武将！")
        return
    idx_forremove=[]
    for iid in selected:
        idx = tree.item(iid, "tags")[0]
        idx_forremove.append(idx)
    ec.warriors = [w for w in warriors if w["idx"] not in idx_forremove]
    warriorsload(False)
    # messagebox.showinfo("成功", "已删除选中的武将！")
    update_warrior_count()  # 更新武将数量
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
        warrior['技能']=new_skills
        skills_str_new = ec.dict_to_skill_string(new_skills)
        skills_hex_new = ec.quaternary_to_hex_战法(skills_str_new)
        warrior_source = warrior.get('source', '')
        updated_source = warrior_source[:start_pos] + skills_hex_new + warrior_source[end_pos:]
        warrior['source'] = updated_source
        warriorsload(False)
    except Exception as e:
        messagebox.showerror("错误", f"保存失败: {str(e)}")
        print(f"保存错误详情: {str(e)}")
def duplicate_warrior_in_tree(tree):
    global warriors,ec
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("警告", "请先选择要复制的武将！")
        return    
    for item in selected_items:
        idx = tree.item(item, "tags")[0]
        warrior = next((w for w in warriors if w["idx"] == idx), None)
        if not warrior:
            messagebox.showerror("错误", f"无法找到ID为{idx}的武将数据")
            continue
        new_warrior = ec.duplicate_warrior(warrior,messagebox)
        
        if(new_warrior==None):            
            continue
        warriors.append(new_warrior)
    warriorsload(False)    
    update_warrior_count()
def rename_selected_warriors(tree):
    global warriors,wp
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("警告", "请先选择要重命名的武将！")
        return    
    for item in selected_items:
        idx = tree.item(item, "tags")[0]
        warrior = next((w for w in warriors if w["idx"] == idx), None)
        if not warrior:
            continue
        warrior['surname'],warrior['firstname']=wp.get_random_name()
    warriorsload(False)
def pic_random(tree):
    global warriors
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("警告", "请先选择要修改立绘的武将！")
        return    
    for item in selected_items:
        idx = tree.item(item, "tags")[0]
        warrior = next((w for w in warriors if w["idx"] == idx), None)
        if not warrior:
            messagebox.showerror("错误", f"无法找到ID为{idx}的武将数据")
            continue
        warrior['headshot'] = wp.get_random_value("headshot")
    warriorsload(False)
def properties_random(tree):
    global warriors
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("警告", "请先选择要修改属性的武将！")
        return    
    for item in selected_items:
        idx = tree.item(item, "tags")[0]
        warrior = next((w for w in warriors if w["idx"] == idx), None)
        if not warrior:
            messagebox.showerror("错误", f"无法找到ID为{idx}的武将数据")
            continue        
        # 随机五维属性
        properties = ['ty', 'wl', 'zz', 'ml', 'zl']
        for prop in properties:
            new_value = f"{random.randint(1, 99)}"
            warrior[prop] = new_value        
        # 随机立绘
        new_pic = f"{random.randint(1, 35):02d}"
        warrior['headshot'] = new_pic        
        # 随机姓名
        warrior['surname'],warrior['firstname']=wp.get_random_name()
        # 随机生年和死年
        born_year = random.randint(165, 210)
        min_died_year = born_year + 25
        max_died_year = min(born_year + 98, 210+98)
        died_year = random.randint(min_died_year, max_died_year)
        warrior['born'] = f"{born_year}"
        warrior['died'] = f"{died_year}"
    warriorsload(False)


# endregion
def create_main_window():
    global tree, warrior_count_label,ec
    init()
    # region 主窗口控件创建和处理
    root = tk.Tk()
    root.title("三国志8RE自建武将修改器")
    root.geometry("1280x640")
    menubar = tk.Menu(root)
    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=10, pady=(10, 50))  
    # 添加武将数量显示
    warrior_count_label = ttk.Label(root, text=f"当前武将数量: {len(ec.warriors)}", font=("Arial", 12))
    warrior_count_label.pack(pady=5)   
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="重新加载", command=lambda: warriorsload(True))
    menubar.add_cascade(label="文件", menu=file_menu)
    root.config(menu=menubar)
    columns = list(ec.properties_savedata.keys())
    column_names = [ec.properties_savedata[col]["trl"] for col in columns 
                    # if not col in ['self']
                    ]    
    tree = ttk.Treeview(tree_frame, columns=column_names, show="headings")
    for col, name in zip(columns, column_names):        
        tree.heading(name, text=name, command=lambda c=name: sort_column(c, tree, False))
        width = ec.properties_savedata[col].get("column_widths", 100)
        tree.column(name, width=width, anchor="center")             

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
    context_menu = tk.Menu(tree, tearoff=0)
    def on_double_click(event):
        item = tree.selection()[0]
        col = tree.identify_column(event.x)
        col_index = int(col.replace("#", "")) - 1
        col_name = columns[col_index]
        current_value = tree.item(item, "values")[col_index]
        
        bbox = tree.bbox(item, column=col)
        if not bbox:
            return
        
        def save_edit(widget, item, col_index, col_name):
            new_value = widget.get().strip()
            if new_value:
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
            widget.destroy()

        if col_name == 'qc':
            widget = ttk.Combobox(tree, width=15, values=list(ec.qicai.values()))
            widget.insert(0, current_value)
            widget.event_generate("<Button-1>", when="tail")  # 模拟点击展开下拉菜单
            widget.bind("<<ComboboxSelected>>", lambda e: save_edit(widget, item, col_index, col_name))  # 选择即保存
        else:
            widget = ttk.Entry(tree)
            widget.insert(0, current_value)
            widget.bind("<Return>", lambda e: save_edit(widget, item, col_index, col_name))
            widget.bind("<FocusOut>", lambda e: save_edit(widget, item, col_index, col_name))
        
        widget.place(x=bbox[0] + 2, y=bbox[1] + 2, width=bbox[2], height=bbox[3])
        widget.focus() 
    def show_context_menu(event):
        selected_items = tree.selection()
        if selected_items:
            context_menu.post(event.x_root, event.y_root)

    tree.bind("<Double-1>", on_double_click)
    tree.bind("<Button-3>", show_context_menu)
    context_menu.add_command(label="批量修改", command=lambda: open_batch_edit_window(tree))
    context_menu.add_command(label="删除武将", command=lambda: delete_warrior(tree))
    context_menu.add_command(label="查看/编辑技能", command=lambda: show_warrior_skills(tree))
    context_menu.add_command(label="复制武将", command=lambda: duplicate_warrior_in_tree(tree))
    context_menu.add_command(label="随机重命名", command=lambda: rename_selected_warriors(tree))
    context_menu.add_command(label="随机修改立绘", command=lambda: pic_random(tree))
    context_menu.add_command(label="随机修改属性", command=lambda: properties_random(tree))
    
    # endregion
    # 加载武将数据
    warriorsload(False) 
    return root
if __name__ == "__main__":
    window = create_main_window()
    window.mainloop()
    