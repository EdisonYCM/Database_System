/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80041 (8.0.41)
 Source Host           : localhost:3306
 Source Schema         : vehicle_information

 Target Server Type    : MySQL
 Target Server Version : 80041 (8.0.41)
 File Encoding         : 65001

 Date: 19/05/2025 19:10:18
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for brand
-- ----------------------------
DROP TABLE IF EXISTS `brand`;
CREATE TABLE `brand`  (
  `brand_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'BMW',
  `headquarters` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `founded_year` year NULL DEFAULT NULL,
  PRIMARY KEY (`brand_id`) USING BTREE,
  UNIQUE INDEX `unique_brand_name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for combustionmodel
-- ----------------------------
DROP TABLE IF EXISTS `combustionmodel`;
CREATE TABLE `combustionmodel`  (
  `model_id` int NOT NULL,
  `engine_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `horsepower` int NULL DEFAULT NULL,
  `fuel_type` enum('Petrol','Diesel') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`model_id`) USING BTREE,
  CONSTRAINT `combustionmodel_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `model` (`model_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for configuration
-- ----------------------------
DROP TABLE IF EXISTS `configuration`;
CREATE TABLE `configuration`  (
  `config_id` int NOT NULL AUTO_INCREMENT,
  `model_id` int NULL DEFAULT NULL,
  `package_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `interior_type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `wheels` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`config_id`) USING BTREE,
  UNIQUE INDEX `model_id`(`model_id` ASC) USING BTREE,
  CONSTRAINT `configuration_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `model` (`model_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for customer
-- ----------------------------
DROP TABLE IF EXISTS `customer`;
CREATE TABLE `customer`  (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `contact` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `region_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`customer_id`) USING BTREE,
  INDEX `region_id`(`region_id` ASC) USING BTREE,
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for electricmodel
-- ----------------------------
DROP TABLE IF EXISTS `electricmodel`;
CREATE TABLE `electricmodel`  (
  `model_id` int NOT NULL,
  `battery_kWh` decimal(5, 1) NULL DEFAULT NULL,
  `range_km` int NULL DEFAULT NULL,
  PRIMARY KEY (`model_id`) USING BTREE,
  CONSTRAINT `electricmodel_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `model` (`model_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for inventory
-- ----------------------------
DROP TABLE IF EXISTS `inventory`;
CREATE TABLE `inventory`  (
  `inventory_id` int NOT NULL AUTO_INCREMENT,
  `model_id` int NULL DEFAULT NULL,
  `batch_id` int NULL DEFAULT NULL,
  `status` enum('In Stock','Sold','In Transit') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`inventory_id`) USING BTREE,
  INDEX `model_id`(`model_id` ASC) USING BTREE,
  INDEX `batch_id`(`batch_id` ASC) USING BTREE,
  CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `model` (`model_id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `inventory_ibfk_2` FOREIGN KEY (`batch_id`) REFERENCES `productionbatch` (`batch_id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for model
-- ----------------------------
DROP TABLE IF EXISTS `model`;
CREATE TABLE `model`  (
  `model_id` int NOT NULL AUTO_INCREMENT,
  `series_id` int NULL DEFAULT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `production_year` year NULL DEFAULT NULL,
  `drive_type` enum('RWD','AWD') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`model_id`) USING BTREE,
  INDEX `series_id`(`series_id` ASC) USING BTREE,
  CONSTRAINT `model_ibfk_1` FOREIGN KEY (`series_id`) REFERENCES `series` (`series_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2044 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for price
-- ----------------------------
DROP TABLE IF EXISTS `price`;
CREATE TABLE `price`  (
  `price_id` int NOT NULL AUTO_INCREMENT,
  `model_id` int NULL DEFAULT NULL,
  `region_id` int NULL DEFAULT NULL,
  `msrp` decimal(12, 2) NULL DEFAULT NULL,
  `dealer_price` decimal(12, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`price_id`) USING BTREE,
  UNIQUE INDEX `model_id`(`model_id` ASC, `region_id` ASC) USING BTREE,
  INDEX `region_id`(`region_id` ASC) USING BTREE,
  CONSTRAINT `price_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `model` (`model_id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `price_ibfk_2` FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2044 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for productionbatch
-- ----------------------------
DROP TABLE IF EXISTS `productionbatch`;
CREATE TABLE `productionbatch`  (
  `batch_id` int NOT NULL AUTO_INCREMENT,
  `model_id` int NULL DEFAULT NULL,
  `batch_year` year NULL DEFAULT NULL,
  `edition` enum('Standard','Limited') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`batch_id`) USING BTREE,
  INDEX `model_id`(`model_id` ASC) USING BTREE,
  CONSTRAINT `productionbatch_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `model` (`model_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for region
-- ----------------------------
DROP TABLE IF EXISTS `region`;
CREATE TABLE `region`  (
  `region_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `currency` char(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`region_id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sale
-- ----------------------------
DROP TABLE IF EXISTS `sale`;
CREATE TABLE `sale`  (
  `sale_id` int NOT NULL AUTO_INCREMENT,
  `inventory_id` int NULL DEFAULT NULL,
  `customer_id` int NULL DEFAULT NULL,
  `sale_date` date NULL DEFAULT (curdate()),
  `final_price` decimal(12, 2) NULL DEFAULT NULL,
  PRIMARY KEY (`sale_id`) USING BTREE,
  UNIQUE INDEX `inventory_id`(`inventory_id` ASC) USING BTREE,
  INDEX `customer_id`(`customer_id` ASC) USING BTREE,
  CONSTRAINT `sale_ibfk_1` FOREIGN KEY (`inventory_id`) REFERENCES `inventory` (`inventory_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sale_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `sale_chk_1` CHECK (`final_price` > 0)
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for series
-- ----------------------------
DROP TABLE IF EXISTS `series`;
CREATE TABLE `series`  (
  `series_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `category` enum('Sedan','SUV','Coupe') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `brand_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`series_id`) USING BTREE,
  INDEX `fk_series_brand`(`brand_id` ASC) USING BTREE,
  CONSTRAINT `fk_series_brand` FOREIGN KEY (`brand_id`) REFERENCES `brand` (`brand_id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 211 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- View structure for vw_sales_summary
-- ----------------------------
DROP VIEW IF EXISTS `vw_sales_summary`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `vw_sales_summary` AS select `b`.`name` AS `brand`,`s`.`name` AS `series`,`m`.`name` AS `model`,count(0) AS `total_sales`,sum(`sl`.`final_price`) AS `total_revenue`,avg(`sl`.`final_price`) AS `avg_price` from ((((`sale` `sl` join `inventory` `i` on((`sl`.`inventory_id` = `i`.`inventory_id`))) join `model` `m` on((`i`.`model_id` = `m`.`model_id`))) join `series` `s` on((`m`.`series_id` = `s`.`series_id`))) join `brand` `b` on((`s`.`brand_id` = `b`.`brand_id`))) group by `b`.`name`,`s`.`name`,`m`.`name`;

-- ----------------------------
-- Procedure structure for update_model_prices
-- ----------------------------
DROP PROCEDURE IF EXISTS `update_model_prices`;
delimiter ;;
CREATE PROCEDURE `update_model_prices`(IN p_model_id INT,
    IN p_increase_percent DECIMAL(5,2),
    IN p_max_increase DECIMAL(12,2))
BEGIN
    DECLARE current_price DECIMAL(12,2);
    DECLARE new_price DECIMAL(12,2);
    
    -- 开始事务
    START TRANSACTION;
    
    -- 获取当前价格
    SELECT msrp INTO current_price FROM Price WHERE model_id = p_model_id LIMIT 1;
    
    -- 计算新价格
    SET new_price = current_price * (1 + p_increase_percent/100);
    
    -- 检查最大涨幅限制
    IF (new_price - current_price) > p_max_increase THEN
        SET new_price = current_price + p_max_increase;
    END IF;
    
    -- 更新价格
    UPDATE Price 
    SET msrp = new_price, 
        dealer_price = new_price * 0.9  -- 经销商价格为MSRP的90%
    WHERE model_id = p_model_id;
    
    -- 提交事务
    COMMIT;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for update_model_prices_new
-- ----------------------------
DROP PROCEDURE IF EXISTS `update_model_prices_new`;
delimiter ;;
CREATE PROCEDURE `update_model_prices_new`(IN p_brand_id INT,
    IN p_series_id INT,
    IN p_price_increase DECIMAL(5,2),
    IN p_max_increase DECIMAL(12,2))
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE model_id_val INT;
    DECLARE current_price DECIMAL(12,2);
    DECLARE new_price DECIMAL(12,2);
    -- 声明游标，获取符合条件的车型
    DECLARE model_cursor CURSOR FOR 
        SELECT m.model_id, p.msrp 
        FROM Model m
        JOIN Price p ON m.model_id = p.model_id
        JOIN Series s ON m.series_id = s.series_id
        WHERE (p_brand_id IS NULL OR s.brand_id = p_brand_id)
          AND (p_series_id IS NULL OR m.series_id = p_series_id);
    -- 声明异常处理
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    -- 验证价格涨幅百分比
    IF p_price_increase < -100 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '价格降幅不能超过100%';
    END IF;
    -- 开始事务
    START TRANSACTION;
    -- 打开游标
    OPEN model_cursor;
    -- 循环处理每个车型
    model_loop: LOOP
        FETCH model_cursor INTO model_id_val, current_price;
        IF done THEN
            LEAVE model_loop;
        END IF;
        -- 计算新价格
        SET new_price = current_price * (1 + p_price_increase/100);
        -- 检查最大涨幅限制
        IF p_max_increase > 0 AND (new_price - current_price) > p_max_increase THEN
            SET new_price = current_price + p_max_increase;
        END IF;
        -- 确保价格不会变为负数
        IF new_price <= 0 THEN
            SET new_price = current_price * 0.1; -- 最低设置为原价的10%
        END IF;
        -- 更新车型价格
        UPDATE Price 
        SET msrp = new_price, 
            dealer_price = new_price * 0.9  -- 经销商价格为MSRP的90%
        WHERE model_id = model_id_val;
    END LOOP;
    -- 关闭游标
    CLOSE model_cursor;
    -- 提交事务
    COMMIT;
    -- 返回更新的车型数量
    SELECT ROW_COUNT() AS models_updated;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table sale
-- ----------------------------
DROP TRIGGER IF EXISTS `before_insert_sale`;
delimiter ;;
CREATE TRIGGER `before_insert_sale` BEFORE INSERT ON `sale` FOR EACH ROW BEGIN
    DECLARE inv_status VARCHAR(20);
    
    -- 检查库存状态
    SELECT status INTO inv_status FROM Inventory WHERE inventory_id = NEW.inventory_id;
    
    IF inv_status != 'In Stock' THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '只能销售在库状态的车辆';
    END IF;
    
    -- 检查价格是否合理
    IF NEW.final_price <= 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '销售价格必须大于0';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table series
-- ----------------------------
DROP TRIGGER IF EXISTS `before_insert_series`;
delimiter ;;
CREATE TRIGGER `before_insert_series` BEFORE INSERT ON `series` FOR EACH ROW BEGIN
    DECLARE brand_count INT;
    
    -- 检查品牌是否存在
    SELECT COUNT(*) INTO brand_count FROM Brand WHERE brand_id = NEW.brand_id;
    
    IF brand_count = 0 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = '添加失败：指定的品牌不存在';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table series
-- ----------------------------
DROP TRIGGER IF EXISTS `before_series_insert`;
delimiter ;;
CREATE TRIGGER `before_series_insert` BEFORE INSERT ON `series` FOR EACH ROW BEGIN
    DECLARE series_count INT;
    
    SELECT COUNT(*) INTO series_count
    FROM Series
    WHERE brand_id = NEW.brand_id AND name = NEW.name;
    
    IF series_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '同一品牌下不能有同名车系';
    END IF;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;

