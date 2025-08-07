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
tree=None
ec = encode()
warriors = ec.warriors


def warriorsload():
    global warriors
    global tree
    if ec.decode_bin_file(path) :
        warriors = ec.warriors
    # 清空现有表格
    for item in tree.get_children():
        tree.delete(item)
    # 重新插入数据
    for warrior in warriors:
        values = [warrior.get(col, "") for col in list(ec.properties_savedata.keys())]
        # 确保 idx 存在且有效
        idx = warrior.get("idx", "")
        if not idx:  # 如果 idx 为空或无效，跳过或分配默认值
            print(f"警告：武将缺少有效 idx，跳过插入：{warrior}")
            continue
        tree.insert("", "end", values=values, iid=str(uuid.uuid4()), tags=(str(idx),))

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

def delete_warrior(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("警告", "请先选择一个武将！")
        return
    for iid in selected:
        # 获取选中行的 idx（从 tags 中）
        s=tree.item(iid, "tags")
        idx = tree.item(iid, "tags")[0]
        # 从 warriors 列表中移除对应武将
        global warriors
        warriors = [w for w in warriors if w["idx"] != idx]
        # 从 Treeview 删除
        tree.delete(iid)
    messagebox.showinfo("成功", "已删除选中的武将！")
def save():
    ec.warriors=warriors
    # 检查保存时的武将数量，现在重载不会山列表，导致每次重载，前端列表都翻倍    
    ec.save_to_bin_file(path)

def show_warrior_skills(tree):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("警告", "请先选择一个武将！")
        return
    
    # 获取第一个选中的武将
    first_selected = selected_items[0]
    values = tree.item(first_selected, "values")
    
    # 通过idx找到对应的武将数据
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
    
    # 获取原始技能字符串（用于调试）
    warrior_source = warrior.get('source', '')
    start_pos = ec.skill["positions"][0]
    end_pos = start_pos + ec.skill["positions"][1]
    original_skill_hex = warrior_source[start_pos:end_pos]
    
    print(f"调试信息 - 武将: {warrior.get('surname', '')}{warrior.get('firstname', '')}")
    print(f"原始技能十六进制字符串: {original_skill_hex}")
    
    # 创建技能显示窗口
    skills_window = tk.Toplevel()
    skills_window.title(f"武将技能 - {warrior.get('surname', '')}{warrior.get('firstname', '')}")
    skills_window.geometry("600x500")  # 调整窗口大小以适应四列布局
    
    # 获取技能数据（已转换为字典）
    skill_dict = warrior.get('战法', {})
    
    # 创建主框架
    main_frame = ttk.Frame(skills_window)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # 创建可滚动的框架来显示技能
    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # 显示技能列表和等级编辑框（分四列显示）
    skill_entries = {}
    skill_names = list(skill_dict.keys()) if skill_dict else []
    
    ttk.Label(scrollable_frame, text="技能列表 (0=无, 1=初, 2=中, 3=极)", font=("Arial", 12, "bold")).grid(
        row=0, column=0, columnspan=8, pady=10)
    
    # 计算每列的技能数量
    skills_per_column = (len(skill_names) + 3) // 4  # 向上取整确保所有技能都能显示
    
    # 分四列显示技能
    for i, skill_name in enumerate(skill_names):
        # 计算当前技能应该放在第几列和第几行
        col_index = (i // skills_per_column) * 2  # 每列包含标签和输入框，所以乘以2
        row_index = (i % skills_per_column) + 1   # 从第2行开始（第1行是标题）
        
        # 技能名称标签
        ttk.Label(scrollable_frame, text=skill_name).grid(row=row_index, column=col_index, sticky="w", padx=(10, 0), pady=2)
        
        # 技能等级输入框
        entry = ttk.Entry(scrollable_frame, width=10)
        entry.insert(0, skill_dict.get(skill_name, "0"))
        entry.grid(row=row_index, column=col_index + 1, padx=(0, 10), pady=2)
        skill_entries[skill_name] = entry
    
    # 将canvas和scrollbar放入主框架
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # 保存技能修改的函数
    def save_skills():
        # 保存技能数据
        save_warrior_skills(warrior, skill_entries, original_skill_hex, start_pos, end_pos)
        skills_window.destroy()
    
    # 添加保存按钮（放在窗口底部，不在滚动区域中）
    button_frame = ttk.Frame(skills_window)
    button_frame.pack(side="bottom", fill="x", padx=10, pady=10)
    
    save_button = ttk.Button(button_frame, text="保存", command=save_skills)
    save_button.pack(pady=5)
def save_warrior_skills(warrior, skill_entries, original_skill_hex, start_pos, end_pos):
    try:
        # 验证并收集技能等级
        new_skills = {}
        for skill_name, entry in skill_entries.items():
            value = entry.get().strip()
            if not value.isdigit() or int(value) < 0 or int(value) > 3:
                raise ValueError(f"技能 {skill_name} 的等级必须是0-3之间的数字")
            new_skills[skill_name] = value
        # 获取原始技能字典
        skills_str_new = ec.dict_to_skill_string(new_skills)
        skills_hex_new=ec.quaternary_to_hex_战法(skills_str_new)
        # 更新 warrior 中的技能十六进制字符串
        warrior_source = warrior.get('source', '')
        updated_source = warrior_source[:start_pos] + skills_hex_new + warrior_source[end_pos:]
        warrior['source'] = updated_source

    except Exception as e:
        messagebox.showerror("错误", f"保存失败: {str(e)}")
        print(f"保存错误详情: {str(e)}")
def create_main_window():
    global tree
    root = tk.Tk()
    root.title("三国志8RE自建武将修改器")
    root.geometry("1280x640")
    # 创建菜单栏
    menubar = tk.Menu(root)
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
    warriorsload()

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="重新加载", command=lambda: warriorsload())
    menubar.add_cascade(label="文件", menu=file_menu)
    root.config(menu=menubar)


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
    save_button = ttk.Button(root, text="保存到文件", command=lambda: save())
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


    # Find this section in your code and modify it:
    context_menu = tk.Menu(tree, tearoff=0)
    context_menu.add_command(label="批量修改", command=lambda: open_batch_edit_window(tree))
    context_menu.add_command(label="删除武将", command=lambda: delete_warrior(tree))
    # Add this new line:
    context_menu.add_command(label="查看/编辑技能", command=lambda: show_warrior_skills(tree))
        
    tree.bind("<Double-1>", on_double_click)
    tree.bind("<Button-3>", show_context_menu)    
    return root

if __name__ == "__main__":
    window = create_main_window()
    window.mainloop()