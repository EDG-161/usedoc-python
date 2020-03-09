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
import json
from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from django.conf import settings
from .forms import UploadImageForm
from .models import AlbumImage
from FaceVerify import DBconnection
from pymongo import MongoClient
from base64 import b64decode
from django.core.files.base import ContentFile
from FaceVerify.storage import OverwriteStorage
from django.core.files.storage import FileSystemStorage

def mongo(request):
	client = MongoClient("mongodb+srv://UseDoc_userDB:UsedocPass_223856220@cluster0-wyexi.mongodb.net/test?retryWrites=true&w=majority")
	db = client.test
	users = db['users']

	for user in users.find({'userType':"Paciente"}):
		print(user['imageRoute'])

	return HttpResponse("Parece que funciona ")

# Create your views here. 
def upload_image_view(request):
	message = "No se pudo"
	try:

		client = MongoClient("mongodb+srv://UseDoc_userDB:UsedocPass_223856220@cluster0-wyexi.mongodb.net/test?retryWrites=true&w=majority")
		db = client.test
		users = db['users']
		if request.method == 'POST':
			img_base64 = request.POST["img"]
			#id_usr = request.POST["id_usr"]
			name = request.POST["img_name"] + ".jpg"
			data = ContentFile(b64decode(img_base64), name)
			newImage = AlbumImage()
			newImage.image = data
			if os.path.isfile('static/images/'+name):
				print('static/images/'+name)
       			os.remove('static/images/' + name)
			newImage.album = name
			newImage.save() 
			message = "Image uploadedasdasdasdasd succesfully!"
			image_send = "https://verify.usedoc.ml/static/images/{}".format(newImage.album)
		for user in users.find({'userType':"Paciente"}):
			userRoute = 'http://157.245.161.67:3001/{}'.format(user['imageRoute'])
			if DBconnection.vefUser(userRoute,image_send):
				return HttpResponse(json.dumps(user))
			
		return HttpResponse('No se ha encontrado paciente')
	except Exception as e:
		print(e)
		message = "Error  "
	return HttpResponse(message) 

def connection(request):
	return HttpResponse("Se conecto")

def verify_session(request):
	try:
		user_key = request.POST["user_key"]
		id = DBconnection.vef_session(user_key)
		if id>0:
			return HttpResponse("verify_session_ok")
		else:
			return HttpResponse("error")
	except:
		return HttpResponse("error")

def login(request):
	try:
		email = request.POST["email"]
		password = request.POST["pass"]
		return HttpResponse(DBconnection.login(email,password),content_type='application/json')
	except Exception as E:
		return HttpResponse(E.args)