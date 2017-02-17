import sys
from scrapy.cmdline import execute

# Select the SpiderScript
sys.argv[2] = "Douban_Movie"
print("开始进行爬虫，爬虫脚本SpiderScript为："+sys.argv[2])

# Start Spider
execute()

"""
# Connect MySQL
connection = pymysql.connect(**Database.config())

# Execute SQL
try:
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM test_table'
        cursor.execute(sql)
        for r in cursor:
            print(r)
    connection.commit()

finally:
    connection.close()
"""