"""
Connect to MYSQL Database: spider_python
"""

import pymysql


def config():  # Database Config
    cfg = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'yourpasswor',
        'db': 'yourdatabase',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    return cfg


