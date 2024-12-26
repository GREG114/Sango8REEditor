import tkinter as tk
from mainFrame import mainFrame 

def create_main_window():    
    root = tk.Tk()
    root.title("三国志8RE武将修改器")  
    root.geometry("1280x640")  
    # 创建菜单栏
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="导出武将修改", command=lambda: print("导出武将的编辑暂时未实现"))
    menubar.add_cascade(label="文件", menu=file_menu)
    root.config(menu=menubar)   
    mainFrame(root)    
    return root

if __name__ == "__main__":    
    window = create_main_window()
    window.mainloop()
