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
from .forms import UploadImageForm
from .models import AlbumImage

from base64 import b64decode
from django.core.files.base import ContentFile
  

# Create your views here. 
def upload_image_view(request):
	if request.method == 'POST':
		print(request.FILES)
		img_base64 = request.POST["img"]
		data = ContentFile(b64decode(img_base64), 'whatup.png')
		print (data)
		newImage = AlbumImage()
		newImage.image = data
		newImage.album = "as"
		newImage.save() 
		form = UploadImageForm(request.POST, request.FILES)
		
		if form.is_valid():
			message = "Image uploaded succesfully!"
			form.save()
			
		else:
			message="no se pudo"
			form = UploadImageForm()

	return HttpResponse(message) 

def connection(request):
	return HttpResponse("Se conecto")