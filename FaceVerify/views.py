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

from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from django.conf import settings
from .forms import UploadImageForm
from .models import AlbumImage
from .DBconnection import *

from base64 import b64decode
from django.core.files.base import ContentFile
  

# Create your views here. 
def upload_image_view(request):
	message = "No se pudo"
	try:
		if request.method == 'POST':
			img_base64 = request.POST["img"]
			name = request.POST["img_name"] + ".png"
			data = ContentFile(b64decode(img_base64), name)
			newImage = AlbumImage()
			newImage.image = data
			newImage.album = name
			newImage.save() 
			message = "Image uploaded succesfully!" 
	except Error:
		message = Error
	return HttpResponse(message) 

def connection(request):
	return HttpResponse("Se conecto")

def verify_session(request):
	try:
		user_key = request.POST["user_key"]
		id = DBconnection.vef_session(user_key)
		if id>0:
			return "verify_session_ok"
		else:
			return "error"
	except Error:
		return "error"
