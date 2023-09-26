#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode

class DAO():
    def __init__(self, table):
        self.args = {
            'host':'db',
            'user':'user',
            'password':'passw0rd',
            'database':'stock_database',
            "charset":'utf8'
        }
        self.config = self.args.copy()
        self.config.update({
            "table" : table
        })
        self.conn = None
        self.cursor = None
    
    def run(self, cmd):
        # Drop previous table of same name if one exists
        #self.cursor.execute("DROP TABLE IF EXISTS inventory;")
        #print("Finished dropping table (if existed).")
        self.cursor.execute(cmd)
        return self.cursor.fetchall()

    def select_all(self):
        self.cursor.execute('SELECT * FROM {}.{}'.format( self.config["database"] , self.config["table"]) )
        return self.cursor.fetchall()

    def __enter__(self):
        try:
            self.conn = mysql.connector.connect(**self.args)
        except mysql.connector.Error as err:
            raise err
        else:
            self.cursor = self.conn.cursor(dictionary=True)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

class DatabaseCreatableDAO(DAO):
    def __init__(self, database_name):
        self.database_name = database_name
        super().__init__("")
    
    def __enter__(self):
        self = super().__enter__()
        # Drop previous table of same name if one exists
        #self.cursor.execute("DROP TABLE IF EXISTS inventory;")
        #print("Finished dropping table (if existed).")
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database_name}")
        return self


class TableCreatableDAO(DAO):
    def __init__(self, table, column):
        self.column = column
        super().__init__(table)
    
    def __enter__(self):
        self = super().__enter__()
        # Drop previous table of same name if one exists
        #self.cursor.execute("DROP TABLE IF EXISTS inventory;")
        #print("Finished dropping table (if existed).")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS {} ({});""".format(self.config["table"], self.column))
        return self


##コマンド実行系

class InsertableDAO(DAO):
    def __init__(self, table):
        super().__init__(table)
    
    def insert(self, values):
        self = super().__enter__()
        sql = f"INSERT INTO {self.config['table']} VALUES {values};"
        self.cursor.execute(sql)
        return self


class CmdDAO(DAO):
    def __init__(self, table):
        super().__init__(table)
    
    def run(self, cmd):
        self = super().__enter__()
        # Drop previous table of same name if one exists
        #self.cursor.execute("DROP TABLE IF EXISTS inventory;")
        #print("Finished dropping table (if existed).")
        self.cursor.execute(cmd)
        return self.cursor.fetchall()


def create_newTable(name, column, newList):
    with InsertableDAO(name, column) as insertableDAO:
        for row in newList:
            insertableDAO(row)
    
