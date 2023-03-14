USE 你的库名称;

/* DIRECTIONS():查看库中存储过程
	   */
DELIMITER $$
DROP PROCEDURE IF EXISTS Directions$$
CREATE PROCEDURE Directions()
BEGIN
	SELECT "存储过程命名:" AS "作用:",
		"某张表每日最低价格" AS DialyPrice_Min,
		"对某张表去重" AS DupRemove,
		"对数据库内所有表去重" AS DupRemove_All,
        "对数据库内所有表添加自增主键id" AS AddPrkey_ALL,
        "新建表" AS CreateNewTable,
		"向表内插入数据" AS InsertData,
        "查询数据库总数据数" AS Info_Count;
END$$
DELIMITER ;

CALL Directions();

/* DialyPrice_Min(skin_name):查找皮肤skin_name每天最低价格
	完成 */
DELIMITER $$
DROP PROCEDURE IF EXISTS DialyPrice_Min$$
CREATE PROCEDURE DialyPrice_Min(IN s_name VARCHAR(20))
BEGIN
	SET @n := CONCAT("SELECT skin_name, skin_float_type, MIN(prices) AS prices, date ", 
    "FROM ",
    s_name,
    " GROUP BY skin_name, skin_float_type, date ORDER BY date DESC");
	PREPARE sl FROM @n;
    EXECUTE sl;
    DEALLOCATE PREPARE sl;
END$$
DELIMITER ;


/* DupRemove(tname):对表tname去重
	完成 */
DELIMITER $$
DROP PROCEDURE IF EXISTS DupRemove$$
CREATE PROCEDURE DupRemove(IN tname VARCHAR(20))
BEGIN
	SET @a := CONCAT("DELETE FROM ",
        tname,
        " WHERE id NOT IN (SELECT id FROM (SELECT id FROM ",
        tname,
        " t GROUP BY date,skin_float,store_name,prices HAVING id = MIN(id)) t)");
        PREPARE sl FROM @a;
        EXECUTE sl;
        DEALLOCATE PREPARE sl;
END$$
DELIMITER ;


/* DupRemove_All():对数据库内所有表去重
	 完成  */
DELIMITER $$
DROP PROCEDURE IF EXISTS DupRemove_All$$
CREATE PROCEDURE DupRemove_All()
BEGIN
	DECLARE i INT;
    DECLARE tname VARCHAR(20);
	DECLARE tname_cur CURSOR FOR 
		SELECT TABLE_NAME FROM information_schema.tables
		WHERE TABLE_SCHEMA = '你的库名称';
    OPEN tname_cur;
    SET i =1;
    WHILE i <= (SELECT COUNT(*) FROM ( SELECT TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA = '你的库名称' ) t) DO
		FETCH tname_cur INTO tname;
        SET @a := CONCAT("DELETE FROM ",
        tname,
        " WHERE id NOT IN (SELECT id FROM (SELECT id FROM ",
        tname,
        " t GROUP BY date,skin_float,store_name,prices HAVING id = MIN(id)) t)");
        PREPARE sl FROM @a;
        EXECUTE sl;
		SET i = i+1;
    END WHILE;
END$$
DELIMITER ;


/* AddPrkey_ALL():对数据库内所有表添加自增主键id
	完成   */
DELIMITER $$
DROP PROCEDURE IF EXISTS AddPrkey_ALL$$
CREATE PROCEDURE AddPrkey_ALL()
BEGIN
	DECLARE i INT;
    DECLARE tname VARCHAR(20);
	DECLARE tname_cur CURSOR FOR 
    SELECT TABLE_NAME FROM information_schema.tables
	WHERE TABLE_SCHEMA = '你的库名称';
    OPEN tname_cur;
    SET i =1;
    WHILE i <= (SELECT  COUNT(*) FROM ( SELECT TABLE_NAME FROM information_schema.tables WHERE TABLE_SCHEMA = '你的库名称' ) t) DO
		FETCH tname_cur INTO tname;
        SET @a = CONCAT("ALTER TABLE ",tname," DROP COLUMN id");
        SET @b = CONCAT("ALTER TABLE ",tname," ADD COLUMN id INT PRIMARY KEY AUTO_INCREMENT FIRST");
        PREPARE sl FROM @a;
        EXECUTE sl;
        DEALLOCATE PREPARE sl;
		PREPARE sl FROM @b;
        EXECUTE sl;
        DEALLOCATE PREPARE sl;
		SET i = i+1;
    END WHILE;
END$$
DELIMITER ;


/* CreateNewTable(skin_name):新建表
	  完成 */
DELIMITER $$
DROP PROCEDURE IF EXISTS CreateNewTable $$
CREATE PROCEDURE CreateNewTable(IN skin_name VARCHAR(20))
BEGIN 
	SET @a := CONCAT("CREATE TABLE IF NOT EXISTS ",skin_name,"       
            (
                id INT PRIMARY KEY AUTO_INCREMENT,
                skin_name VARCHAR(20),
                skin_float_type VARCHAR(6),
                skin_float DECIMAL(18,17),
                prices INT,
                store_name VARCHAR(20),
                stock VARCHAR(10),
                date DATE
            )");
	PREPARE sl FROM @a;
    EXECUTE sl;
    DEALLOCATE PREPARE sl;
END $$
DELIMITER ;


/* InsertData():插入数据
	 完成  */
DELIMITER $$
DROP PROCEDURE IF EXISTS InsertData $$
CREATE PROCEDURE InsertData(IN skin_name VARCHAR(20),IN skin_float_type VARCHAR(6),IN skin_float DECIMAL(18,17),IN prices INT,IN store_name VARCHAR(20),IN stock VARCHAR(10))
BEGIN 
	SET @a := CONCAT("INSERT INTO ",skin_name,"(
		skin_name,
		skin_float_type,
		skin_float,
		prices,
		store_name,
		stock,
		date
	)
    VALUES(",skin_name,",",skin_float_type,",",skin_float,",",prices,",",store_name,",",stock,",CURRENT_DATE())");
    PREPARE sl FROM @a;
    EXECUTE sl;
    DEALLOCATE PREPARE sl;
END $$
DELIMITER ;


/* Info_Count ():计算数据库中数据总数
	完成   */
DELIMITER $$
DROP PROCEDURE IF EXISTS Info_Count $$
CREATE PROCEDURE Info_Count()
BEGIN
	SELECT SUM(TABLE_ROWS) AS dbRows_Total FROM INFORMATION_SCHEMA.TABLES
	WHERE TABLE_SCHEMA = "你的库名称";
END $$
DELIMITER ;


