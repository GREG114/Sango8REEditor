import tkinter as tk
from tkinter import ttk

def open_save_editor():
    save_editor = tk.Toplevel()
    save_editor.title("存档武将修改")
    save_editor.geometry("800x600")  # 设置窗口大小

    # 这里添加你的逻辑，例如显示表格、编辑按钮等
    # 示例：
    frame = ttk.Frame(save_editor, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # 添加示例表格
    tree = ttk.Treeview(frame, columns=("Name", "Class", "Level"), show="headings")
    tree.heading("Name", text="姓名")
    tree.heading("Class", text="职业")
    tree.heading("Level", text="等级")
    tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # 示例数据
    tree.insert("", "end", values=("张三", "战士", "50"))
    tree.insert("", "end", values=("李四", "法师", "45"))

    # 保存按钮
    ttk.Button(frame, text="保存修改", command=lambda: print("保存逻辑")).grid(row=1, column=0, pady=10)

    save_editor.mainloop()

if __name__ == "__main__":
    open_save_editor()
