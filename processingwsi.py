"""
Tilizing WSI images
"""

from openslide import open_slide
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import tifffile as tiff
from time import sleep


from openslide.deepzoom import DeepZoomGenerator


slide = open_slide("/Users/Mason/github/MasonSBrown/WSI-normalization-data-augmentation/rawimages/MIDOG2022IMG1")
tiles = DeepZoomGenerator(slide, tile_size=256, overlap=0, limit_bounds=False)

# # # # #Tile non normalized creator

# cols, rows = tiles.level_tiles[16]
# import os
# tile_dir = "/Users/Mason/Pictures/saved_tiles/original_tiles/"
# for row in range(rows):
#     for col in range(cols):
#         tile_name = os.path.join(tile_dir, '%d_%d' % (col, row))
#         print("Now saving tile with title: ", tile_name)
#         temp_tile = tiles.get_tile(16, (col, row))
#         temp_tile_RGB = temp_tile.convert('RGB')
#         temp_tile_np = np.array(temp_tile_RGB)
#         plt.imsave(tile_name + ".tiff", temp_tile_np)


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

# plt.axis('off')

# plt.imshow(smaller_region_np)

# plt.show() 
# ^ prints image of tile if you want to :)


norm_img, H_img, E_img = norm_HnE(smaller_region_np, Io=240, alpha=1, beta=0.15)
# # plt.figure(figsize=(12, 12))
# # plt.axis('off')
# plt.subplot(221)
# plt.title('Original Image')
# # plt.imshow(smaller_region_np)
# # plt.axis('off')
# plt.subplot(222)
# plt.title('Normalized Image')
# # plt.imshow(norm_img)
# # plt.axis('off')
# plt.subplot(223)
# plt.title('H image')
# # plt.axis('off')
# # plt.imshow(H_img)
# plt.subplot(224)
# plt.title('E image')
# # plt.axis('off')
# # plt.imshow(E_img)
# # plt.show()


def find_mean_std_pixel_value(img_list):
    
    avg_pixel_value = []
    stddev_pixel_value= []
    for file in img_list:
        image = tiff.imread(file)
        avg = image.mean()
        std = image.std()
        avg_pixel_value.append(avg)
        stddev_pixel_value.append(std)
        
    avg_pixel_value = np.array(avg_pixel_value)  
    stddev_pixel_value=np.array(stddev_pixel_value)
        
    print("Average pixel value for all images is:", avg_pixel_value.mean())
    print("Average std dev of pixel value for all images is:", stddev_pixel_value.mean())
    
    return(avg_pixel_value, stddev_pixel_value)


import glob

orig_tile_dir_name = "/Users/Mason/Pictures/saved_tiles/original_tiles"

blank_img_list=(glob.glob(orig_tile_dir_name+"blank/*.tif"))
partial_img_list=(glob.glob(orig_tile_dir_name+"partial/*.tif"))
good_img_list=(glob.glob(orig_tile_dir_name+"good/*.tif"))

blank_img_stats = find_mean_std_pixel_value(blank_img_list)
partial_img_stats = find_mean_std_pixel_value(partial_img_list)
good_img_stats = find_mean_std_pixel_value(good_img_list)


# blank = tiff.imread("/Users/Mason/Pictures/saved_tiles/original_tiles0_0_original.tif")
# norm_img, H_img, E_img = norm_HnE(blank, Io=240, alpha=1, beta=0.15)

#Function to detect blank tiles and tiles with very minimal information
#This function can be used to identify these tiles so we can make a decision on what to do with them. 
#Calculates mean and std dev of pixel values in a tile. 


#Generate object for tiles using the DeepZoomGenerator
tiles = DeepZoomGenerator(slide, tile_size=256, overlap=0, limit_bounds=False)
#Here, we have divided our svs into tiles of size 256 with no overlap. 

#The tiles object also contains data at many levels. 
#To check the number of levels
print("The number of levels in the tiles object are: ", tiles.level_count)
print("The dimensions of data in each level are: ", tiles.level_dimensions)
#Total number of tiles in the tiles object
print("Total number of tiles = : ", tiles.tile_count)

###### processing and saving each tile to local directory
cols, rows = tiles.level_tiles[16]

orig_tile_dir_name = "/Users/Mason/Pictures/saved_tiles/original_tiles/"
norm_tile_dir_name = "/Users/Mason/Pictures/saved_tiles/normal_tiles/"
H_tile_dir_name = "/Users/Mason/Pictures/saved_tiles/H_tiles/"
E_tile_dir_name = "/Users/Mason/Pictures/saved_tiles/E_tiles/"

for row in range(rows):
    for col in range(cols):
        tile_name = str(col) + "_" + str(row)
        #tile_name = os.path.join(tile_dir, '%d_%d' % (col, row))
        #print("Now processing tile with title: ", tile_name)
        temp_tile = tiles.get_tile(16, (col, row))
        temp_tile_RGB = temp_tile.convert('RGB')
        temp_tile_np = np.array(temp_tile_RGB)
        #Save original tile
        plt.imsave(orig_tile_dir_name+tile_name + "_original.tiff", temp_tile_np)
        
        if temp_tile_np.mean() < 230 and temp_tile_np.std() > 15:
            print("Processing tile number:", tile_name)
            norm_img, H_img, E_img = norm_HnE(temp_tile_np, Io=240, alpha=1, beta=0.15)
            #Save the norm tile, H and E tiles      
        
            plt.imsave(norm_tile_dir_name+tile_name + "_norm.tiff", norm_img)
            plt.imsave(H_tile_dir_name+tile_name + "_H.tiff", H_img)
            plt.imsave(E_tile_dir_name+tile_name + "_E.tiff", E_img)
            
        else:
            print("NOT PROCESSING TILE:", tile_name)
