#import cv2
import numpy as np
import matplotlib.pyplot as plt

img = plt.imread('temp.png')

#tmp = cv2.resize(img, (1280, 720), 
#               interpolation = cv2.INTER_LINEAR)

#cv2.imwrite('../pictures/test_track3_resized.png', tmp)


plt.imshow(img)
plt.show()
