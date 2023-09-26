
import sqlite3



class UserInfoCollector():
    def __init__(self):
        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        self.dbname1 = "/sqlite/goodness_counter.db"
        self.dbname2 = "flamevalue_user"
        self.dbfilename2 = "/sqlite/v6_flamevalue_user.db"
        self.dbname3 = "profile_image"
        self.dbfilename3 = "/sqlite/profile_image.db"
        self.conn = sqlite3.connect(self.dbname1)
        self.conn.row_factory = dict_factory
        # テーブル初期化
        cur = self.conn.cursor()
        cur.execute(f"ATTACH DATABASE '{self.dbfilename2}' as {self.dbname2};")
        cur.execute(f"ATTACH DATABASE '{self.dbfilename3}' as {self.dbname3};")
    
    def end(self):
        self.conn.close()

    def fetch_user_fullinfo(self, e_mail):
        cur = self.conn.cursor()
        sql = f"""
        select
            users.username username,
            users.password hashed_password,
            users.e_mail e_mail,
            group_concat(goodness_counter.FLAMEWORK_NAME) flamework_names,
            user_profile_images.profile_image_url profile_image_url
        from 
            {self.dbname2}.FLAMEVALUE_USERS users,
            GOODNESS_COUNTER goodness_counter,
            {self.dbname3}.USER_PROFILE_IMAGES user_profile_images
        where 1=1
            and users.e_mail=goodness_counter.e_mail
            and users.e_mail=user_profile_images.e_mail
            and users.e_mail="{e_mail}"
        group by
            users.e_mail
        order by
            users.e_mail
        """
        result = {}
        cur.execute(sql)
        fetch_result = cur.fetchall()
        result = fetch_result
        self.conn.commit()
        self.conn.close()
        return result[0]
    
    def get_user_good_flameworks(self, e_mail):
        cur = self.conn.cursor()
        sql = f"""
        select
            goodness_counter.FLAMEWORK_NAME
        from 
            {self.dbname2}.FLAMEVALUE_USERS users,
            goodness_counter goodness_counter
        where 1=1
            and users.e_mail=goodness_counter.e_mail
            and users.e_mail="{e_mail}"
        """
        result = {}
        try:
            cur.execute(sql)
            fetch_result = cur.fetchall()
            result = fetch_result
        except sqlite3.Error:
            pass
        self.conn.commit()
        self.conn.close()
        return result


    def get_users(self):
        cur = self.conn.cursor()
        sql = f"""
        select
            users.username username,
            group_concat(goodness_counter.FLAMEWORK_NAME) flamework_names,
            user_profile_images.profile_image_url profile_image_url
        from 
            {self.dbname2}.FLAMEVALUE_USERS users,
            GOODNESS_COUNTER goodness_counter,
            {self.dbname3}.USER_PROFILE_IMAGES user_profile_images
        where 1=1
            and users.e_mail=goodness_counter.e_mail
            and users.e_mail=user_profile_images.e_mail
        group by
            users.e_mail
        order by
            users.e_mail
        """
        result = {}
        cur.execute(sql)
        fetch_result1 = cur.fetchall()
        result = list(map(lambda row: { **row, "flamework_names" : row["flamework_names"].split(",") } ,fetch_result1))
        try:
            cur.execute(sql)
            fetch_result1 = cur.fetchall()
            result = list(map(lambda row: { **row, "flamework_names" : row["flamework_names"].split(",") } ,fetch_result1))
        except sqlite3.Error:
            pass
        self.conn.commit()
        self.conn.close()
        return result

