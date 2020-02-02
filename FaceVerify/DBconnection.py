import pymysql
from Usedoc import Cipher


def login():
    db = pymysql.connect("gautabases.ga","usedoc_user","Use_pass223856220","microuniverse")
    cursor = db.cursor()
    grafica = []
    sql = "SELECT * FROM cbacteria"
    cursor.execute(sql)
    grafica = cursor.fetchall()
    db.close()

def vef_session(key):
    db = pymysql.connect("gautabases.ga","usedoc_user","Use_pass223856220","usedoc")
    cursor = db.cursor()
    res = []
    sql = "SELECT id_usr FROM musuarios where key_usr = '{}' limit 1".format(key)
    cursor.execute(sql)
    res = cursor.fetchall()
    db.close()
    return res