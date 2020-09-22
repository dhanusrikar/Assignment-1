# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 16:01:10 2020

@author: srikar
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt


I = cv2.imread('hys.png', 0)
img = cv2.imread('hys.png')

size_i = I.shape
theta = np.linspace(-90.0, 90.0, 181)
q = np.int(np.ceil(np.sqrt((size_i[0]-1)**2+(size_i[1]-1)**2)))
nrho = np.int(2*q + 1)
rho = np.linspace(-q, +q, nrho)
I1 = np.zeros((len(rho), len(theta)))
I1 = np.array(I1)
for i in range(size_i[0]):
    for j in range(size_i[1]):
        if(I[i,j]):
            for x in range(len(theta)):
                rad = np.pi / 180.0
                rhoVal =int(np.abs(i*np.sin(theta[x]*rad)+j*np.cos(theta[x]*rad)))
                I1[rhoVal, x] += 1


plt.imshow(I1, origin='lower')
plt.xlim(0,180)
plt.ylim(0,450)

sorted_arr = I1[I1[:,0].argsort()]
max_row = np.amax(sorted_arr, axis = 1)
max_col = np.amax(sorted_arr, axis = 0)
fin = sorted(np.unique(np.concatenate((max_row, max_col))))
fin = fin[::-1]
fin = fin[:10]

for x in range(len(rho)):
    for y in range(len(theta)):
        if(I1[x, y] in fin):
            a = np.cos(y*np.pi/180.0);
            b = np.sin(y*np.pi/180.0);
            
            if(y == 0 or y == 180): #horizontal line
                y0 = int(a * x)
                cv2.line(img, (0, y0), (size_i[0], y0), (255, 0, 0), 1)
            elif(y == 90): #vertical line
                x0 = int(b * x)
                cv2.line(img, (x0, 0), (x0, size_i[1]), (255, 0, 0), 1)
            
            else:
                m = (a/ b)
                c = x / b
                x1 = 0
                y1 = int(c + m * x1)
                x2 = size_i[0]
                y2 = int(c + m * x2)
                #print(x, y, x1, y1, x2, y2)
                cv2.line(img, (y1, x1), (y2, x2), (255, 0, 0), 1)
        
                                                                                
cv2.imwrite('EDGES.png', img)         