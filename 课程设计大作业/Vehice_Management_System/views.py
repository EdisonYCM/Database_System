import tkinter
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

class MainView:
    def __init__(self, root):
        self.controller = None
        self.root = root
        self.setup_styles()
        # 只创建框架，不创建具体控件
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)        # 初始化各标签页框架（空容器）
        # 初始化各标签页变量（但不创建）
        self.brand_frame = None
        self.series_frame = None
        self.model_frame = None
        self.sale_frame = None
        self.query_frame = None

    def set_controller(self, controller):
        """由控制器调用的设置方法"""
        self.controller = controller
        self.create_full_interface()
        print("控制器已设置，界面创建完成")

    def create_full_interface(self):
        """创建所有界面组件"""
        self.create_brand_tab()
        self.create_series_tab()
        self.create_model_tab()
        self.create_sale_tab()
        self.create_query_tab()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # 字体设置
        self.title_font = Font(family="Microsoft YaHei", size=12, weight="bold")
        self.normal_font = Font(family="Microsoft YaHei", size=10)
        # 样式配置
        self.style.configure('TFrame', background="#f0f0f0")
        self.style.configure('TLabel', background="#f0f0f0", font=self.normal_font)
        self.style.configure('TButton', font=self.normal_font, padding=5)
        self.style.configure('Treeview.Heading', font=self.title_font)
        self.style.configure('Treeview', font=self.normal_font, rowheight=25)
        # 按钮样式
        self.style.configure('Accent.TButton', foreground='white', background='#4a6baf')
        self.style.configure('Danger.TButton', foreground='white', background='#dc3545')
        self.style.configure('Info.TButton', foreground='white', background='#17a2b8')
        self.style.map('Accent.TButton',
                       foreground=[('active', 'white'), ('!active', 'white')],
                       background=[('active', '#3a5a9f'), ('!active', '#4a6baf')])
        self.style.map('Danger.TButton',
                       foreground=[('active', 'white'), ('!active', 'white')],
                       background=[('active', '#c82333'), ('!active', '#dc3545')])
        self.style.map('Info.TButton',
                       foreground=[('active', 'white'), ('!active', 'white')],
                       background=[('active', '#138496'), ('!active', '#17a2b8')])

    # ========== 品牌管理标签页 ==========
    def create_brand_tab(self):
        self.brand_frame = ttk.Frame(self.notebook)
        # 输入表单
        input_frame = ttk.LabelFrame(self.brand_frame, text="➕ 品牌信息录入", padding=10)

        ttk.Label(input_frame, text="品牌名称:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.brand_name = ttk.Entry(input_frame, font=self.normal_font)
        self.brand_name.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(input_frame, text="总部地址:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.brand_hq = ttk.Entry(input_frame, font=self.normal_font)
        self.brand_hq.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(input_frame, text="成立年份:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.brand_year = ttk.Entry(input_frame, font=self.normal_font)
        self.brand_year.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        btn_frame = ttk.Frame(input_frame)
        self.brand_add_btn = ttk.Button(btn_frame, text="添加品牌", style='Accent.TButton',command=lambda: print("添加品牌按钮被点击") or self.controller.add_brand())
        self.brand_add_btn.pack(side='left', padx=5)
        self.brand_clear_btn = ttk.Button(btn_frame, text="清空表单", command=self.clear_brand_form)
        self.brand_clear_btn.pack(side='left', padx=5)
        self.brand_delete_btn = ttk.Button(btn_frame, text="删除品牌", style='Danger.TButton',command=lambda: print("删除品牌按钮被点击") or self.controller.delete_brand())
        self.brand_delete_btn.pack(side='left', padx=5)
        btn_frame.grid(row=3, columnspan=2, pady=10)

        input_frame.pack(pady=10, padx=10, fill='x')
        # 数据表格
        columns = ("brand_id", "name", "headquarters", "founded_year")
        self.brand_tree = ttk.Treeview(self.brand_frame, columns=columns, show='headings')

        for col in columns:
            self.brand_tree.heading(col, text=col.replace('_', ' ').title())
            self.brand_tree.column(col, width=150, anchor='center')

        scrollbar = ttk.Scrollbar(self.brand_frame, orient="vertical", command=self.brand_tree.yview)
        self.brand_tree.configure(yscrollcommand=scrollbar.set)

        self.brand_tree.pack(side='left', expand=True, fill='both', padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)

        self.notebook.add(self.brand_frame, text="🏷️ 品牌管理")

    # ========== 车系管理标签页 ==========
    def create_series_tab(self):
        self.series_frame = ttk.Frame(self.notebook)
        # 输入表单
        input_frame = ttk.LabelFrame(self.series_frame, text="➕ 车系信息录入", padding=10)

        ttk.Label(input_frame, text="所属品牌:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.series_brand_combo = ttk.Combobox(input_frame, state='readonly')
        self.series_brand_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(input_frame, text="车系名称:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.series_name = ttk.Entry(input_frame, font=self.normal_font)
        self.series_name.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(input_frame, text="车系类型:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.series_category = ttk.Combobox(input_frame, values=['Sedan', 'SUV', 'Coupe', 'Electric'], state='readonly')
        self.series_category.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.series_category.current(0)

        btn_frame = ttk.Frame(input_frame)
        self.series_add_btn = ttk.Button(btn_frame, text="添加车系", style='Accent.TButton',command=lambda: print("添加车系按钮被点击") or self.controller.add_series())
        self.series_add_btn.pack(side='left', padx=5)
        self.series_clear_btn = ttk.Button(btn_frame, text="清空表单", command=self.clear_series_form)
        self.series_clear_btn.pack(side='left', padx=5)
        self.series_price_btn = ttk.Button(btn_frame, text="批量调价", style='Info.TButton',command=lambda: print("批量调价按钮被点击") or self.controller.show_price_update_dialog())
        self.series_price_btn.pack(side='left', padx=5)
        btn_frame.grid(row=3, columnspan=2, pady=10)

        input_frame.pack(pady=10, padx=10, fill='x')
        # 数据表格
        columns = ("series_id", "brand", "name", "category")
        self.series_tree = ttk.Treeview(self.series_frame, columns=columns, show='headings')

        for col in columns:
            self.series_tree.heading(col, text=col.replace('_', ' ').title())
            self.series_tree.column(col, width=150, anchor='center')

        scrollbar = ttk.Scrollbar(self.series_frame, orient="vertical", command=self.series_tree.yview)
        self.series_tree.configure(yscrollcommand=scrollbar.set)

        self.series_tree.pack(side='left', expand=True, fill='both', padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)

        self.notebook.add(self.series_frame, text="🚙 车系管理")

    # ========== 车型管理标签页 ==========
    def initialize_model_data(self):
        """确保车型管理界面数据初始化"""
        if not self.model_brand_combo['values']:
            # 如果品牌数据未加载，从控制器获取
            if hasattr(self, 'controller'):
                brands = self.controller.get_all_brands()
                self.model_brand_combo['values'] = [f"{b['brand_id']}:{b['name']}" for b in brands]
                if brands:
                    self.model_brand_combo.current(0)
                    # 手动触发车系加载
                    self.controller.load_series_for_model(
                        int(brands[0]['brand_id'])
                    )
    def load_model_brand_data(self):
        """加载品牌数据到车型管理界面的下拉框"""
        try:
            brands = self.controller.db.get_all_brands()
            brand_values = [f"{b['brand_id']}:{b['name']}" for b in brands]
            self.model_brand_combo['values'] = brand_values
            if brand_values:
                self.model_brand_combo.current(0)
                self.on_model_brand_selected()  # 初始化车系数据
        except Exception as e:
            messagebox.showerror("错误", f"加载品牌数据失败: {str(e)}")
    def on_model_brand_selected(self, event=None):
        """车型管理界面的品牌选择变化时加载对应车系"""
        print(f"品牌选择变化事件触发，当前选择: {self.model_brand_combo.get()}")
        selected = self.model_brand_combo.get()
        if selected and ":" in selected:
            brand_id = int(selected.split(":")[0])
            try:
                # 通过控制器获取车系数据
                if self.controller:  # 确保控制器存在
                    series = self.controller.db.get_series_by_brand(brand_id)
                    series_values = [f"{s['series_id']}:{s['name']}" for s in series]
                    self.model_series_combo['values'] = series_values
                    if series_values:
                        self.model_series_combo.current(0)
                else:
                    print("警告: 控制器未初始化")
            except Exception as e:
                messagebox.showerror("错误", f"加载车系数据失败: {str(e)}")
    def create_model_tab(self):
        self.model_frame = ttk.Frame(self.notebook)
        # 车型类型选择
        type_frame = ttk.LabelFrame(self.model_frame, text="🚘 选择车型类型", padding=10)
        self.model_type = tk.StringVar(value="combustion")

        ttk.Radiobutton(type_frame, text="燃油车型", variable=self.model_type,
                        value="combustion", command=self.toggle_model_fields).pack(side='left', padx=10)
        ttk.Radiobutton(type_frame, text="电动车型", variable=self.model_type,
                        value="electric", command=self.toggle_model_fields).pack(side='left', padx=10)
        type_frame.pack(pady=10, padx=10, fill='x')
        # 动态表单
        self.form_frame = ttk.LabelFrame(self.model_frame, text="📝 车型信息", padding=10)
        # 品牌和车系选择
        ttk.Label(self.form_frame, text="所属品牌:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.model_brand_combo = ttk.Combobox(self.form_frame, state='readonly')
        self.model_brand_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(self.form_frame, text="所属车系:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.model_series_combo = ttk.Combobox(self.form_frame, state='readonly')
        # self.series_brand_combo = ttk.Combobox(self.form_frame, state='readonly')
        self.model_series_combo.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        # 加载品牌数据并绑定事件
        self.load_model_brand_data()
        self.model_brand_combo.bind('<<ComboboxSelected>>', self.on_model_brand_selected)
        # 强制初始化数据
        self.root.after(100, self.initialize_model_data)  # 延迟确保组件就绪
        # 车型名称
        ttk.Label(self.form_frame, text="车型名称:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.model_name = ttk.Entry(self.form_frame, font=self.normal_font)
        self.model_name.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        # 动态字段
        self.combustion_fields = self.create_combustion_fields()
        self.electric_fields = self.create_electric_fields()
        self.toggle_model_fields()
        # 按钮
        btn_frame = ttk.Frame(self.form_frame)
        self.model_add_btn = ttk.Button(btn_frame, text="添加车型", style='Accent.TButton',command=lambda: print("添加车型按钮被点击") or self.controller.add_model())
        self.model_add_btn.pack(side='left', padx=5)
        self.model_clear_btn = ttk.Button(btn_frame, text="清空表单", command=self.clear_model_form)
        self.model_clear_btn.pack(side='left', padx=5)
        btn_frame.grid(row=6, columnspan=2, pady=10)

        self.form_frame.pack(pady=10, padx=10, fill='x')
        # 数据表格
        columns = ("model_id", "brand", "series", "model_name", "type", "production_year", "spec")
        self.model_tree = ttk.Treeview(self.model_frame, columns=columns, show='headings')

        for col in columns:
            self.model_tree.heading(col, text=col.replace('_', ' ').title())
            self.model_tree.column(col, width=120, anchor='center')

        scrollbar = ttk.Scrollbar(self.model_frame, orient="vertical", command=self.model_tree.yview)
        self.model_tree.configure(yscrollcommand=scrollbar.set)

        self.model_tree.pack(side='left', expand=True, fill='both', padx=(10, 0), pady=10)
        scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)

        self.notebook.add(self.model_frame, text="🚘 车型管理")

    def create_combustion_fields(self):
        frame = ttk.Frame(self.form_frame)

        ttk.Label(frame, text="发动机型号:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.engine_code = ttk.Entry(frame, font=self.normal_font)
        self.engine_code.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(frame, text="马力(HP):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.horsepower = ttk.Entry(frame, font=self.normal_font)
        self.horsepower.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(frame, text="燃油类型:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.fuel_type = ttk.Combobox(frame, values=['Petrol', 'Diesel'], state='readonly')
        self.fuel_type.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.fuel_type.current(0)

        return frame

    def create_electric_fields(self):
        frame = ttk.Frame(self.form_frame)

        ttk.Label(frame, text="电池容量(kWh):").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.battery = ttk.Entry(frame, font=self.normal_font)
        self.battery.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(frame, text="续航里程(km):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.range = ttk.Entry(frame, font=self.normal_font)
        self.range.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        return frame

    def toggle_model_fields(self):
        if self.model_type.get() == "combustion":
            self.electric_fields.grid_remove()
            self.combustion_fields.grid(row=3, column=0, columnspan=2, sticky='ew')
        else:
            self.combustion_fields.grid_remove()
            self.electric_fields.grid(row=3, column=0, columnspan=2, sticky='ew')

    # ========== 销售管理标签页 ==========
    def create_sale_tab(self):
        self.sale_frame = ttk.Frame(self.notebook)
        # 搜索框
        search_frame = ttk.Frame(self.sale_frame)
        ttk.Label(search_frame, text="搜索车辆:").pack(side='left', padx=5)
        self.sale_search = ttk.Entry(search_frame, font=self.normal_font)
        self.sale_search.pack(side='left', padx=5, fill='x', expand=True)
        self.sale_search_btn = ttk.Button(search_frame, text="搜索", style='Accent.TButton')
        self.sale_search_btn.pack(side='left', padx=5)
        search_frame.pack(fill='x', padx=10, pady=10)
        # 库存表格
        columns = ("inventory_id", "brand", "series", "model", "type", "batch_year", "status")
        self.inventory_tree = ttk.Treeview(self.sale_frame, columns=columns, show='headings')

        for col in columns:
            self.inventory_tree.heading(col, text=col.replace('_', ' ').title())
            self.inventory_tree.column(col, width=120, anchor='center')

        scrollbar = ttk.Scrollbar(self.sale_frame, orient="vertical", command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)

        self.inventory_tree.pack(side='top', fill='both', expand=True, padx=10, pady=(0, 10))
        scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=(0, 10))
        # 销售表单
        form_frame = ttk.LabelFrame(self.sale_frame, text="🛒 销售信息", padding=10)

        ttk.Label(form_frame, text="客户姓名:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.customer_name = ttk.Entry(form_frame, font=self.normal_font)
        self.customer_name.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(form_frame, text="联系电话:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.customer_phone = ttk.Entry(form_frame, font=self.normal_font)
        self.customer_phone.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        ttk.Label(form_frame, text="成交价格:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.sale_price = ttk.Entry(form_frame, font=self.normal_font)
        self.sale_price.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        btn_frame = ttk.Frame(form_frame)
        self.sale_complete_btn = ttk.Button(btn_frame, text="完成销售", style='Accent.TButton',command=self.controller.process_sale)
        self.sale_complete_btn.pack(side='left', padx=5)
        self.sale_clear_btn = ttk.Button(btn_frame, text="清空表单", command=self.clear_sale_form)
        self.sale_clear_btn.pack(side='left', padx=5)
        btn_frame.grid(row=3, columnspan=2, pady=10)

        form_frame.pack(fill='x', padx=10, pady=10)

        self.notebook.add(self.sale_frame, text="💰 销售管理")

    # ========== 查询管理标签页 ==========
    def create_query_tab(self):
        self.query_frame = ttk.Frame(self.notebook)
        columns = []  # 根据实际需要设置列
        self.query_tree = ttk.Treeview(self.query_frame, columns=columns, show='headings')
        # 查询类型选择
        query_frame = ttk.LabelFrame(self.query_frame, text="🔍 查询选项", padding=10)

        self.query_type = tk.StringVar(value="brand")
        ttk.Radiobutton(query_frame, text="品牌查询", variable=self.query_type,
                        value="brand", command=self.update_query_form).pack(side='left', padx=10)
        ttk.Radiobutton(query_frame, text="车型查询", variable=self.query_type,
                        value="model", command=self.update_query_form).pack(side='left', padx=10)
        ttk.Radiobutton(query_frame, text="销售查询", variable=self.query_type,
                        value="sale", command=self.update_query_form).pack(side='left', padx=10)
        ttk.Radiobutton(query_frame, text="销售汇总", variable=self.query_type,
                        value="sales_summary", command=self.update_query_form).pack(side='left', padx=10)
        ttk.Radiobutton(query_frame, text="库存查询", variable=self.query_type,
                        value="inventory", command=self.update_query_form).pack(side='left', padx=10)

        query_frame.pack(fill='x', padx=10, pady=10)
        # 动态查询表单
        self.query_form_frame = ttk.Frame(self.query_frame)
        self.query_form_frame.pack(fill='x', padx=10, pady=5)
        self.update_query_form()
        # 查询按钮
        btn_frame = ttk.Frame(self.query_frame)
        self.query_execute_btn = ttk.Button(btn_frame, text="执行查询", style='Accent.TButton',command=self.controller.execute_query)
        self.query_execute_btn.pack(side='left', padx=5)
        self.query_export_btn = ttk.Button(btn_frame, text="导出Excel",command=self.controller.export_to_excel)
        self.query_export_btn.pack(side='left', padx=5)
        self.query_reset_btn = ttk.Button(btn_frame, text="重置条件", command=self.reset_query_form)
        self.query_reset_btn.pack(side='left', padx=5)
        btn_frame.pack(pady=10)
        # 结果显示表格
        self.query_tree = ttk.Treeview(self.query_frame)

        scrollbar_y = ttk.Scrollbar(self.query_frame, orient="vertical", command=self.query_tree.yview)
        scrollbar_x = ttk.Scrollbar(self.query_frame, orient="horizontal", command=self.query_tree.xview)
        self.query_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.query_tree.pack(side='top', fill='both', expand=True, padx=(10, 0), pady=(0, 10))
        scrollbar_y.pack(side='right', fill='y', padx=(0, 10), pady=(0, 10))
        scrollbar_x.pack(side='bottom', fill='x', padx=(10, 0), pady=(0, 10))
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.query_frame, textvariable=self.status_var, relief='sunken')
        self.status_bar.pack(fill='x', padx=10, pady=(0, 10))

        self.notebook.add(self.query_frame, text="🔍 综合查询")

    def load_brand_data(self):
        """加载品牌数据到下拉框"""
        try:
            brands = self.controller.db.get_all_brands()
            brand_values = [f"{b['brand_id']}:{b['name']}" for b in brands]
            self.model_brand_combo['values'] = brand_values
            if brand_values:
                self.model_brand_combo.current(0)
                self.on_brand_selected()  # 初始化车系数据
        except Exception as e:
            messagebox.showerror("错误", f"加载品牌数据失败: {str(e)}")

    def on_brand_selected(self, event=None):
        """品牌选择变化时加载对应车系"""
        selected = self.model_brand_combo.get()
        if selected and ":" in selected:
            brand_id = int(selected.split(":")[0])
            try:
                series = self.controller.db.get_series_by_brand(brand_id)
                series_values = [f"{s['series_id']}:{s['name']}" for s in series]
                self.model_series_combo['values'] = series_values
                if series_values:
                    self.model_series_combo.current(0)
            except Exception as e:
                messagebox.showerror("错误", f"加载车系数据失败: {str(e)}")

    def update_query_form(self):
        # 清除旧表单
        for widget in self.query_form_frame.winfo_children():
            widget.destroy()

        query_type = self.query_type.get()

        if query_type == "brand":
            ttk.Label(self.query_form_frame, text="品牌名称:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
            self.brand_query = ttk.Entry(self.query_form_frame, font=self.normal_font)
            self.brand_query.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

            ttk.Label(self.query_form_frame, text="成立年份:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
            self.year_query = ttk.Combobox(self.query_form_frame, values=["全部", "2020", "2021", "2022", "2023"])
            self.year_query.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
            self.year_query.current(0)

        elif query_type == "model":
            # 品牌选择
            ttk.Label(self.query_form_frame, text="品牌:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
            self.model_brand_combo = ttk.Combobox(self.query_form_frame, state='readonly')
            self.model_brand_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
            # 车系选择
            ttk.Label(self.query_form_frame, text="车系:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
            self.model_series_combo = ttk.Combobox(self.query_form_frame, state='readonly')
            self.model_series_combo.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
            # 加载品牌数据
            self.load_brand_data()
            # 绑定品牌选择事件
            self.model_brand_combo.bind('<<ComboboxSelected>>', self.on_brand_selected)

        elif query_type == "sale":
            # 销售查询表单
            ttk.Label(self.query_form_frame, text="开始日期:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
            self.start_date = ttk.Entry(self.query_form_frame, font=self.normal_font)
            self.start_date.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

            ttk.Label(self.query_form_frame, text="结束日期:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
            self.end_date = ttk.Entry(self.query_form_frame, font=self.normal_font)
            self.end_date.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

            ttk.Label(self.query_form_frame, text="客户姓名:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
            self.customer_query = ttk.Entry(self.query_form_frame, font=self.normal_font)
            self.customer_query.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

            ttk.Label(self.query_form_frame, text="价格范围:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
            range_frame = ttk.Frame(self.query_form_frame)
            self.min_price = ttk.Entry(range_frame, font=self.normal_font, width=8)
            self.min_price.pack(side='left', padx=2)
            ttk.Label(range_frame, text="~").pack(side='left', padx=2)
            self.max_price = ttk.Entry(range_frame, font=self.normal_font, width=8)
            self.max_price.pack(side='left', padx=2)
            range_frame.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        elif query_type == "sales_summary":
            ttk.Label(self.query_form_frame, text="品牌筛选:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
            self.model_brand_combo = ttk.Combobox(self.query_form_frame, state='readonly')
            self.model_brand_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
            self.load_brand_data()

        elif query_type == "inventory":
            # 库存查询表单
            ttk.Label(self.query_form_frame, text="库存状态:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
            self.inv_status = ttk.Combobox(self.query_form_frame,
                                           values=["全部", "在库", "已售", "在途"],
                                           state='readonly')
            self.inv_status.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
            self.inv_status.current(0)

            ttk.Label(self.query_form_frame, text="生产年份:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
            self.inv_year = ttk.Combobox(self.query_form_frame,
                                         values=["全部", "2020", "2021", "2022", "2023"],
                                         state='readonly')
            self.inv_year.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
            self.inv_year.current(0)
        # 更新表格列（根据查询类型）
        self.update_tree_columns()

    def update_tree_columns(self):
        """动态设置表格列（中英文对照版）"""
        query_type = self.query_type.get()
        # 清空现有列和内容
        for col in self.query_tree["columns"]:
            self.query_tree.heading(col, text="")
            self.query_tree.column(col, width=0)
        self.query_tree.delete(*self.query_tree.get_children())

        columns_config = {
            "brand": {
                "columns": ("brand_id", "name", "headquarters", "founded_year"),
                "headers": ("Brand Id", "Name", "Headquarters", "Founded Year"),
                # "headers": ("品牌编号", "品牌名称", "总部地址", "成立年份"),
                "widths": (160, 300, 500, 200),
                "align": ['center'] * 4
            },
            "model": {
                "columns": ("model_id", "brand_name", "series_name", "name", "type", "production_year", "spec"),
                "headers": ("Model Id", "Brand Name", "Series Name", "Name", "Type", "Production Year", "Spec"),
                # "headers": ("车型编号", "品牌名称", "车系名称", "车型名称", "动力类型", "生产年份", "规格参数"),
                "widths": (80, 120, 120, 120, 80, 100, 100),
                "align": ['center'] * 7
            },
            "sale": {
                "columns": ("sale_id", "customer", "brand", "series", "model", "sale_date", "final_price"),
                "headers": ("Sale Id", "Customer", "Brand", "Series", "Model", "Sale Date", "Final Price"),
                # "headers": ("销售单号", "客户姓名", "品牌名称", "车系名称", "车型名称", "销售日期", "成交价格"),
                "widths": (80, 120, 120, 120, 120, 100, 100),
                "align": ['center', 'center', 'center', 'center', 'center', 'center', 'e']
            },
            "sales_summary": {
                "columns": ("brand", "series", "model", "total_sales", "total_revenue", "avg_price"),
                "headers": ("Brand", "Series", "Model", "Total Sales", "Total Revenue", "Avg Price"),
                # "headers": ("品牌名称", "车系名称", "车型名称", "销售总量", "总销售额", "平均售价"),
                "widths": (120, 120, 120, 100, 120, 120),
                "align": ['center', 'center', 'center', 'center', 'e', 'e']
            },
            "inventory": {
                "columns": ("inventory_id", "brand", "series", "model", "type", "batch_year", "status"),
                "headers": ("Inventory Id", "Brand", "Series", "Model", "Type", "Batch Year", "Status"),
                # "headers": ("库存编号", "品牌名称", "车系名称", "车型名称", "动力类型", "生产年份", "库存状态"),
                "widths": (60, 120, 120, 120, 100, 120, 120),
                "align": ['center'] * 7
            }
        }
        # 应用配置
        config = columns_config.get(query_type)
        if not config:
            return
        self.query_tree["columns"] = config["columns"]

        for idx, col in enumerate(config["columns"]):
            self.query_tree.heading(col, text=config["headers"][idx])
            self.query_tree.column(
                col,
                width=config["widths"][idx],
                stretch=True,
                anchor=config["align"][idx],
                minwidth=config["widths"][idx]  # 设置最小宽度防止挤压
            )

    def reset_query_form(self):
        """重置查询表单"""
        self.update_query_form()

    def display_query_results(self, results):
        """显示查询结果"""
        print(f"[DEBUG] 收到结果数据: {results}")
        if not results:
            self.query_tree.delete(*self.query_tree.get_children())
            self.status_var.set("查询完成，未找到匹配记录")
            return
        # 获取列名
        columns = list(results[0].keys())
        self.query_tree["columns"] = columns
        # 配置列标题
        for col in columns:
            self.query_tree.heading(col, text=col.replace('_', ' ').title())
            self.query_tree.column(col, width=120, anchor='center')
        # 清空现有数据
        self.query_tree.delete(*self.query_tree.get_children())
        # 添加新数据
        for row in results:
            self.query_tree.insert('', 'end', values=list(row.values()))
        # 更新状态栏
        self.status_var.set(f"查询完成，共找到 {len(results)} 条记录")

    # ========== 表单清理方法 ==========
    def clear_brand_form(self):
        """清空品牌表单"""
        self.brand_name.delete(0, 'end')
        self.brand_hq.delete(0, 'end')
        self.brand_year.delete(0, 'end')

    def clear_series_form(self):
        """清空车系表单"""
        self.series_name.delete(0, 'end')
        self.series_category.current(0)

    def clear_model_form(self):
        """清空车型表单"""
        self.model_name.delete(0, 'end')
        if self.model_type.get() == "combustion":
            self.engine_code.delete(0, 'end')
            self.horsepower.delete(0, 'end')
        else:
            self.battery.delete(0, 'end')
            self.range.delete(0, 'end')

    def clear_sale_form(self):
        """清空销售表单"""
        self.customer_name.delete(0, 'end')
        self.customer_phone.delete(0, 'end')
        self.sale_price.delete(0, 'end')

    # ========== 数据获取方法 ==========
    def get_selected_brand(self):
        """获取选中的品牌数据"""
        selection = self.brand_tree.selection()
        if selection:
            return self.brand_tree.item(selection)['values']
        return None

    def get_selected_series(self):
        """获取选中的车系数据"""
        selection = self.series_tree.selection()
        if selection:
            return self.series_tree.item(selection)['values']
        return None

    def get_selected_inventory(self):
        """获取选中的库存数据"""
        selection = self.inventory_tree.selection()
        if selection:
            return self.inventory_tree.item(selection)['values']
        return None

    # ========== 数据更新方法 ==========
    def update_brand_tree(self, brands):
        """更新品牌表格数据"""
        self.brand_tree.delete(*self.brand_tree.get_children())
        for brand in brands:
            self.brand_tree.insert('', 'end', values=(
                brand['brand_id'],
                brand['name'],
                brand['headquarters'],
                brand['founded_year']
            ))

    def update_series_tree(self, series):
        """更新车系表格数据"""
        self.series_tree.delete(*self.series_tree.get_children())
        for item in series:
            self.series_tree.insert('', 'end', values=(
                item['series_id'],
                item['brand_name'],
                item['name'],
                item['category']
            ))

    def update_model_tree(self, models):
        """更新车型表格数据"""
        self.model_tree.delete(*self.model_tree.get_children())
        for model in models:
            self.model_tree.insert('', 'end', values=(
                model['model_id'],
                model['brand_name'],
                model['series_name'],
                model['name'],
                model['type'],
                model['production_year'],
                model['spec']
            ))

    def update_inventory_tree(self, inventory):
        """更新库存表格数据"""
        self.inventory_tree.delete(*self.inventory_tree.get_children())
        for item in inventory:
            self.inventory_tree.insert('', 'end', values=(
                item['inventory_id'],
                item['brand'],
                item['series'],
                item['model'],
                item['type'],
                item['batch_year'],
                item['status']
            ))

    def update_series_brand_combo(self, brands):
        """更新车系页面的品牌下拉框"""
        self.series_brand_combo['values'] = [f"{b['brand_id']}:{b['name']}" for b in brands]
        if brands:
            self.series_brand_combo.current(0)

    def update_model_brand_combo(self, brands):
        """更新车型页面的品牌下拉框"""
        self.model_brand_combo['values'] = [f"{b['brand_id']}:{b['name']}" for b in brands]
        if brands:
            self.model_brand_combo.current(0)

    def update_series_combo(self, series):
        """更新车系列表"""
        self.model_series_combo['values'] = [f"{s['series_id']}:{s['name']}" for s in series]
        if series:
            self.model_series_combo.current(0)

    # def update_model_series_combo(self, event=None):
    #     """更新车型页面的车系下拉框数据"""
    #     selected_brand = self.model_brand_combo.get()
    #     if selected_brand and ":" in selected_brand:
    #         brand_id = int(selected_brand.split(":")[0])
    #         series = self.db.get_series_by_brand(brand_id)
    #         self.update_series_combo(series)
    def update_model_series_combo(self, series_list):
        """更新车系下拉框数据"""
        print(f"更新车系下拉框，共 {len(series_list)} 个车系")
        self.model_series_combo['values'] = [
            f"{s[0]}:{s[1]}" for s in series_list  # 格式化为"ID:名称"
        ]
        if series_list:
            self.model_series_combo.current(0)  # 默认选择第一个
