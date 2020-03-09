import pymysql
import json
from Usedoc import Cipher
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType

import http.client, urllib.request, urllib.parse, urllib.error, base64

def deleteFace(id_face):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'b44fab4424424f399c32ca79326182f2',
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("DELETE", "/face/v1.0/facelists/{id_face}/persistedFaces/{persistedFaceId}?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def vefUser(user,upload):
    KEY = 'b44fab4424424f399c32ca79326182f2'
    ENDPOINT = 'https://face-usedoc.cognitiveservices.azure.com/'
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    source_image_file_name1 = user
    target_image_file_names = upload
    print(source_image_file_name1 + "   " + target_image_file_names)
    detected_faces1 = face_client.face.detect_with_url(source_image_file_name1)
    print(detected_faces1)
    source_image1_id = detected_faces1[0].face_id
    detected_faces_ids = []
    detected_faces = face_client.face.detect_with_url(target_image_file_names)
    print(detected_faces)
    detected_faces_ids.append(detected_faces[0].face_id)

    verify_result_same = face_client.face.verify_face_to_face(source_image1_id, detected_faces_ids[0])
    deleteFace(source_image1_id)
    return verify_result_same.is_identical


def login(email,password):
    db = pymysql.connect("gautabases.ga","usedoc_user","Use_pass223856220","usedoc")
    cursor = db.cursor()
    cemail = Cipher.encrypt(email)
    cpassword = Cipher.encrypt(password)
    sql = "SELECT * FROM musuarios where email_usr='"+cemail+"'"
    sql = sql + "&& pass_usr='"+cpassword+"' limit 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result)>0:
        tabla = ""
        if result[0][4] == 1:
            tabla = "nom_med,appat_med,apmat_med,ced_med FROM mdoctores"
        else:
            tabla = "nom_pac,appat_pac,apmat_pac,sta_pac FROM mpacientes"
        sql = "SELECT "+tabla+" where id_usr={}".format(result[0][0])+" limit 1"
        cursor.execute(sql)
        second = cursor.fetchall()
        user = {
            "id_usr":result[0][0],
            "email_usr":result[0][1],
            "reg_usr":Cipher.decrypt(result[0][3]),
            "id_tid":result[0][4],
            "img_usr":Cipher.decrypt(result[0][5]),
            "key_usr":result[0][6],
            "name_usr":Cipher.decrypt(second[0][0]),
            "appat_usr":Cipher.decrypt(second[0][1]),
            "apmat_usr":Cipher.decrypt(second[0][2]),
            "dat_usr": "{}".format(second[0][3]),
        }
        
    else:
        user = {
            "id_usr":0,
            "email_usr":"",
            "reg_usr":"",
            "id_tid":0,
            "img_usr":"",
            "key_usr":"",
        }
    db.close()

    return json.dumps(user)

def getImageServer(id_usr):
    db = pymysql.connect("gautabases.ga","usedoc_user","Use_pass223856220","usedoc")
    cursor = db.cursor()
    sql = "SELECT * FROM musuarios where id_usr="+id_usr+" limit 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result)>0:
        cursor.execute(sql)
        second = cursor.fetchall()
        user = Cipher.decrypt(result[0][5])
        
    else:
        user = False
    db.close()

    return user

def vef_session(key):
    db = pymysql.connect("gautabases.ga","usedoc_user","Use_pass223856220","usedoc")
    cursor = db.cursor()
    res = []
    sql = "SELECT id_usr FROM musuarios where key_usr = '{}' limit 1".format(key)
    cursor.execute(sql)
    res = cursor.fetchall()
    db.close()
    return res