import pymysql
from Usedoc import Cipher


def login():
    db = pymysql.connect("gautabases.ga","usedoc_user","Use_pass223","microuniverse")
    cursor = db.cursor()
    grafica = []
    sql = "SELECT * FROM cbacteria"
    cursor.execute(sql)
    grafica = cursor.fetchall()
    db.close()