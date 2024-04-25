import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('npc_path_line_edited.png')

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


contours, hierarchy = cv2.findContours(image=img, mode=cv2.RETR_EXTERNAL, 
                                       method=cv2.CHAIN_APPROX_NONE)


#if contours[0].all() == contours[1].all():
#    print('iguais')

tmp = contours[0]
contours = tmp
#print(contours[0][0][0])


string = '['
for i in range(len(contours) - 1):
    string += f"[{contours[i][0][0]}, {contours[i][0][1]}],"
    if i % 99 == 98:
        string += "\n"
    else:
        string += " "
string += f'[{contours[-1][0][0]}, {contours[-1][0][1]}]'


print(string)