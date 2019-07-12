#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 10:31:08 2018

@author: hiteshsapkota
"""

import numpy
import sys
import math
import random
import queue as Q

width=395
height=500
NO_POINTS=5
min_slope = -1.3536635761589395
max_slope = 1.3536635761589395




TERRIAN_COLORS={'#F89412': 'A', '#FFC000': 'B', '#FFFFFF': 'C',\
                '#02D03C': 'E', '#028828': 'F', '#054918': 'G',\
                '#0000FF': 'H', '#473303': 'K', '#000000': 'M',\
                '#CD0065':'O'}
               
TERRIAN_FACTORS={'A': 4, 'B': 0.5, 'C': 2.5, 'D': 2.5, 'E': 2, 'F': 1, \
                'G':0, 'H':0, 'I': 0, 'J': 0, 'K': 4, 'L': 4, 'M': 3, 'N':3, 'O': 0}





def comp_slope(elev_current, elev_success, distance):

    
    return float(elev_current-elev_success)/float(distance)

def find_slope(elevation_matrix, succ_point, curr_point):
    succ_j=succ_point%width
    succ_i=int(succ_point/width)
    curr_j=curr_point%width
    curr_i=int(curr_point/width)
    eucl_dist=numpy.sqrt((7.55*(succ_i-curr_i))**2+(10.29*(succ_j-curr_j))**2)
    slope=comp_slope(elevation_matrix[curr_i][curr_j], elevation_matrix[succ_i][succ_j], eucl_dist) 
    slope=(slope-min_slope)/(max_slope-min_slope)
    return slope

def find_path(child_parent_map, source, state, path):
    if state==source:
        path.append(state)
        path.reverse()
        return path
    parent=child_parent_map[state]
    path.append(state)
    
    return find_path(child_parent_map, source, parent, path )

def find_gn(pixel_matrix, elevation_matrix, prev_cost, curr_point, succ_point):
    succ_j=succ_point%width
    succ_i=int(succ_point/width)
    curr_j=curr_point%width
    curr_i=int(curr_point/width)
    eucl_dist=numpy.sqrt((7.55*(succ_i-curr_i))**2+(10.29*(succ_j-curr_j))**2)
    color=pixel_matrix[succ_i][succ_j]
    terrian_factor=TERRIAN_FACTORS[TERRIAN_COLORS[color]]
    slope=find_slope(elevation_matrix, succ_point, curr_point)
    speed=1.388*terrian_factor*slope
    if speed==0:
        total_cost=math.inf
    else:
        total_cost = (eucl_dist/speed + prev_cost)
    return total_cost

def find_hn(pixel_matrix, elevation_matrix, successor, destination):
    curr_j=successor%width
    curr_i=int(successor/width)
    dest_i=destination[1]
    dest_j=destination[0]
    
    
    eucl_dist=numpy.sqrt((7.55*(dest_i-curr_i))**2+(10.29*(dest_j-curr_j))**2)
    color=pixel_matrix[curr_i][curr_j]
    
    if curr_i<=dest_i:
       if abs(curr_i-dest_i)>NO_POINTS:
           i_candidates=random.sample(list(range(curr_i, dest_i+1)), NO_POINTS)
       else:
            i_candidates=list(range(curr_i, dest_i+1))
    else:
        if abs(curr_i-dest_i)>NO_POINTS:
            i_candidates=random.sample(list(range(curr_i, dest_i+1, -1)), NO_POINTS)
        else:
            if curr_i==(dest_i+1):
                 i_candidates=[curr_i]
            else:
                i_candidates=list(range(curr_i, dest_i+1, -1))
    
    if curr_j<=dest_j:
       if abs(curr_j-dest_j)>NO_POINTS:
           j_candidates=random.sample(list(range(curr_j, dest_j+1)), NO_POINTS)
       else:
            j_candidates=list(range(curr_j, dest_j+1))
    else:
        if abs(curr_j-dest_j)>NO_POINTS:
            j_candidates=random.sample(list(range(curr_j, dest_j+1, -1)), NO_POINTS)
        else:
            if curr_j==(dest_j+1):
                 j_candidates=[curr_j]
            else:
                j_candidates=list(range(curr_j, dest_j+1, -1))
            
            
    terrian_factors=[]
    slopes=[]
    for i in range(0, len(i_candidates)):
        i_candidate=i_candidates[i]
        for j in range(0, len(j_candidates)):
           
            
            j_candidate=j_candidates[j]
           
            color=pixel_matrix[i_candidate][j_candidate]
            
            if i_candidate*width+j_candidate!=successor:
                
                slope=find_slope(elevation_matrix, i_candidate*width+j_candidate, successor)
                slopes.append(slope)
            if TERRIAN_COLORS[color]=='O':
                continue
            terrian_factor=TERRIAN_FACTORS[TERRIAN_COLORS[color]]
            terrian_factors.append(terrian_factor)
           
            
    color=pixel_matrix[curr_i][curr_j]
    terrian_factor=TERRIAN_FACTORS[TERRIAN_COLORS[color]]
    
    try:
     terrian_factor=numpy.max(terrian_factors)
     slope=numpy.max(slopes)
    except ValueError:
     slope=1
     terrian_factor=TERRIAN_FACTORS[TERRIAN_COLORS[color]]
   
   
    speed=1.388*terrian_factor*slope
    if speed==0:
        return math.inf
    return eucl_dist/speed


def find_succ_location(current_pixel, pixel_matrix):
    curr_j=current_pixel%width
    curr_i=int(current_pixel/width)
    successors=[]
    for i in [-1, 0,  1]:
        for j in [-1, 0,  1]:
            if i==0 and j==0:
                continue
            next_pixel=(curr_i+i)*width+(curr_j+j)
            if next_pixel<0 or next_pixel>(width*height-1):
                continue
            successors.append(next_pixel)
    return successors

def outofbound(successor, pixel_matrix):
    j=successor%width
    i=int(successor/width)
    color=pixel_matrix[i][j]
    if TERRIAN_COLORS[color]=='O':
        return True
    else:
        return False
    
def impassable(successor, pixel_matrix):
    j=successor%width
    i=int(successor/width)
    color=pixel_matrix[i][j]
    terrian_factor=TERRIAN_FACTORS[TERRIAN_COLORS[color]]
    if terrian_factor==0:
        return True
    else:
        return False
    
    
def Aastricsearch(pixel_matrix, elevation_matrix, source, destination):
    q = Q.PriorityQueue()
    child_parent_map={}
    pixel_actual_cost={}
    source_1d=source[0]+source[1]*width
    destination_1d=destination[0]+destination[1]*width
    g_n=0
    h_n=find_hn(pixel_matrix, elevation_matrix, source_1d, destination)
    f_n=g_n+h_n
    pixel_actual_cost[source_1d]=0
    q.put((f_n, source_1d))
    iter_count = 0
    while not q.empty():
        iter_count += 1
        curr_pixel=q.get()
        if curr_pixel[1]==destination_1d:
           return [curr_pixel[0], find_path(child_parent_map, source_1d, destination_1d, [])]
        successors=find_succ_location(curr_pixel[1], pixel_matrix)
        for successor in successors:
            
            if outofbound(successor, pixel_matrix):
                continue
            if impassable(successor, pixel_matrix):
                continue
            
                
            g_n=find_gn(pixel_matrix, elevation_matrix, pixel_actual_cost[curr_pixel[1]], curr_pixel[1], successor)
            h_n=find_hn(pixel_matrix, elevation_matrix,  successor, destination)
            f_n=g_n+h_n
            
            if curr_pixel[1] in child_parent_map:
                if successor==child_parent_map[curr_pixel[1]]:
                    continue
            if successor in child_parent_map:
                if pixel_actual_cost[successor]>g_n:
                    child_parent_map[successor]=curr_pixel[1]
                    pixel_actual_cost[successor]=g_n
                continue
            child_parent_map[successor]=curr_pixel[1]
            pixel_actual_cost[successor]=g_n
            q.put((f_n, successor))
            
            
    return "Not found the path"


    
  
def optimal_path(source, destination, pixel_matrix, elevation_matrix): 
    source_color=pixel_matrix[source[1]][source[0]]
    source_terrian_factor=TERRIAN_FACTORS[TERRIAN_COLORS[source_color]]
    dest_color=pixel_matrix[destination[1]][destination[0]]
    dest_terrian_factor=TERRIAN_FACTORS[TERRIAN_COLORS[dest_color]]
    if source_terrian_factor==0 or dest_terrian_factor==0:
        print("Either source or destination is impassable")
        sys.exit(1)
    else:
        path_pixels = Aastricsearch(pixel_matrix, elevation_matrix, source, destination)
        return path_pixels

    

