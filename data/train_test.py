import glob
import os

current_dir = "custom_data/images"
# Percentage of images to be used for the valid set
percentage_test = 20
# Create train.txt and valid.txt
file_train = open('train.txt', 'w')
file_test = open('valid.txt', 'w')
# Populate train.txt and valid.txt
counter = 1
index_test = round(100 / percentage_test)
for file in glob.iglob(os.path.join(current_dir, '*.jpg')):
	title, ext = os.path.splitext(os.path.basename(file))
	if counter == index_test:
		counter = 1
		file_test.write(current_dir + "/" + title + '.jpg' + "\n")
	else:
		file_train.write(current_dir + "/" + title + '.jpg' + "\n")
	counter = counter + 1
