import os
from imutils import face_utils
import numpy as np
import dlib
import cv2
import glob
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

import pickle
import os
from base64 import urlsafe_b64decode, urlsafe_b64encode

from mimetypes import guess_type as guess_mime_type
import random
import string
from datetime import datetime
import shutil
# Create your views here.


def index(request):

	if request.method == "POST":
		repair(1)

	return render(request, "index.html",{})

def case1(request):

	if request.method == "POST":
		repair(1)

	return render(request, "case1.html",{})

def case2(request):

	if request.method == "POST":
		repair(2)

	return render(request, "case2.html",{})

def case3(request):

	if request.method == "POST":
		repair(3)

	return render(request, "case3.html",{})

def case4(request):

	if request.method == "POST":
		repair(4)

	return render(request, "case4.html",{})

def case5(request):

	if request.method == "POST":
		repair(5)

	return render(request, "case5.html",{})

def case6(request):

	if request.method == "POST":
		repair(6)

	return render(request, "case6.html",{})

def case7(request):

	if request.method == "POST":
		repair(7)

	return render(request, "case7.html",{})

def case8(request):

	if request.method == "POST":
		repair(8)

	return render(request, "case8.html",{})


def getAreaOfPolyGonbyVector(points):

	area = 0
	for i in range(0,len(points)-1):
		p1 = points[i]
		p2 = points[i + 1]

		triArea = (p1[0]*p2[1] - p2[0]*p1[1])/2
		area += triArea

		fn=(points[-1][0]*points[0][1]-points[0][0]*points[-1][1])/2
	return abs(area+fn)

def loadImage(c):
	img = []
	print(c)
	path = "./app/static/case"+str(c)+"\*"
	files = glob.glob(path)
	for fl in files:
		image = cv2.imread(fl)
		# image = cv2.resize(image, (1200, 1600),0,0, cv2.INTER_LINEAR)
		img.append(image)
	return np.array(img)

def repair(c):
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(r'.\shape_predictor_68_face_landmarks.dat')

	images = loadImage(c)

	Area = [[], [], []]

	list = [[[], [], [], []],
		  [[], [], [], []],
		  [[], [], [], []]]
	print(len(images))
	#image
	for r in range(len(images)):
		image = images[r]
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		rects = detector(gray, 1)
		
		for (i, rect) in enumerate(rects):
			count = 0
			shape = predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)
			
			#左眼右眼
			for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
				if count == 4:
					
					Area[r].append(getAreaOfPolyGonbyVector(shape[i:j]))
					# print(name + str(getAreaOfPolyGonbyVector(shape[i:j])))
					(x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
					list[r][0].append(x-45)
					list[r][1].append(y-40)
					list[r][2].append(w+85)
					list[r][3].append(h+95)
				if count == 5:
					Area[r].append(getAreaOfPolyGonbyVector(shape[i:j]))
					# print(name + str(getAreaOfPolyGonbyVector(shape[i:j])))
					(x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
					list[r][0].append(x-25)
					list[r][1].append(y-50)
					list[r][2].append(w+75)
					list[r][3].append(h+95)

				count = count + 1
	n = np.array(Area)
	nT = np.transpose(n)

	index = []
	for i in range(nT.shape[0]):
		nT[i] = np.array(nT[i])
		index.append(nT[i].argmax())

	# #張數 元素數 眼鏡個數
	# #x, y, w, h
	n = np.array(list)
	
	for i in range(2):#眼睛
		for j in range(n[1][3][0]):#w
			images[0][n[1][1][i] + j][n[1][0][i]:n[1][0][i] + n[1][2][0]] = images[index[i]][n[1][1][i] + j][n[1][0][i]:n[1][0][i] + n[1][2][0]]

	cv2.imwrite("./app/static/case"+str(c)+"/result.JPG", images[0])