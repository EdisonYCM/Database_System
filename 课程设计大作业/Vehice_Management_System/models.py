import pymysql
from datetime import datetime

class Database:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host='localhost',
                user='root',
                password='Yuchenmin1125',
                database='vehicle_information',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
            print("数据库连接成功")
        except pymysql.Error as e:
            print(f"数据库连接失败: {e}")
            raise

    def close(self):
        print("关闭数据库连接...")
        if self.connection:
            self.connection.close()
            print("数据库连接已关闭")

    # ========== 品牌操作 ==========
    def get_all_brands(self):
        print("执行获取所有品牌查询...")
        try:
            self.cursor.execute("SELECT * FROM Brand ORDER BY name")
            brands = self.cursor.fetchall()
            print(f"获取到 {len(brands)} 个品牌")
            return brands
        except pymysql.Error as e:
            print(f"获取品牌数据时出错: {e}")
            raise

    def add_brand(self, name, headquarters, founded_year):
        print(f"尝试添加品牌 - 名称: {name}, 总部: {headquarters}, 年份: {founded_year}")
        try:
            print("执行INSERT语句...")
            self.cursor.execute(
                "INSERT INTO Brand (name, headquarters, founded_year) VALUES (%s, %s, %s)", # 占位符，用于防止 SQL 注入攻击
                (name, headquarters, founded_year)
            )
            print("提交事务...")
            self.connection.commit()
            print(f"成功添加品牌: {name}")
            return True
        except pymysql.Error as e:
            print(f"添加品牌失败: {e}")
            self.connection.rollback() # 保证数据的一致性，回滚事务
            raise e

    def delete_brand(self, brand_id):
        print(f"尝试删除品牌 - ID: {brand_id}")
        try:
            print("开始事务...")
            self.cursor.execute("START TRANSACTION")

            # 删除关联数据
            print("删除关联的燃油车型...")
            self.cursor.execute("""
                DELETE cm FROM CombustionModel cm
                JOIN Model m ON cm.model_id = m.model_id
                JOIN Series s ON m.series_id = s.series_id
                WHERE s.brand_id = %s
            """, (brand_id,))
            print("删除关联的电动车型...")
            self.cursor.execute("""
                DELETE em FROM ElectricModel em
                JOIN Model m ON em.model_id = m.model_id
                JOIN Series s ON m.series_id = s.series_id
                WHERE s.brand_id = %s
            """, (brand_id,))
            print("删除关联的车型...")
            self.cursor.execute("""
                DELETE m FROM Model m
                JOIN Series s ON m.series_id = s.series_id
                WHERE s.brand_id = %s
            """, (brand_id,))
            print("删除关联的车系...")
            self.cursor.execute("DELETE FROM Series WHERE brand_id = %s", (brand_id,))
            print("删除品牌...")
            self.cursor.execute("DELETE FROM Brand WHERE brand_id = %s", (brand_id,))
            print("提交事务...")
            self.connection.commit()
            print("品牌删除成功")
            return True
        except pymysql.Error as e:
            print(f"删除品牌时出错: {e}")
            self.connection.rollback()
            raise e

    # ========== 车系操作 ==========
    def get_all_series(self):
        print("执行获取所有车系查询...")
        try:
            self.cursor.execute("""
                        SELECT s.series_id, b.name as brand_name, s.name, s.category 
                        FROM Series s JOIN Brand b ON s.brand_id = b.brand_id
                        ORDER BY b.name, s.name
                    """)
            series = self.cursor.fetchall()
            print(f"获取到 {len(series)} 个车系")
            return series
        except pymysql.Error as e:
            print(f"获取车系数据时出错: {e}")
            raise

    def get_series_by_brand(self, brand_id):
        """根据品牌ID获取车系列表"""
        print(f"查询品牌ID {brand_id} 的车系")
        try:
            self.cursor.execute("""
                    SELECT series_id, name 
                    FROM Series 
                    WHERE brand_id = %s 
                    ORDER BY name
                """, (brand_id,))
            result = self.cursor.fetchall()
            print(f"查询结果: {result}")  # 调试信息
            return result
        except pymysql.Error as e:
            print(f"查询车系列表出错: {e}")
            raise

    def add_series(self, brand_id, name, category):
        print(f"尝试添加车系 - 品牌ID: {brand_id}, 名称: {name}, 类别: {category}")
        try:
            self.cursor.execute(
                "INSERT INTO Series (brand_id, name, category) VALUES (%s, %s, %s)",
                (brand_id, name, category)
            )
            self.connection.commit()
            print("车系添加成功")
            return True
        except pymysql.Error as e:
            print(f"添加车系时出错: {e}")
            self.connection.rollback()
            raise e

    # ========== 车型操作 ==========
    def get_all_models(self):
        self.cursor.execute("""
            SELECT m.model_id, b.name as brand_name, s.name as series_name, m.name, 
                   CASE WHEN cm.model_id IS NOT NULL THEN '燃油' ELSE '电动' END as type,
                   m.production_year,
                   CASE 
                     WHEN cm.model_id IS NOT NULL THEN CONCAT(cm.engine_code, ' (', cm.horsepower, 'HP)')
                     ELSE CONCAT(em.battery_kWh, 'kWh (', em.range_km, 'km)')
                   END as spec
            FROM Model m
            JOIN Series s ON m.series_id = s.series_id
            JOIN Brand b ON s.brand_id = b.brand_id
            LEFT JOIN CombustionModel cm ON m.model_id = cm.model_id
            LEFT JOIN ElectricModel em ON m.model_id = em.model_id
            ORDER BY b.name, s.name, m.name
        """)
        return self.cursor.fetchall()

    def add_combustion_model(self, series_id, name, engine_code, horsepower, fuel_type):
        try:
            self.cursor.execute("START TRANSACTION")

            self.cursor.execute(
                "INSERT INTO Model (series_id, name, production_year) VALUES (%s, %s, %s)",
                (series_id, name, datetime.now().year)
            )
            model_id = self.cursor.lastrowid

            self.cursor.execute(
                "INSERT INTO CombustionModel VALUES (%s, %s, %s, %s)",
                (model_id, engine_code, horsepower, fuel_type)
            )

            self.connection.commit()
            return True
        except pymysql.Error as e:
            self.connection.rollback()
            raise e

    def add_electric_model(self, series_id, name, battery_kwh, range_km):
        try:
            self.cursor.execute("START TRANSACTION")

            self.cursor.execute(
                "INSERT INTO Model (series_id, name, production_year) VALUES (%s, %s, %s)",
                (series_id, name, datetime.now().year)
            )
            model_id = self.cursor.lastrowid

            self.cursor.execute(
                "INSERT INTO ElectricModel VALUES (%s, %s, %s)",
                (model_id, battery_kwh, range_km)
            )

            self.connection.commit()
            return True
        except pymysql.Error as e:
            self.connection.rollback()
            raise e

    # ========== 库存操作 ==========
    def get_inventory(self, status=None):
        query = """
            SELECT i.inventory_id, b.name as brand, s.name as series, m.name as model, 
                   CASE WHEN cm.model_id IS NOT NULL THEN '燃油' ELSE '电动' END as type,
                   pb.batch_year, i.status
            FROM Inventory i
            JOIN Model m ON i.model_id = m.model_id
            JOIN Series s ON m.series_id = s.series_id
            JOIN Brand b ON s.brand_id = b.brand_id
            LEFT JOIN CombustionModel cm ON m.model_id = cm.model_id
            LEFT JOIN ElectricModel em ON m.model_id = em.model_id
            LEFT JOIN ProductionBatch pb ON i.batch_id = pb.batch_id
        """
        params = ()
        if status:
            query += " WHERE i.status = %s"
            params = (status,)
        query += " ORDER BY b.name, s.name, m.name"

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    # ========== 销售操作 ==========
    def add_sale(self, inventory_id, customer_name, customer_phone, final_price):
        try:
            self.cursor.execute("START TRANSACTION")
            # 1. 先创建销售记录（不立即更新库存）
            self.cursor.execute(
                """INSERT INTO Customer (name, contact)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE contact=VALUES(contact)""",
                (customer_name, customer_phone)
            )
            customer_id = self.cursor.lastrowid
            # 2. 直接插入销售记录
            self.cursor.execute(
                """INSERT INTO Sale 
                (inventory_id, customer_id, final_price, sale_date)
                VALUES (%s, %s, %s, CURDATE())""",
                (inventory_id, customer_id, final_price)
            )
            # 3. 最后更新库存状态（不检查原状态）
            self.cursor.execute(
                """UPDATE Inventory 
                SET status='Sold' 
                WHERE inventory_id=%s""",  # 移除了状态检查
                (inventory_id,)
            )
            self.connection.commit()
            return True
        except pymysql.Error as e:
            self.connection.rollback()
            raise Exception(f"数据库错误({e.args[0]}): {e.args[1]}")
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"系统异常: {str(e)}")

    # ========== 查询操作 ==========
    def search_models(self, brand_id=None, series_id=None, model_type=None):
        query = """
            SELECT m.model_id, b.name as brand_name, s.name as series_name, m.name, 
                   CASE WHEN cm.model_id IS NOT NULL THEN '燃油' ELSE '电动' END as type,
                   m.production_year,
                   CASE 
                     WHEN cm.model_id IS NOT NULL THEN CONCAT(cm.engine_code, ' (', cm.horsepower, 'HP)')
                     ELSE CONCAT(em.battery_kWh, 'kWh (', em.range_km, 'km)')
                   END as spec
            FROM Model m
            JOIN Series s ON m.series_id = s.series_id
            JOIN Brand b ON s.brand_id = b.brand_id
            LEFT JOIN CombustionModel cm ON m.model_id = cm.model_id
            LEFT JOIN ElectricModel em ON m.model_id = em.model_id
        """
        conditions = []
        params = []

        if brand_id:
            conditions.append("b.brand_id = %s")
            params.append(brand_id)
        if series_id:
            conditions.append("s.series_id = %s")
            params.append(series_id)
        if model_type:
            if model_type == "燃油":
                conditions.append("cm.model_id IS NOT NULL")
            else:
                conditions.append("em.model_id IS NOT NULL")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY b.name, s.name, m.name"
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_sales_summary(self, brand_name=None):
        # self.cursor.execute("SELECT * FROM vw_sales_summary ORDER BY total_revenue DESC")
        # return self.cursor.fetchall()
        """获取销售汇总视图数据"""
        print(f"[DEBUG] 调用get_sales_summary，brand_name={brand_name}")  # 调试
        sql = "SELECT * FROM vw_sales_summary"
        params = []
        if brand_name:
            sql += " WHERE brand = %s"
            params.append(brand_name)
        sql += " ORDER BY total_revenue DESC"
        print(f"[DEBUG] 执行SQL: {sql}, 参数: {params}")  # 调试
        return self.execute_query(sql, params)

    def update_model_prices(self, brand_id=None, series_id=None, price_increase=0, max_increase=0):
        try:
            self.cursor.callproc(
                "update_model_prices_new",
                (brand_id, series_id, price_increase, max_increase)
            )
            result = self.cursor.fetchone()
            self.connection.commit()
            return result['models_updated'] if result else 0
        except pymysql.Error as e:
            self.connection.rollback()
            raise e

    def execute_query(self, query, params=None):
        """执行自定义SQL查询"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except pymysql.Error as e:
            self.connection.rollback()
            raise e

    def get_brands_for_combobox(self):
        """获取品牌数据用于下拉框"""
        self.cursor.execute("SELECT brand_id, name FROM Brand ORDER BY name")
        return [f"{row['brand_id']}:{row['name']}" for row in self.cursor.fetchall()]

    def get_series_by_brand(self, brand_id):
        """根据品牌ID获取车系列表"""
        self.cursor.execute("SELECT series_id, name FROM Series WHERE brand_id=%s", (brand_id,))
        return self.cursor.fetchall()