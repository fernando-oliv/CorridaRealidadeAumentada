import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


img = cv2.imread('../pictures/test_track3_resized.png')
result = np.ndarray((img.shape[0], img.shape[1], 4), dtype=np.uint8) #criando imagem cinza com transparencia
#img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#lower_color = np.array([0, 0, 0])
#upper_color = np.array([60, 255, 60])

    
src = cv2.GaussianBlur(img, (5, 5), 0)
#img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


img_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)




    
grad_x = cv2.Sobel(img_gray, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
# Gradient-Y
# grad_y = cv2.Scharr(gray_tmp,ddepth,0,1)
grad_y = cv2.Sobel(img_gray, cv2.CV_16S, 0, 1, ksize=3)


abs_grad_x = cv2.convertScaleAbs(grad_x)
abs_grad_y = cv2.convertScaleAbs(grad_y)


grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

threshold = 70
grad[grad < threshold] = 0
grad[grad > 0] = 1
#plt.imshow(grad, 'gray')
#plt.subplot(122)
#plt.imshow(mask1, 'gray')
#plt.imshow(img)
#plt.show()
#stretch_near = cv2.resize(grad, (1280, 720), 
#               interpolation = cv2.INTER_LINEAR)
#plt.imshow(grad, 'gray')
#plt.show()
grad2 = grad.copy()
cv2.floodFill(grad2, None, (150, 200), 1)

kernel = np.asarray([[0, 1, 0],
                     [1, 1, 0],
                     [0, 1, 0]], dtype=np.uint8)


grad2 = cv2.dilate(grad2, kernel, iterations = 10)

from skimage.morphology import skeletonize


path = skeletonize(grad2)
pathInt = np.ndarray((path.shape), dtype=np.uint8)
pathInt[path == False] = 0
pathInt[path == True] = 255
#plt.imshow(path, 'gray')
#plt.show()

grad *= 255

result[:,:,3] = grad[:,:]



cv2.imwrite('track_border.png', result)
cv2.imwrite('npc_path_line.png', pathInt)