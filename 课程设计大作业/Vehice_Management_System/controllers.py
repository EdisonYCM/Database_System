import tkinter as tk
import traceback
from tkinter import ttk
import tkinter.messagebox as messagebox
from datetime import datetime

import pymysql


class MainController:
    def __init__(self, view, db):
        print("初始化MainController...")
        self.view = view
        self.db = db    # 保存视图和模型引用
        self.root = view.root  # 从视图获取根窗口
        # self.view.controller = self  # 双向引用
        self.view.set_controller(self)  # 设置控制器
        # 延迟执行需要访问UI组件的操作
        self.root.after(100, self.finalize_setup)

    def finalize_setup(self):
        """确保界面完全创建后再设置事件处理器"""
        if not hasattr(self.view, 'model_brand_combo'):
            print("警告: model_brand_combo 尚未创建，重试...")
            self.root.after(100, self.finalize_setup)
            return

        print("界面已完全加载，设置事件处理器...")
        self.setup_event_handlers()
        self.load_initial_data()

    def setup_event_handlers(self):
        print("设置事件处理器...")
        if hasattr(self.view, 'model_brand_combo'):  # 检查控件是否存在
            self.view.model_brand_combo.bind('<<ComboboxSelected>>', self.on_model_brand_select)
        # 品牌管理事件
        self.view.brand_tree.bind('<<TreeviewSelect>>', self.on_brand_select)
        self.view.brand_add_btn.configure(command=self.add_brand)
        self.view.brand_clear_btn.configure(command=self.view.clear_brand_form)
        self.view.brand_delete_btn.configure(command=self.delete_brand)
        # 车系管理事件
        self.view.series_brand_combo.bind('<<ComboboxSelected>>', self.on_series_brand_select)
        # self.view.model_series_combo.bind('<<ComboboxSelected>>', self.on_series_brand_select)
        # self.view.model_series_combo.bind('<<ComboboxSelected>>', self.load_series_for_selected_brand)
        self.view.series_add_btn.configure(command=self.add_series)
        self.view.series_clear_btn.configure(command=self.view.clear_series_form)
        self.view.series_price_btn.configure(command=self.show_price_update_dialog)
        # 车型管理事件
        # self.view.model_brand_combo.bind('<<ComboboxSelected>>', self.on_model_brand_select)
        self.view.model_brand_combo.bind('<<ComboboxSelected>>', lambda e: self.load_series_for_model_tab())
        self.view.model_series_combo.bind('<<ComboboxSelected>>', self.on_series_brand_select)
        self.view.model_add_btn.configure(command=self.add_model)
        self.view.model_clear_btn.configure(command=self.view.clear_model_form)
        # 销售管理事件
        self.view.sale_search_btn.configure(command=self.search_inventory)
        self.view.sale_complete_btn.configure(command=self.process_sale)
        self.view.sale_clear_btn.configure(command=self.view.clear_sale_form)
        # 查询管理事件
        self.view.query_execute_btn.configure(command=self.execute_query)
        self.view.query_export_btn.configure(command=self.export_to_excel)
        self.view.query_reset_btn.configure(command=self.reset_query_form)
        # 绑定查询类型切换事件
        self.view.query_type.trace('w', self.on_query_type_changed)
        print("所有事件处理器设置完成")
        print("品牌下拉框存在:", hasattr(self.view, 'model_brand_combo'))
        print("车系下拉框存在:", hasattr(self.view, 'model_series_combo'))
        print("品牌下拉框选项:", self.view.model_brand_combo['values'])
        print("车系下拉框选项:", self.view.model_series_combo['values'])
        # 测试手动触发
        self.view.model_brand_combo.event_generate('<<ComboboxSelected>>')

    def on_query_type_changed(self, *args):
        """当查询类型变化时重新加载表单"""
        self.view.update_query_form()

    def load_series_for_model_tab(self):
        """专用车系加载方法"""
        try:
            selected = self.view.model_brand_combo.get()
            if ":" in selected:
                brand_id = int(selected.split(":")[0])
                series = self.db.get_series_by_brand(brand_id)

                # 双重更新保障
                self.view.model_series_combo['values'] = [
                    f"{s['series_id']}:{s['name']}" for s in series
                ]

                # 调试输出
                print(f"已加载 {len(series)} 个车系选项")
                print("当前车系下拉框状态:", self.view.model_series_combo['values'])

                if series:
                    self.view.model_series_combo.current(0)
        except Exception as e:
            print(f"车系加载错误: {str(e)}")
    def load_initial_data(self):
        print("加载初始数据...")
        try:
            # 加载品牌数据
            print("尝试加载品牌数据...")
            brands = self.db.get_all_brands()
            print(f"获取到 {len(brands)} 个品牌")
            self.view.update_brand_tree(brands)
            self.view.update_series_brand_combo(brands)
            self.view.update_model_brand_combo(brands)
            # 加载车系数据
            print("尝试加载车系数据...")
            series = self.db.get_all_series()
            print(f"获取到 {len(series)} 个车系")
            self.view.update_series_tree(series)
            # 加载车型数据
            print("尝试加载车型数据...")
            models = self.db.get_all_models()
            print(f"获取到 {len(models)} 个车型")
            self.view.update_model_tree(models)
            # 加载库存数据
            print("尝试加载库存数据...")
            inventory = self.db.get_inventory(status='In Stock')
            print(f"获取到 {len(inventory)} 个库存记录")
            self.view.update_inventory_tree(inventory)
            print("初始数据加载完成")
        except Exception as e:
            print(f"加载数据时发生错误: {str(e)}")
            self.show_message("错误", f"加载数据失败: {str(e)}", is_error=True)

    # ========== 通用方法 ==========
    def show_message(self, title, message, is_error=False, ask=False):
        print(f"显示消息框 - 标题: {title}, 消息: {message}, 是否错误: {is_error}, 是否询问: {ask}")
        if ask:
            return messagebox.askyesno(title, message)
        elif is_error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)

    # ========== 品牌管理方法 ==========
    def on_brand_select(self, event):
        print("品牌选择事件触发")
        selected = self.view.get_selected_brand()
        if selected:
            print(f"选择了品牌: ID={selected[0]}, 名称={selected[1]}")
            self.view.brand_name.delete(0, 'end')
            self.view.brand_name.insert(0, selected[1])
            self.view.brand_hq.delete(0, 'end')
            self.view.brand_hq.insert(0, selected[2])
            self.view.brand_year.delete(0, 'end')
            self.view.brand_year.insert(0, selected[3])

    def add_brand(self):
        print("尝试添加品牌...")
        name = self.view.brand_name.get()
        hq = self.view.brand_hq.get()
        year = self.view.brand_year.get()
        print(f"获取的表单数据 - 名称: {name}, 总部: {hq}, 年份: {year}")
        if not name:
            self.show_message("警告", "品牌名称不能为空！")
            return
        try:
            print("调用数据库添加品牌...")
            if self.db.add_brand(name, hq, year):
                self.show_message("成功", "品牌添加成功！")
                self.view.clear_brand_form()
                self.load_initial_data()
        except Exception as e:
            self.show_message("错误", f"添加品牌失败: {str(e)}", is_error=True)

    def delete_brand(self):
        print("尝试删除品牌...")
        selected = self.view.get_selected_brand()
        if not selected:
            self.show_message("警告", "请先选择要删除的品牌！")
            return
        brand_id = selected[0]
        brand_name = selected[1]
        if not self.show_message("确认", f"确定要删除品牌 {brand_name} 及其所有车型吗？", ask=True):
            print("用户取消了删除操作")
            return
        try:
            print("调用数据库删除品牌...")
            if self.db.delete_brand(brand_id):
                self.show_message("成功", "品牌删除成功！")
                self.load_initial_data()
        except Exception as e:
            self.show_message("错误", f"删除品牌失败: {str(e)}", is_error=True)

    # ========== 车系管理方法 ==========
    def on_series_brand_select(self, event):
        selected_brand = self.view.series_brand_combo.get()
        if selected_brand and ":" in selected_brand:
            brand_id = int(selected_brand.split(":")[0])
            series = self.db.get_series_by_brand(brand_id)
            self.view.update_series_combo(series)

    def load_series_for_selected_brand(self, event=None):
        """车型管理页专用车系加载"""
        print("\n[DEBUG] 触发品牌选择事件")
        # 获取选中品牌（格式："6:brand_test1"）
        selected = self.view.model_brand_combo.get()
        if not selected or ":" not in selected:
            return
        brand_id = int(selected.split(":")[0])
        print(f"[DEBUG] 解析出品牌ID: {brand_id}")
        try:
            # 从数据库获取车系
            series = self.db.get_series_by_brand(brand_id)
            print(f"[DEBUG] 查询到车系数据: {series}")
            # 更新下拉框（格式："ID:名称"）
            self.view.model_series_combo['values'] = [
                f"{s['series_id']}:{s['name']}" for s in series
            ]
            print(f"[DEBUG] 已更新车系下拉框，选项数: {len(series)}")
        except Exception as e:
            print(f"[ERROR] 加载车系失败: {e}")

    def add_series(self):
        selected_brand = self.view.series_brand_combo.get()
        name = self.view.series_name.get()
        category = self.view.series_category.get()
        if not selected_brand or ":" not in selected_brand:
            self.show_message("警告", "请选择所属品牌！")
            return
        if not name:
            self.show_message("警告", "车系名称不能为空！")
            return
        brand_id = int(selected_brand.split(":")[0])
        try:
            if self.db.add_series(brand_id, name, category):
                self.show_message("成功", "车系添加成功！")
                self.view.clear_series_form()
                self.load_initial_data()
        except Exception as e:
            self.show_message("错误", f"添加车系失败: {str(e)}", is_error=True)

    def show_price_update_dialog(self):
        dialog = tk.Toplevel(self.view.root)
        dialog.title("批量更新车型价格")
        dialog.geometry("400x300")
        # 品牌选择
        ttk.Label(dialog, text="品牌:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        brand_combo = ttk.Combobox(dialog, state='readonly')
        brand_combo.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        # 车系选择
        ttk.Label(dialog, text="车系:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        series_combo = ttk.Combobox(dialog, state='readonly')
        series_combo.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        # 价格涨幅
        ttk.Label(dialog, text="价格涨幅(%):").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        price_increase = ttk.Entry(dialog)
        price_increase.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        # 最大涨幅限制
        ttk.Label(dialog, text="最大涨幅金额:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        max_increase = ttk.Entry(dialog)
        max_increase.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        # 加载品牌数据
        brands = self.db.get_all_brands()
        brand_combo['values'] = ["全部品牌"] + [f"{b['brand_id']}:{b['name']}" for b in brands]
        brand_combo.current(0)

        def update_series_combo(event=None):
            selected = brand_combo.get()
            if selected == "全部品牌":
                series_combo['values'] = ["全部车系"]
            else:
                brand_id = int(selected.split(":")[0])
                series = self.db.get_series_by_brand(brand_id)
                series_combo['values'] = ["全部车系"] + [f"{s['series_id']}:{s['name']}" for s in series]
            series_combo.current(0)

        brand_combo.bind('<<ComboboxSelected>>', update_series_combo)

        def execute_update():
            try:
                # 解析品牌ID
                brand_id = None
                selected_brand = brand_combo.get()
                if selected_brand != "全部品牌":
                    brand_id = int(selected_brand.split(":")[0])
                # 解析车系ID
                series_id = None
                selected_series = series_combo.get()
                if selected_series != "全部车系":
                    series_id = int(selected_series.split(":")[0])
                # 获取价格参数
                increase = float(price_increase.get())
                max_inc = float(max_increase.get()) if max_increase.get() else 0
                # 调用更新
                # updated = self.db.update_model_prices(brand_id, series_id, increase, max_inc)
                # self.show_message("成功", f"成功更新了 {updated} 个车型的价格！")
                self.db.update_model_prices(brand_id, series_id, increase, max_inc)
                self.show_message("成功", f"成功更新了车型的价格！")
                dialog.destroy()
                self.load_initial_data()
            except ValueError:
                self.show_message("错误", "请输入有效的数字！", is_error=True)
            except Exception as e:
                self.show_message("错误", f"价格更新失败: {str(e)}", is_error=True)

        # 按钮框架
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="执行更新", command=execute_update, style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side='left', padx=5)

    # ========== 车型管理方法 ==========
    def on_model_brand_select(self, event):
        """当品牌选择变化时加载对应车系"""
        print("品牌选择变化事件触发")
        self.view.on_model_brand_selected(event)

    def add_model(self):
        selected_series = self.view.model_series_combo.get()
        name = self.view.model_name.get()
        model_type = self.view.model_type.get()

        if not selected_series or ":" not in selected_series:
            self.show_message("警告", "请选择所属车系！")
            return
        if not name:
            self.show_message("警告", "车型名称不能为空！")
            return

        series_id = int(selected_series.split(":")[0])

        try:
            if model_type == "combustion":
                engine_code = self.view.engine_code.get()
                horsepower = self.view.horsepower.get()
                fuel_type = self.view.fuel_type.get()
                if not all([engine_code, horsepower]):
                    self.show_message("警告", "请填写完整的燃油车型信息！")
                    return
                if self.db.add_combustion_model(series_id, name, engine_code, horsepower, fuel_type):
                    self.show_message("成功", "燃油车型添加成功！")
                    self.view.clear_model_form()
                    self.load_initial_data()
            else:
                battery = self.view.battery.get()
                range_km = self.view.range.get()
                if not all([battery, range_km]):
                    self.show_message("警告", "请填写完整的电动车型信息！")
                    return
                if self.db.add_electric_model(series_id, name, battery, range_km):
                    self.show_message("成功", "电动车型添加成功！")
                    self.view.clear_model_form()
                    self.load_initial_data()
        except Exception as e:
            self.show_message("错误", f"添加车型失败: {str(e)}", is_error=True)

    # ========== 销售管理方法 ==========
    def search_inventory(self):
        keyword = self.view.sale_search.get()
        try:
            inventory = self.db.get_inventory()
            if keyword:
                inventory = [item for item in inventory
                             if keyword.lower() in item['brand'].lower()
                             or keyword.lower() in item['series'].lower()
                             or keyword.lower() in item['model'].lower()
                             or keyword in str(item['batch_year'])]
            self.view.update_inventory_tree(inventory)
        except Exception as e:
            self.show_message("错误", f"搜索失败: {str(e)}", is_error=True)

    def process_sale(self):
        try:
            selected = self.view.get_selected_inventory()
            if not selected:
                raise ValueError("请先选择要销售的车辆")
            # 获取界面输入
            inventory_id = selected[0]
            customer_name = self.view.customer_name.get().strip()
            customer_phone = self.view.customer_phone.get().strip()
            # price = self.view.sale_price.get()
            price_str = self.view.sale_price.get()
            # 验证必填字段
            if not all([customer_name, customer_phone, price_str]):
                raise ValueError("请填写完整的客户信息和销售价格")
            # 转换价格格式
            try:
                final_price = float(price_str)
                if final_price <= 0:
                    raise ValueError("价格必须大于0")
            except ValueError:
                raise ValueError("请输入有效的价格数字")
            # 执行销售
            if not self.db.add_sale(inventory_id, customer_name, customer_phone, final_price):
                raise Exception("销售记录创建失败")
            # 成功处理
            self.show_message("成功", f"车辆 {inventory_id} 销售成功！")
            self.view.clear_sale_form()
            self.load_initial_data()
        except ValueError as e:
            self.show_message("输入错误", str(e), is_error=True)
        except pymysql.err.OperationalError as e:
            self.show_message("销售失败", f"{e.args[1]} (代码:{e.args[0]})", is_error=True)
        except Exception as e:
            error_msg = f"销售处理失败: {str(e)}"
            print(f"[ERROR] {error_msg}\n{traceback.format_exc()}")
            self.show_message("系统错误", error_msg, is_error=True)

    # ========== 查询管理方法 ==========
    def reset_query_form(self):
        self.view.update_query_form()

    def setup_event_handlers(self):
        # 绑定查询类型切换事件
        self.view.query_type.trace('w', self.on_query_type_changed)

    def on_query_type_changed(self, *args):
        """当查询类型变化时重新加载表单"""
        self.view.update_query_form()

    def execute_query(self):
        query_type = self.view.query_type.get()
        print(f"执行查询，类型: {query_type}")  # 调试输出
        try:
            if query_type == "brand":
                # 获取品牌查询参数
                brand_name = self.view.brand_query.get()
                year = self.view.year_query.get()
                # 构建查询条件
                conditions = []
                params = []
                if brand_name:
                    conditions.append("name LIKE %s")
                    params.append(f"%{brand_name}%")
                if year and year != "全部":
                    conditions.append("founded_year = %s")
                    params.append(year)
                # 构建完整查询
                query = "SELECT * FROM brand"
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                query += " ORDER BY name"
                print(f"执行品牌查询: {query}")  # 调试输出
                results = self.db.execute_query(query, params)
                self.view.display_query_results(results)
            elif query_type == "model":
                # 获取查询参数
                brand = self.view.model_brand_combo.get()
                series = self.view.model_series_combo.get()
                # 解析ID
                brand_id = int(brand.split(":")[0]) if brand and ":" in brand else None
                series_id = int(series.split(":")[0]) if series and ":" in series else None
                # 执行查询
                try:
                    results = self.db.search_models(brand_id, series_id)
                    self.view.display_query_results(results)
                except Exception as e:
                    self.show_message("错误", f"查询失败: {str(e)}", is_error=True)
            elif query_type == "sale":
                self.query_sales()
            elif query_type == "inventory":
                self.query_inventory()
            elif query_type == "sales_summary":
                # 获取选择的品牌
                selected_brand = self.view.model_brand_combo.get()
                brand_name = None
                if selected_brand and ":" in selected_brand:
                    brand_name = selected_brand.split(":")[1]  # 获取品牌名称部分
                # 执行查询
                try:
                    results = self.db.get_sales_summary(brand_name)
                    self.view.display_query_results(results)
                except Exception as e:
                    print(f"销售汇总查询错误: {str(e)}")  # 打印详细错误
                    self.show_message("错误", f"查询失败: {str(e)}", is_error=True)
            # 更新状态栏
            count = len(self.view.query_tree.get_children())
            self.view.status_var.set(f"查询完成，共找到 {count} 条记录")
        except Exception as e:
            self.show_message("错误", f"查询失败: {str(e)}", is_error=True)

    def query_brands(self):
        try:
            # 确保控件存在
            if not hasattr(self.view, 'brand_combo'):
                raise ValueError("品牌选择控件未初始化")
            # 获取查询条件
            brand_name = self.view.brand_name_entry.get()  # 假设有品牌名称输入框
            if not brand_name:
                self.show_message("提示", "请输入品牌名称", is_error=False)
                return
            # 执行查询
            results = self.db.query_brands_by_name(brand_name)
            # 更新显示
            self.view.update_query_results(results)
        except Exception as e:
            self.show_message("错误", f"查询失败: {str(e)}", is_error=True)
            print(f"DEBUG - 错误详情: {traceback.format_exc()}")  # 打印完整错误栈

    def query_models(self):
        brand = self.view.model_brand_combo.get()
        series = self.view.model_series_combo.get()
        model_type = self.view.model_type_combo.get()

        brand_id = int(brand.split(":")[0]) if brand and brand != "全部" else None
        series_id = int(series.split(":")[0]) if series and series != "全部" else None
        mtype = model_type if model_type != "全部" else None

        results = self.db.search_models(brand_id, series_id, mtype)
        self.view.display_query_results(results)

    def query_sales(self):
        start_date = self.view.start_date.get()
        end_date = self.view.end_date.get()
        customer = self.view.customer_query.get()
        min_price = self.view.min_price.get()
        max_price = self.view.max_price.get()
        conditions = []
        params = []
        if start_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                conditions.append("s.sale_date >= %s")
                params.append(start_date)
            except ValueError:
                self.show_message("错误", "开始日期格式错误，请使用 YYYY-MM-DD 格式！", is_error=True)
                return
        if end_date:
            try:
                datetime.strptime(end_date, '%Y-%m-%d')
                conditions.append("s.sale_date <= %s")
                params.append(end_date)
            except ValueError:
                self.show_message("错误", "结束日期格式错误，请使用 YYYY-MM-DD 格式！", is_error=True)
                return
        if customer:
            conditions.append("c.name LIKE %s")
            params.append(f"%{customer}%")
        if min_price and max_price:
            try:
                min_val = float(min_price)
                max_val = float(max_price)
                if min_val > max_val:
                    self.show_message("错误", "最低价格不能大于最高价格！", is_error=True)
                    return
                conditions.append("s.final_price BETWEEN %s AND %s")
                params.extend([min_val, max_val])
            except ValueError:
                self.show_message("错误", "请输入有效的价格数字！", is_error=True)
                return
        elif min_price:
            try:
                conditions.append("s.final_price >= %s")
                params.append(float(min_price))
            except ValueError:
                self.show_message("错误", "请输入有效的价格数字！", is_error=True)
                return
        elif max_price:
            try:
                conditions.append("s.final_price <= %s")
                params.append(float(max_price))
            except ValueError:
                self.show_message("错误", "请输入有效的价格数字！", is_error=True)
                return

        where = "WHERE " + " AND ".join(conditions) if conditions else ""
        query = f"""
            SELECT s.sale_id, c.name as customer, i.brand, i.series, i.model, 
                   s.sale_date, s.final_price
            FROM Sale s
            JOIN Customer c ON s.customer_id = c.customer_id
            JOIN (
                SELECT i.inventory_id, b.name AS brand, s.name AS series, m.name AS model
                FROM Inventory i
                JOIN Model m ON i.model_id = m.model_id
                JOIN Series s ON m.series_id = s.series_id
                JOIN Brand b ON s.brand_id = b.brand_id
            ) i ON s.inventory_id = i.inventory_id
            {where}
            ORDER BY s.sale_date
        """

        results = self.db.execute_query(query, params)
        self.view.display_query_results(results)

    def query_sales_summary(self):
        """处理销售汇总视图查询"""
        try:
            selected_brand = self.view.model_brand_combo.get()
            brand_name = selected_brand.split(":")[1] if selected_brand and ":" in selected_brand else None
            print(f"[DEBUG] 查询销售汇总，品牌: {brand_name}")  # 调试用
            # 执行查询
            results = self.db.get_sales_summary(brand_name)
            print(f"[DEBUG] 查询结果: {len(results)}条")  # 调试用
            if not results:
                self.show_message("提示", "没有找到匹配的销售汇总数据")
                self.view.display_query_results([])
                return
            # 显示结果
            self.view.display_query_results(results)
            self.view.status_var.set(f"查询完成，共找到 {len(results)} 条记录")
        except Exception as e:
            self.show_message("错误", f"查询失败: {str(e)}", is_error=True)
            print(f"完整错误: {traceback.format_exc()}")

    def query_inventory(self):
        status = self.view.inv_status.get()
        year = self.view.inv_year.get()
        status_map = {
            "在库": "In Stock",
            "已售": "Sold",
            "在途": "In Transit"
        }
        status_val = status_map.get(status) if status != "全部" else None
        year_val = year if year != "全部" else None

        results = self.db.get_inventory(status_val)
        if year_val:
            results = [item for item in results if str(item['batch_year']) == year_val]

        self.view.display_query_results(results)

    def export_to_excel(self):
        try:
            import openpyxl
            from openpyxl import Workbook
            # 获取当前查询结果
            items = []
            for child in self.view.query_tree.get_children():
                items.append(self.view.query_tree.item(child)['values'])

            if not items:
                self.show_message("警告", "没有数据可导出！")
                return
            # 创建Excel文件
            wb = Workbook()
            ws = wb.active
            # 添加表头
            columns = [self.view.query_tree.heading(col)['text'] for col in self.view.query_tree['columns']]
            ws.append(columns)
            # 添加数据
            for item in items:
                ws.append(item)
            # 保存文件
            file_path = "query_results.xlsx"
            wb.save(file_path)
            self.show_message("成功", f"查询结果已导出到 {file_path}")
        except ImportError:
            self.show_message("错误", "未安装 openpyxl 库，请先安装！", is_error=True)
        except Exception as e:
            self.show_message("错误", f"导出失败: {str(e)}", is_error=True)