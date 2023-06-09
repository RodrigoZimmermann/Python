# Rodrigo Luís Zimmermann

#Pré-processamento para para remoção de linhas da partitura
import cv2
from google.colab.patches import cv2_imshow
import numpy as np

image = cv2.imread('teste.png')

cv2_imshow(image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN,
horizontal_kernel, iterations=5)

cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

for c in cnts:
   cv2.drawContours(image, [c], -1, (255, 255, 255), 2)

repair_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))

result = 255 - cv2.morphologyEx(255 - image, cv2.MORPH_CLOSE, repair_kernel,
iterations=1)

cv2_imshow(image)
cv2.imwrite("image.png", image)
cv2.waitKey()
cv2.destroyAllWindows()

# Tratamento de erosão e dilatação para corrigir a remoção das linhas
import cv2
from google.colab.patches import cv2_imshow
img = cv2.imread('image.png', 0) 
kernel = np.ones((3,5), np.uint8) 
  
img_erosion = cv2.erode(img, kernel, iterations=1) 
img_dilation = cv2.dilate(img, kernel, iterations=1)
cv2_imshow(img_erosion)

#tecnicas para pegar contornos
import cv2
from google.colab.patches import cv2_imshow
import numpy as np

image = cv2.imread('image.png') 
cv2.waitKey(0) 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
edged = cv2.Canny(gray, 30, 200) 
cv2.waitKey(0) 
  
contours, hierarchy = cv2.findContours(edged,  
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
  
cv2_imshow(edged) 
cv2.waitKey(0) 
  
print("Number of Contours found = " + str(len(contours))) 
cv2.drawContours(image, contours, -1, (0, 0, 0), 3) 
  
cv2_imshow(image) 
cv2.waitKey(0) 
cv2.destroyAllWindows()

import cv2 as cv
import numpy as np
img = cv.imread('image.png')
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray,50,150,apertureSize = 3)
lines = cv.HoughLinesP(edges,1,np.pi/180,70,minLineLength=0,maxLineGap=100)
for line in lines:
    x1,y1,x2,y2 = line[0]
    cv.line(img,(x1-35,y1),(x2-35,y2),(0,255,0),2)
cv2_imshow(img)
cv.imwrite('image.png',img)

from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

model = load_model('keras_model.h5', compile = False)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
image = Image.open('finalteste.png').convert('RGB')
size = (224, 224)
image = ImageOps.fit(image, size, Image.ANTIALIAS)
image_array = np.asarray(image)
normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
data[0] = normalized_image_array
class_names = ['Eight', 'Half', 'Quarter', 'Sixteenth', 'Whole']
prediction = model.predict(data)
class_names[np.argmax(prediction)]