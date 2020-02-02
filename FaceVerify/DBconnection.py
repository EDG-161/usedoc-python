import pymysql
import json
from Usedoc import Cipher

def vefUser(email,password):
    pass

def login(email,password):
    db = pymysql.connect("gautabases.ga","usedoc_user","Use_pass223856220","usedoc")
    cursor = db.cursor()
    sql = "SELECT * FROM musuarios where email_usr='{}' && pass_usr='{}' limit 1".format(Cipher.encrypt(email),Cipher.encrypt(password))
    cursor.execute(sql)
    try:
        result = cursor.fetchall()

        user = {
            "id_usr":result[0][0],
            "email_usr":result[0][1],
            "reg_usr":Cipher.decrypt(result[0][3]),
            "id_tid":result[0][4],
            "img_usr":result[0][5],
            "key_usr":result[0][6],
        }
        db.close()
        return json.dumps(user)
    except:
        db.close()
        return "Error"


def vef_session(key):
    db = pymysql.connect("gautabases.ga","usedoc_user","Use_pass223856220","usedoc")
    cursor = db.cursor()
    res = []
    sql = "SELECT id_usr FROM musuarios where key_usr = '{}' limit 1".format(key)
    cursor.execute(sql)
    res = cursor.fetchall()
    db.close()
    return res