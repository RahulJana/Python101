# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 19:40:34 2020

@author: HP
"""

# Images are NumPy’s arrays
import numpy as np
check = np.zeros((8, 8))
check[::2, 1::2] = 2
check[1::2, ::2] = 2
import matplotlib.pyplot as plt
plt.imshow(check, cmap='gray', interpolation='nearest')
# cmap() method which returns a matplotlib color map with n colors.
# Interpolation is the process of finding a value between two points on a line or a curve


from skimage import data
camera = data.camera()
# An image with 512 rows
# and 512 columns
type(camera)
print(camera.shape)
print(camera.dtype)


from skimage import io
img = io.imread('applications-of-machine-learning.png')
io.imshow(img)


from skimage import io
import pandas as pd
#Pandas is used to read, write, and process various file formats.
img = io.imread('applications-of-machine-learning.png')
df = pd.DataFrame(img.flatten())
# flatten function is used to convert the three dimensions of an RGB image to a single dimension
#filepath = 'pixel_values1.xlsx'
# DataFrame function converts a one-dimensional array into an Excel-like format, with rows and columns
#df.to_excel(filepath, index=False)
# to_excel save that image in an excel file.
#print(df)
#print(filepath)

# Converting Color Space
# pylab is used to see different figures in different blocks.
# RGB to HSV and Vice Versa
#Import libraries
from skimage import io
from skimage import color
from skimage import data
from pylab import figure
#Read image
img = data.coffee()
#Convert to HSV
img_hsv = color.rgb2hsv(img)
#Convert back to RGB
img_rgb = color.hsv2rgb(img_hsv)
#Show both figures
figure(0)
io.imshow(img_hsv)
figure(1)
io.imshow(img_rgb)


from skimage import io
from skimage import color
from skimage import data
from skimage import transform
#Read image
img = data.horse()

new_img = transform.resize(img,(328,400,3))
#Convert to XYZ
img_xyz = color.rgb2xyz(new_img)
#Convert back to RGB
img_rgb = color.xyz2rgb(img_xyz)
#Show both figures
figure(0)
io.imshow(img_xyz)
figure(1)
io.imshow(img_rgb)

# Saving an Image
#Import libraries
from skimage import io
from skimage import color
#Read image
img = img_rgb
#Convert to YPbPr
img_ypbpr= color.rgb2ypbpr(img)
#Convert back to RGB
img_rgb= color.ypbpr2rgb(img_ypbpr)
io.imsave("horse_ypbpr.jpg", img_ypbpr)


from skimage import exposure
from skimage import io
from pylab import figure
img = data.coffee()
gamma_corrected1 = exposure.adjust_gamma(img, 0.5)
gamma_corrected2 = exposure.adjust_gamma(img, 3)
figure(0)
io.imshow(gamma_corrected1)
figure(1)
io.imshow(gamma_corrected2)


# Rotating, Shifting, and Scaling Images
from skimage import io
from skimage.transform import rotate
img = data.coffee()
img_rot = rotate(img, 90)
io.imshow(img_rot)



















