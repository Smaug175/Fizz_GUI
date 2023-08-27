from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter.ttk import *
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

class App:
    def __init__(self, root):
        #setting title
        root.title("Fizz Law")
        #setting window size
        width=966
        height=606
        screenwidth = root.winfo_screenwidth()#获取屏幕宽度
        screenheight = root.winfo_screenheight()#获取屏幕高度
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)
        
        #添加菜单栏目
        self.menubar=Menu(root,font=("Microsoft YaHei",12,"normal"))
        self.filemenu=Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="文件", menu=self.filemenu)#添加子菜单

        self.filemenu.add_command(label="New", command=self.newfile)
        self.filemenu.add_command(label="Open", command=self.openfile)
        self.filemenu.add_separator()#添加分割线
        self.filemenu.add_command(label="Save", command=self.savefile)
        self.filemenu.add_command(label="Save As", command=self.saveasfile)
        self.filemenu.add_separator()#添加分割线
        self.filemenu.add_command(label='exit', command=root.destroy)

        self.helpmenu=Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)#添加子菜单
        self.helpmenu.add_command(label="About", command=self.about)

        root.config(menu=self.menubar)#显示菜单
        
    def newfile(self):
        messagebox.showinfo("New File", "New File")
    def openfile(self):
        messagebox.showinfo("Open File", "Open File")
    def savefile(self):
        messagebox.showinfo("Save File", "Save File")
    def saveasfile(self):
        messagebox.showinfo("Save As File", "Save As File") 

    def about(self):
        messagebox.showinfo("About", "构建菲兹定律的GUI界面")
    
if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
