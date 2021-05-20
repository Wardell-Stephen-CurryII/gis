# python mysql 操作类

import pymysql

# 数据库助手
class DBHelper:
    def __init__(self):
        try:
            self.host="127.0.0.1"
            self.port=3306
            self.user="root"
            self.password="qwe123"
            self.database="gis"
            self.conn = pymysql.connect(host=self.host,
                                        port=self.port,
                                        user=self.user,
                                        password=self.password,
                                        database=self.database,
                                        charset='utf8mb4')
            self.cur = self.conn.cursor()
        except Exception as e:
            print(e)

    def insert_data(self):
        pass

