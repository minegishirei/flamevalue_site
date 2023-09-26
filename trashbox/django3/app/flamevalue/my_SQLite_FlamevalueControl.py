
import sqlite3

class SQLiteFlamevalueControl():
    def __init__(self, filepath='/sqlite/goodness_counter.db'):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        dbname = filepath
        self.conn = sqlite3.connect(dbname)
        # テーブル初期化
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS GOODNESS_COUNTER(
            E_MAIL STRING,
            FLAMEWORK_NAME STRING,
            PRIMARY KEY(E_MAIL, FLAMEWORK_NAME)
        )
        """)
 
    def end(self):
        self.conn.close()

    def add_one_good(self, e_mail, flamework_name):
        cur = self.conn.cursor()
        sql = f'INSERT INTO GOODNESS_COUNTER(E_MAIL, FLAMEWORK_NAME) values("{e_mail}", "{flamework_name}")'
        try:
            cur.execute(sql)
        except sqlite3.Error:
            pass
        self.conn.commit()
        self.conn.close()
    
    def get_goodness_count(self, flamework_name):
        cur = self.conn.cursor()
        cur.execute(f'SELECT count(*) good_count FROM GOODNESS_COUNTER WHERE FLAMEWORK_NAME="{flamework_name}"')
        result =  cur.fetchall()
        self.conn.close()
        return result
   
    def get_select_all(self):
        cur = self.conn.cursor()
        cur.execute(f'SELECT * FROM GOODNESS_COUNTER')
        result =  cur.fetchall()
        self.conn.close()
        return result









