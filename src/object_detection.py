import numpy as np
import cv2 as cv
from PIL import Image
from matplotlib import pyplot as plt

img_path = "/Users/coviam/obj_test/000278.jpg"


def get_output_layers(net):
	layer_names = net.getLayerNames()
	output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
	return output_layers


ROOT = "/Users/coviam/image_search/models/od/"
class_ids = []
confidences = []
boxes = []
confidence_thresh = 0.5
non_max_suppression_thresh = 0.4
input_width = 416
input_height = 416

scale = 0.00392
class_names = ROOT + "obj.names"
model_conf = ROOT + "yolo-small.cfg"
model_weights = ROOT + "yolo-small.weights"
classes = None

image = cv.imread(img_path)
Width = image.shape[1]
Height = image.shape[0]

with open(class_names, "rt") as file:
	classes = file.read().rstrip("\n").split("\n")

# generate different colors for different classes
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

cnn_model = cv.dnn.readNetFromDarknet(model_conf, model_weights)
cnn_model.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
cnn_model.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

# cnn_model.getLayerNames()

# pre-processing image
blob = cv.dnn.blobFromImage(image, 1 / 255, (input_width, input_height), (0, 0, 0), True, crop=False)

cnn_model.setInput(blob)

# output of 3 layers
outs = cnn_model.forward(get_output_layers(cnn_model))

# processing outputs of 3 layers
for out in outs:
	for detection in out:
		scores = detection[5:]
		class_id = np.argmax(scores)  # getting class no. of max score
		confidence = scores[class_id]
		if confidence > 0.5:
			center_x = int(detection[0] * Width)
			center_y = int(detection[1] * Height)
			w = int(detection[2] * Width)
			h = int(detection[3] * Height)
			x = center_x - w / 2
			# to get the corner value of bounding box we do w/2 and the subtract from center coordinates
			y = center_y - h / 2
			class_ids.append(class_id)
			confidences.append(float(confidence))
			boxes.append([x, y, w, h])
print boxes
# apply non-max suppression
indices = cv.dnn.NMSBoxes(boxes, confidences, confidence_thresh, non_max_suppression_thresh)


def get_cropped_image(x0, y0, x1, y1, image):
	image_pil = Image.fromarray(np.uint8(image)).convert('RGB')
	image_pil = image_pil.crop((x0, y0, x1, y1))
	image = np.array(image_pil)

	margin_x = max(0, 380 - x1)
	margin_y = max(0, 380 - y1)
	if margin_x != 0:
		print np.full((margin_x, 380, 3), 255).shape
		print image.shape
		image = np.concatenate((image, np.full((380, margin_x, 3), 255)), axis=1)
	if margin_y != 0:
		image = np.concatenate((image, np.full((margin_y, 380, 3), 255)), axis=0)
	plt.imshow(image)
	plt.show()

for i in indices:
	i = i[0]
	box = boxes[i]
	x = box[0]
	y = box[1]
	w = box[2]
	h = box[3]
	get_cropped_image(x, y, w, h, image)
