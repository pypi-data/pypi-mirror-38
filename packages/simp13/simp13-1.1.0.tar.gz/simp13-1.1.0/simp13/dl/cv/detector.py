from urllib.request import urlretrieve
from six.moves.urllib.error import HTTPError
from six.moves.urllib.error import URLError
import numpy as np
import progressbar
import zipfile
import cv2
import os 


class Detector:
	def __init__(self,detector=None,filter_confidence=0.5,filter_threshold=0.3):
		self.root_path = ".simp13/models/"
		self.detector = detector
		self.filter_confidence = filter_confidence
		self.filter_threshold = filter_threshold
		self.progressbar = None

	def detect(self,input_image):
		
		if not os.path.exists(self.root_path):
			os.makedirs(self.root_path)

		if self.detector == None:
			raise "You must need to specify detector example YOLO"

		elif self.detector.lower().strip() == "yolo":
			return self.yolo_opencv_detector(input_image)

		else:
			raise "Not found that model"

	def yolo_opencv_detector(self,input_image):

		if not os.path.exists(os.path.join(self.root_path,"yolo")):
			os.makedirs(os.path.join(self.root_path,"yolo"));
			
		files = os.listdir(os.path.join(self.root_path,"yolo"))
		if len(files) <= 0:
			self.download(model='yolo')

		labelsPath = os.path.sep.join([self.root_path,"yolo", "coco.names"])
		LABELS = open(labelsPath).read().strip().split("\n")

		# initialize a list of colors to represent each possible class label
		np.random.seed(42)
		COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
			dtype="uint8")

		# derive the paths to the YOLO weights and model configuration
		weightsPath = os.path.sep.join([self.root_path,"yolo", "yolov3.weights"])
		configPath = os.path.sep.join([self.root_path,"yolo", "yolov3.cfg"])

		# load our YOLO object detector trained on COCO dataset (80 classes)
		print("[INFO] loading YOLO from disk...")
		net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

		# load our input image and grab its spatial dimensions
		
		image = input_image
		(H, W) = image.shape[:2]

		# determine only the *output* layer names that we need from YOLO
		ln = net.getLayerNames()
		ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

		# construct a blob from the input image and then perform a forward
		# pass of the YOLO object detector, giving us our bounding boxes and
		# associated probabilities
		blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
			swapRB=True, crop=False)
		net.setInput(blob)
		layerOutputs = net.forward(ln)

		# initialize our lists of detected bounding boxes, confidences, and
		# class IDs, respectively
		boxes = []
		confidences = []
		classIDs = []

		# loop over each of the layer outputs
		for output in layerOutputs:
			# loop over each of the detections
			for detection in output:
				# extract the class ID and confidence (i.e., probability) of
				# the current object detection
				scores = detection[5:]
				classID = np.argmax(scores)
				confidence = scores[classID]

				# filter out weak predictions by ensuring the detected
				# probability is greater than the minimum probability
				if confidence > self.filter_confidence:
					# scale the bounding box coordinates back relative to the
					# size of the image, keeping in mind that YOLO actually
					# returns the center (x, y)-coordinates of the bounding
					# box followed by the boxes' width and height
					box = detection[0:4] * np.array([W, H, W, H])
					(centerX, centerY, width, height) = box.astype("int")

					# use the center (x, y)-coordinates to derive the top and
					# and left corner of the bounding box
					x = int(centerX - (width / 2))
					y = int(centerY - (height / 2))

					# update our list of bounding box coordinates, confidences,
					# and class IDs
					boxes.append([x, y, int(width), int(height)])
					confidences.append(float(confidence))
					classIDs.append(classID)

				# apply non-maxima suppression to suppress weak, overlapping bounding
				# boxes
		idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.filter_confidence,
			self.filter_threshold)

		# ensure at least one detection exists
		if len(idxs) > 0:
			# loop over the indexes we are keeping
			for i in idxs.flatten():
				# extract the bounding box coordinates
				(x, y) = (boxes[i][0], boxes[i][1])
				(w, h) = (boxes[i][2], boxes[i][3])

				# draw a bounding box rectangle and label on the image
				color = [int(c) for c in COLORS[classIDs[i]]]
				text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
				

				yield ((x,y,w,h),color,text)


	def download_progress(self,count,block_size,total_size):
		widgets = ["Downloading model: ", progressbar.Percentage(), " ",
			progressbar.Bar(), " ", progressbar.ETA()]
		if self.progressbar is None:
			self.progressbar = progressbar.ProgressBar(maxval=total_size,widgets=widgets).start()
		if count * block_size < total_size:
			self.progressbar.update(count * block_size)
		else:
			self.progressbar.finish()
			self.progressbar = None

	def download(self,model=None):
		if model is None:
			raise "can't download model"
		if model == "yolo":
			
			origin = "https://s3-us-west-2.amazonaws.com/s3pyrobocity/media/models/yolo.zip"
			filename = origin.split("/")[-1]
			yolo_path = os.path.sep.join([self.root_path,"yolo"])
			fpath = os.path.sep.join([self.root_path,"yolo",filename])
			if not os.path.exists(yolo_path):
				os.makedirs(yolo_path)
			try:
			    try:
			        urlretrieve(origin, fpath, self.download_progress)
			    except HTTPError as e:
			        raise Exception(error_msg.format(origin, e.code, e.msg))
			    except URLError as e:
			        raise Exception(error_msg.format(origin, e.errno, e.reason))
			except (Exception, KeyboardInterrupt):
			    if os.path.exists(fpath):
			        os.remove(fpath)
			    raise
			print("[INFO] Extracting...")
			try:
				zip_ref = zipfile.ZipFile(fpath, 'r')
				zip_ref.extractall(yolo_path)
				zip_ref.close()
			except Exception as e:
				raise
			print("[INFO] Finished...")
