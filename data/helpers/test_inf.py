import cv2
import numpy as np
import argparse

with open('test.txt') as f:
    lines = f.read().splitlines()

image_list = [i.strip("custom_data/") for i in lines]

print(image_list)

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--config", default='cfg/yolov3.cfg', help="YOLO config path")
parser.add_argument("--weights", default='yolov3.weights', help="YOLO weights path")
parser.add_argument("--names", default='data/coco.names', help="class names path")
args = parser.parse_args()

CONF_THRESH, NMS_THRESH = 0.5, 0.5

# Load the network
net = cv2.dnn.readNetFromDarknet(args.config, args.weights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Get the output layer from YOLO
layers = net.getLayerNames()
output_layers = [layers[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Read and convert the image to blob and perform forward pass to get the bounding boxes with their confidence scores
for i in image_list:
    img = cv2.imread(i)
    height, width = img.shape[:2]
    #print(height, width)

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layers)

    class_ids, confidences, b_boxes = [], [], []
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > CONF_THRESH:
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                b_boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))

    # Perform non maximum suppression for the bounding boxes to filter overlapping and low confident bounding boxes
    #print(cv2.dnn.NMSBoxes(b_boxes, confidences, CONF_THRESH, NMS_THRESH))
    try:
        indices = cv2.dnn.NMSBoxes(b_boxes, confidences, CONF_THRESH, NMS_THRESH).flatten().tolist()

        # Draw the filtered bounding boxes with their class to the image
        with open(args.names, "r") as f:
            classes = [line.strip() for line in f.readlines()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))

        rows = []

        for index in sorted(indices):
            x, y, w, h = b_boxes[index]
            rows.append((class_ids[index], CONF_THRESH, float(x), float(y), float(x + w), float(y + h)))
            #print((x, y), (x + w, y + h), class_ids[index])

        with open("./input/detection-results/"+str(i.split('/')[-1].split('.')[0])+".txt", "w") as text_file:
            for i in rows:
                j = str(i).replace(',', '')
                text_file.write(j[1:len(j)-1]+'\n')
    except:
        pass