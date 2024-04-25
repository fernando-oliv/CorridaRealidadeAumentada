import cv2
import matplotlib.pyplot as plt

def resize():
    img = plt.imread('../pictures/test_track3.jpg')
    tmp = cv2.resize(img, (1280, 720), interpolation = cv2.INTER_LINEAR)
    cv2.imwrite('../pictures/test_track3_resized.png', tmp)