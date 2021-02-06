from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
import glob

def getAreaOfPolyGonbyVector(points):

	area = 0
	for i in range(0,len(points)-1):
		p1 = points[i]
		p2 = points[i + 1]

		triArea = (p1[0]*p2[1] - p2[0]*p1[1])/2
		area += triArea

	fn=(points[-1][0]*points[0][1]-points[0][0]*points[-1][1])/2
	return abs(area+fn)

def loadImage():
	img = []
	files = glob.glob(r'.\fig_1\*')
	for fl in files:
		image = cv2.imread(fl)
		image = cv2.resize(image, (1200, 1600),0,0, cv2.INTER_LINEAR)
		img.append(image)
	return np.array(img)


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

images = loadImage()
Area = [[], [], [], [], [], []]

#image, x, y, w, h
list = [[[], [], [], []],
		[[], [], [], []],
		[[], [], [], []],
		[[], [], [], []],
		[[], [], [], []],
		[[], [], [], []]]

#image
for r in range(len(images)):

	image = images[r]
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	rects = detector(gray, 1)

	#face
	for (i, rect) in enumerate(rects):
		count = 0
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		#左眼右眼
		for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
			if count == 4 or count == 5:
				Area[r].append(getAreaOfPolyGonbyVector(shape[i:j]))

				(x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
				list[r][0].append(x-25)
				list[r][1].append(y-25)
				list[r][2].append(w+50)
				list[r][3].append(h+40)

			count = count + 1

n = np.array(Area)
nT = np.transpose(n)
index = []

for i in range(nT.shape[0]):
	index.append(nT[i].argmax())

#張數 元素數 眼鏡個數
#x, y, w, h
n = np.array(list)

for i in range(n.shape[2]):#眼睛
	print(i)
	for j in range(n[1][3][0]):#w
		images[0][n[1][1][i] + j][n[1][0][i]:n[1][0][i] + n[1][2][0]] = images[index[i]][n[1][1][i] + j][n[1][0][i]:n[1][0][i] + n[1][2][0]]

cv2.imshow("CLONE", images[0])
cv2.waitKey(0)