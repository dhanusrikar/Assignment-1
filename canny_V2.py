# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 20:33:09 2020

@author: srikar
"""

import cv2
import numpy as np

def gaussian(I, patch_size):
    #gauss matrix
    patch = [[1,2,1],[2,4,2],[1,2,1]]
    patch = np.array(patch)
    size_i = I.shape
    
    I1 = np.zeros([size_i[0] - 2, size_i[1]-2])    
    for i in range(size_i[0] - 2):
        for j in range(size_i[1]-2):
            
            output = np.zeros(patch_size)
            for k in range(patch_size[0]):
                for l in range(patch_size[1]):
                    output[k,l] = I[k+i, l+j]
                    
            temp = np.sum(patch*output)
            temp = temp/16
            I1[i, j] = temp
    cv2.imwrite('graussian.png', I1)
    return I1


def gradient(I, patch_size):
    patch_x = [[1,0,-1],[2,0,-2],[1,0,-1]]
    patch_x = np.array(patch_x)
    patch_y = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    patch_y = np.array(patch_y)
    size_i = I.shape
    Imag = np.zeros([size_i[0] - 2, size_i[1]-2])
    
    for i in range(size_i[0] - 2):
        for j in range(size_i[1]-2):
            
            output = np.zeros(patch_size)
            for k in range(patch_size[0]):
                for l in range(patch_size[1]):
                    output[k,l] = I[k+i, l+j]
                    
            temp1 = np.sum(patch_x*output) / 8
            temp2 = np.sum(patch_y*output) / 8
            Imag[i, j] = np.sqrt(temp1**2 + temp2**2)
            
    cv2.imwrite('gradient.png', Imag)
    return Imag
    
def laplace(I, patch_size):
    patch = [[0,1,0],[1,-4,1],[0,1,0]]
    patch = np.array(patch)
    
    size_i = I.shape
    
    I1 = np.zeros([size_i[0] - 2, size_i[1]-2])
    #I1 = copy.deepcopy(I)
    
    for i in range(size_i[0] -  2):
        for j in range(size_i[1]-2):
            
            output = np.zeros(patch_size)
            for k in range(patch_size[0]):
                for l in range(patch_size[1]):
                    output[k,l] = I[k+i, l+j]
                    
            temp = np.sum(patch*output)
            I1[i, j] = temp
    
    cv2.imwrite('laplace.png', I1)
    return I1    
    
def hysteresis(I):
    t1 = 160
    t2 = 180
    size_i = I.shape
    ht = np.where(I > t1)
    lt = np.where(I < t2)
    I[ht] = 255
    I[lt] = 0
    
    for i in range(1, size_i[0] - 1):
        for j in range(1, size_i[1] - 1):
            if(I[i, j] > t1 and I[i,j] < t2):
                temp = max(I[i+1, j], I[i-1, j], I[i, j+1], I[i, j-1])
                if(temp == 255):
                    I[i, j] = 255
                else:
                    I[i,j] = 0
    cv2.imwrite('hys.png', I)
    return I
                    

I = cv2.imread('testing_image.png',0)
patch_size = [3,3]
I = gaussian(I, patch_size)
I = gaussian(I, patch_size)
I_grad = gradient(I, patch_size)
I_lap = laplace(I_grad, patch_size)
I = gaussian(I_lap, patch_size)
I = gaussian(I, patch_size)
I = gaussian(I, patch_size)
I = np.uint8(gaussian(I_lap, patch_size))
I_hys = hysteresis(I)
