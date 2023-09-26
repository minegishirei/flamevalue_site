import sqlite3


class SQLiteProfileImage():
    def __init__(self):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        dbname = "/sqlite/profile_image.db"
        self.conn = sqlite3.connect(dbname)
        self.conn.row_factory = dict_factory
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS USER_PROFILE_IMAGES(
            E_MAIL STRING,
            profile_image_url STRING NOT NULL,
            PRIMARY KEY(E_MAIL)
        )
        """)
        
    def end(self):
        self.conn.close()

    def replace(self, e_mail, profile_image_url):
        cur = self.conn.cursor()
        sql = f'replace into USER_PROFILE_IMAGES values("{e_mail}", "{profile_image_url}")'
        try:
            cur.execute(sql)
            self.conn.commit()
        except:
            self.conn.close()
            return False
        self.conn.close()
        return True

    def fetch(self, e_mail):
        cur = self.conn.cursor()
        cur.execute(f'SELECT * FROM USER_PROFILE_IMAGES WHERE e_mail="{e_mail}"')
        try:
            result =  cur.fetchall()[0]
        except:
            return None
        self.conn.close()
        return result

