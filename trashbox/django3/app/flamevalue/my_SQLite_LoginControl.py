import sqlite3
import hashlib

class SQLiteLoginControl():
    
    def __init__(self):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        dbname = "/sqlite/v6_flamevalue_user.db"
        self.conn = sqlite3.connect(dbname)
        self.conn.row_factory = dict_factory
        # テーブル初期化
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS FLAMEVALUE_USERS (
            E_MAIL STRING,
            USERNAME STRING NOT NULL,
            PASSWORD STRING NOT NULL,
            PRIMARY KEY (E_MAIL)
        )""")
        def build_hashing(secret_key):
            def hashing(target):
                return hashlib.sha256( (secret_key + target).encode() ).hexdigest()
                #return cipher.encrypt_and_digest(target)
            return hashing
        self.hashing = build_hashing("G0y6cfj3iqw84j3q8gp")

    def end(self):
        self.conn.close() 

    def create_acount(self, request):
        cur = self.conn.cursor()
        sql = f"""
        INSERT INTO 
            FLAMEVALUE_USERS(USERNAME, E_MAIL, PASSWORD)
        VALUES(
            "{request.POST.get("username")}", 
            "{request.POST.get("e_mail")}", 
            "{self.hashing(request.POST.get("unhashed_password"))}" 
        )
        """
        try:
            cur.execute(sql)
        except sqlite3.Error:
            self.conn.commit()
            self.conn.close()
            return False
        self.conn.commit()
        self.conn.close()
        return True
    
    def update_acount(self, e_mail, username):
        cur = self.conn.cursor()
        sql = f"""
        UPDATE 
            FLAMEVALUE_USERS
        SET 
            USERNAME = "{username}"
        Where
            E_MAIL = "{e_mail}"
        """
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
        return True

    def update_acount_password(self, e_mail, unhashed_password):
        cur = self.conn.cursor()
        sql = f"""
        UPDATE 
            FLAMEVALUE_USERS
        SET 
            PASSWORD = "{self.hashing(unhashed_password)}"
        Where
            E_MAIL = "{e_mail}"
        """
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
        return True

    def certification_by_unhashed_password(self, e_mail, unhashed_password):
        user_info = self.fetch_user_info( e_mail, self.hashing(unhashed_password) )
        if len(user_info) > 0:
            return True
        else:
            return False
    
    def certification_by_hashed_password(self, e_mail, hashed_password):
        user_info = self.fetch_user_info( e_mail, hashed_password )
        if len(user_info) > 0:
            return True
        else:
            return False
    
    def fetch_user_info(self, e_mail, hashed_password):
        # After
        cur = self.conn.cursor()
        sql = f"""
        select 
            users.USERNAME username,
            users.e_mail e_mail,
            users.password hashed_password
        from 
            FLAMEVALUE_USERS users
        where 1=1
            and users.e_mail = "{e_mail}"
            and users.password = "{hashed_password}"
        """
        result = {}
        try:
            cur.execute(sql)
            fetch_result = cur.fetchall()
            if len(fetch_result) > 0:
                result = fetch_result[0]
                result.update({
                    "username" : result["username"],
                    "e_mail" : result["e_mail"],
                    "hashed_password" : result["hashed_password"]
                })
        except sqlite3.Error:
            pass
        self.conn.close()
        return result

    def fetch_user_info_by_unhashed_password(self, e_mail, unhashed_password):
        # After
        cur = self.conn.cursor()
        sql = f"""
        select 
            users.USERNAME username,
            users.e_mail e_mail,
            users.password hashed_password
        from 
            FLAMEVALUE_USERS users
        where 1=1
            and users.e_mail = "{e_mail}"
            and users.password = "{self.hashing(unhashed_password)}"
        """
        result = {}
        try:
            cur.execute(sql)
            fetch_result = cur.fetchall()
            if len(fetch_result) > 0:
                result = fetch_result[0]
                result.update({
                    "username" : result["username"],
                    "e_mail" : result["e_mail"],
                    "hashed_password" : result["hashed_password"]
                })
        except:
            pass
        self.conn.close()
        return result

