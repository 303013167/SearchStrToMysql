import pymysql

#数据库IP
db_ip = input("请输入数据库IP：")
#db_ip = "localhost"
#数据库用户名
db_name = input("请输入数据库用户名：")
#db_name = "root"
#数据库密码
db_password = input("请输入数据库密码：")
#db_password = "root"
#数据库名称
db_table = input("请输入数据库名称：")
#db = "test1"
#要查询的字符串
seach_str = input("请输入查询的字符串：")
#seach_str = "C48001"

pf = input("请输入盘符：")

#打开数据库连接
try:
    db = pymysql.connect(db_ip, db_name, db_password, db_table)
except :
    print("数据库连接失败")
else:
    print("连接数据库成功！")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询  --获取所有的表名
cursor.execute("select table_name from information_schema.tables where table_schema='"+db_table+"'")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()

desktop_path = pf+":\\"  # 新创建的txt文件的存放路径
full_path = str(desktop_path + 'table.txt')
file = open(full_path, 'a')

print("写入数据中...........")


for row in data:
    table_name = row[0]

    cursor.execute("select column_name,data_type from information_schema.COLUMNS where TABLE_NAME='"+table_name+"'")

    data1 = cursor.fetchall()

    for row1 in data1:
        column_name = row1[0]
        data_type = row1[1]

        if data_type == "date" or data_type == "datetime":
            continue

        try:
            cursor.execute("select * from "+table_name+" where "+column_name+" like '%"+seach_str+"%'")

            count = cursor.fetchone()

            if not count is None:
                file.write("字符串"+seach_str+"存在于表："+table_name+" 字段："+column_name+"")
                file.write('\n')
                print("字符串"+seach_str+"存在于表："+table_name+" 字段："+column_name+"")
        except :
            print()
print("已生成table.txt文件到" + pf + "盘根目录")
