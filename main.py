#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 03:19:09 2018

@author: hiteshsapkota
"""

import sys
from PIL import Image
from colormap import rgb2hex
from colormap import hex2rgb
from travelling_salesman import held_karp
import numpy
import time as t
from own_optimal_path import optimal_path as optimal_path_own
from own_optimal_path import find_hn as find_hn_own
from other_optimal_path import optimal_path as optimal_path_other
from other_optimal_path import find_hn as find_hn_other


width=395
height=500
   
    
"""Read the image from the file"""
def readimage():
    im=Image.open("Dataset/terrain.png")
    [width, height]=im.size
    RGBA_pixel=im.load()
    HEX_pixel=[]
    for i in range(0, height):
        row_data=[]
        for j in range(0, width):
            r=RGBA_pixel[j, i][0]
            g=RGBA_pixel[j, i][1]
            b=RGBA_pixel[j, i][2]
            row_data.append(rgb2hex(r, g, b))
        HEX_pixel.append(row_data)
            
    return HEX_pixel

"""Read the elevation data """
def readelevation():
    elevation_matrix = numpy.zeros(shape=(height, width))
    elevation_file=open("dataset/mpp.txt")
    i=0
    for line in elevation_file:
        elevations = line.split()
        for j in range(0, width):
            elevation_matrix[i][j]=elevations[j]
        i+=1
    return elevation_matrix


def displayimage(path_pixels, control_points_1d):
    if path_pixels=="Not found the path":
        print("Sorry Unable to find the path")
        return 0
    im=Image.open("dataset/terrain.png")
    pixelMap = im.load()
    img = Image.new(im.mode, im.size)
    pixelsNew = img.load()
     
        
    for i in range(img.size[1]):
        for j in range(img.size[0]):
            pixelsNew[j,i] = pixelMap[j,i]
    for pixel in  path_pixels:
        
            
        j=pixel%width
        i=int(pixel/width)
        if pixel in control_points_1d:
           
            rgb=hex2rgb('#000000')
        else:
            rgb=hex2rgb('#FF0000')
        pixelsNew[j,i]=(rgb[0], rgb[1], rgb[2], 255)
    img.show()       
    

"""Read the controls from the data"""
def readpoints(file, file_type):
    if file_type=='c':
        control_points=[]
        i=0
        for line in file:
            points=line.split()
            control_points.append((int(points[0]), int(points[1])))
            i+=1
        return control_points
    elif file_type=='s':
        control_points=[]
        i=0
        for line in file:
           
            if i==0:
            
                points=line.split()
               
                time=float(points[0])
                i+=1
                
                continue
            points=line.split()
            control_points.append((int(points[0]), int(points[1])))
            i+=1
        return [control_points, time]

"""2D to 1D conversion"""
def twodto1d(points):
    control_points_1d=[]
    for i in range(0, len(points)):
        x=points[i][0]
        y=points[i][1]
        control_points_1d.append(x+y*width)
    return control_points_1d


if __name__== "__main__":
    
    if len(sys.argv)!=3:
        print("Either file name or path cost type is missing")
        sys.exit (1)
   
    else:
        
        file_name=sys.argv[1]
        path_cost_type=sys.argv[2]
        if path_cost_type=='own':
            optimal_path=optimal_path_own
            find_hn=find_hn_own
        else:
            optimal_path=optimal_path_other
            find_hn=find_hn_other
            
        file=open("dataset/"+file_name)
        pixel_matrix=readimage()
        elevation_matrix=readelevation()
        for line in file:
            event_type=line.split()[0]
            break
        if event_type=="Classic":
            start_time=t.time()
            print("Working on the classic type")
            control_points=readpoints(file, 'c')
            path_pixels=[]
            control_points_1d=twodto1d(control_points)
            total_cost=0
            for i in range(0, len(control_points)-1):
                [cost, path]=optimal_path(control_points[i], control_points[i+1], pixel_matrix, elevation_matrix)
                path_pixels+=path
                total_cost+=cost
            finish_time=t.time()
            print("Path cost:", total_cost)
            print("Exectuion time:", (finish_time-start_time))
            
            
            displayimage(path_pixels, control_points_1d)
            
            
        elif event_type=="ScoreO":
            start_time=t.time()
            print("Working on the ScoreO")
            control_points, time_limit=readpoints(file, 's')
            path_pixels=[]
            control_points_1d=twodto1d(control_points)
            no_control_points=len(control_points_1d)
            A=numpy.zeros((no_control_points, no_control_points))
            for i in range(0, no_control_points):
                for j in range(0, no_control_points):
                    if i==j:
                        A[i][j]=0
                    else:
                        A[i][j]=find_hn(pixel_matrix, elevation_matrix, control_points_1d[i], control_points[j])
            index_control_points=held_karp(A)[1]
            sequence_points=[]
            for index_point in index_control_points:
                sequence_points.append(control_points[index_point])
            sequence_points.append(control_points[0])
            print("Sequence Points:", sequence_points)
            total_cost=0
            
            for i in range(0, len(sequence_points)-1):
               [cost, path]=optimal_path(sequence_points[i], sequence_points[i+1], pixel_matrix, elevation_matrix)
               path_pixels+=path
               total_cost+=cost
            finish_time=t.time()
            if (total_cost>time_limit):
                print("Sorry unable to find the path within the given time limit")
            else:
                print("Path cost:", total_cost)
                print("Time Limit:", time_limit)
                print("Execution time:", (finish_time-start_time))
                displayimage(path_pixels, control_points_1d)
            
            
        else:
            print("Unknown file type")
        
            
        
