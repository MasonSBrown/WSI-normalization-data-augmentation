"""
Tilizing WSI images
"""

from openslide import open_slide
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import tifffile as tiff
from time import sleep

#I named the file which I kept the first image in as rawimages 
#if you would like to run this code you should change the path ***
slide = open_slide("/Users/Mason/github/MasonSBrown/WSI-normalization-data-augmentation/rawimages/MIDOG2022IMG1")

# #Quick Thumbnail of slides
# thumbnail = slide.get_thumbnail((slide.dimensions[0] // 256, slide.dimensions[1] // 256))
# thumbnail.show()

# #Get the properties of the slide
# slide_props = slide.properties
# print(slide_props)

from normalizingslides import norm_HnE

#Img 1 has dimensions of 130304 width by 247552 height

#read_region: (x = pixel you want to focus on, y = magnification level, z is the size of the region)
smaller_region = slide.read_region((65150,123750), 0, (1024,1024))
smaller_region_KGB = smaller_region.convert("RGB")
smaller_region_np = np.array(smaller_region_KGB)

plt.axis('off')
plt.imshow(smaller_region_np)
# plt.show() 
# ^ prints image of tile if you want to :)



norm_img, H_img, E_img = norm_HnE(smaller_region_np, Io=240, alpha=1, beta=0.15)

plt.figure(figsize=(12, 12))
# plt.axis('off')
plt.subplot(221)
plt.title('Original Image')
plt.imshow(smaller_region_np)
# plt.axis('off')
plt.subplot(222)
plt.title('Normalized Image')
plt.imshow(norm_img)
# plt.axis('off')
plt.subplot(223)
plt.title('H image')
# plt.axis('off')
plt.imshow(H_img)
plt.subplot(224)
plt.title('E image')
# plt.axis('off')
plt.imshow(E_img)
plt.show()

# blank = tiff.imread("TODOinsertblankpathhere!!!")
# norm_img, H_img, E_img = norm_HnE(blank, Io=240, alpha=1, beta=0.15)

# #Function to detect blank tiles and tiles with very minimal information
# #This function can be used to identify these tiles so we can make a decision on what to do with them. 
# #Calculates mean and std dev of pixel values in a tile. 
# def find_mean_std_pixel_value(img_list):
    
#     avg_pixel_value = []
#     stddev_pixel_value= []
#     for file in img_list:
#         image = tiff.imread(file)
#         avg = image.mean()
#         std = image.std()
#         avg_pixel_value.append(avg)
#         stddev_pixel_value.append(std)
        
#     avg_pixel_value = np.array(avg_pixel_value)  
#     stddev_pixel_value=np.array(stddev_pixel_value)
        
#     print("Average pixel value for all images is:", avg_pixel_value.mean())
#     print("Average std dev of pixel value for all images is:", stddev_pixel_value.mean())
    
#     return(avg_pixel_value, stddev_pixel_value)