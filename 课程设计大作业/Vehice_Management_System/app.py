import tkinter as tk
# from tkinter import Canvas
# from PIL import Image, ImageTk, ImageEnhance
from controllers import MainController
from views import MainView
from models import Database

class VehicleManagementApp:
    def __init__(self):
        print("初始化车辆管理应用...")
        self.root = tk.Tk()     # 创建主窗口
        self.root.title("🚗 车辆信息管理系统")
        self.root.geometry("1280x800")
        self.root.configure(bg="#f0f0f0")
        print("主窗口创建完成")
        # 初始化MVC组件
        print("初始化MVC组件...")
        try:
            self.db = Database()
            self.view = MainView(self.root)  # 先创建基础视图
            self.root.after(100, self.init_controller)
            # self.controller = MainController(self.view, self.db)  # 然后创建控制器
        except Exception as e:
            print(f"初始化失败: {e}")
            self.root.destroy()
            raise
        print("应用初始化完成")

    def init_controller(self):
        """延迟初始化控制器"""
        self.controller = MainController(self.view, self.db)
        print("控制器初始化完成")

    def run(self):
        print("启动应用主循环...")
        self.root.mainloop()
        print("应用主循环结束")

    def __del__(self):
        print("清理应用资源...")
        self.db.close()
        print("数据库连接已关闭")

if __name__ == "__main__":
    print("启动车辆信息管理系统...")
    try:
        app = VehicleManagementApp()
        app.run()
    except Exception as e:
        print(f"应用运行时发生错误: {e}")
    print("应用已退出")
