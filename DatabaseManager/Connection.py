import pymysql

class Connection(object):
    # __server = 'sql10.freemysqlhosting.net'
    __server = 'localhost'
    # __user = 'sql10190757'
    __user = 'root'
    # __password = 'bqwh8pTxPg'
    __password = ''
    # __database = 'sql10190757'
    __database = 'patrimonioifg'

    def __init__(self):
        self.db = pymysql.connect(host = Connection.__server, port = 3306, user = Connection.__user, passwd = Connection.__password, db = Connection.__database)
        self.cursor = self.db.cursor()
        print('Connected in database '+Connection.__database)

    def execute_sql(self, sql):
        self.cursor.execute(sql)
        return self.cursor

    def close_connection(self):
        self.db.close()
        print('Close database')

    def commit(self):
        self.db.commit()
        return

    def rollback(self):
        self.db.rollback()
        return
