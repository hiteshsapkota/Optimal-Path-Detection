# Optimal-Path-Detection
Determines the optimal path between source and target using A* search and Held-Karp algorithm
The project consisits of two tasks: (1) Classic Event and (2) Score-O Event. In each task, we have to determine the optimal path from source to the destination. 
# Task Description:
## Classic Event:
   In this case, we have a number of controls and we need to visit them in the sequence. Our objective is to find an optimal path between given pair of control points.
   
## Score-O Event:
In case of the Score-O event, we can visit the given controls in any order but we need to make sure that we return to the origin in a most optimal way. This is also regarded as a travelling salesman problem

# Data Description:
We have two inputs. First one is a map (terrain.png), dimension of 395 × 500, with the appropriate color values according to the pixel coordinates. Second one (mpp.txt) is a text representation of the elevation corresponding to each pixel in the map.
Map has different obstacle types and are distinguished by the color [CLICK HERE FOR THE INFORMATION](https://www.cs.rit.edu/~zjb/courses/630-2181/lab1/index.html).

For the terrain factor refer to the writup.pdf file

For the Classic event testing, we are given a three text ﬁles: white, brown, and red. Each file has a 'classic' text in the first line. From the second line set of control points are provided in the form of (x, y).
Similarly, for the Score-O, we are given two ﬁles: control points corresponding to a nice hilly area (eastesker.txt), and the control points representing all over the park (allpark.txt). Each file has: (1) 'ScoreO' text in the first line, (2) maximum allowed time (ms) in the second line, and (3) sequence of control points to be visited starting from the third line.

# Approach
  ## Classic Event: 
     In this case, we use A* search which computes the total cost as:
      f(n) = g(n)+h(n); 
      where g(n) is cost from source to destination 
      h(n) is heuristic estimated cost function from given point to destination
      Detail calculation of each parameter is described in a writeup 
   ## Score-O Event:
      In this case, we use the [Held-Karp algorithm] (https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm)       is the dynamic programming approach to ﬁnd the optimal route  in the given set of points. We ﬁrst compute the               heuristic cost function from the one control point to another. Note that the heuristic cost function is asymmetric           between pair of nodes. Then, we pass the adjacency matrix to the Held-Karp, which returns the optimal sequence of the       control points to visit.After getting the order of the control points to visit, we follow the procedure same as that         of the Classic Event.
      
# Implementation:
 Implementation is performed into the Python3. Imported library includes colormap, sys, queue, PIL, numpy, math, and random.
 It consists of the follwoing python scripts:
  1. other_optimal_path.py:
     It takes the two control points and returns the optimal path pixel values. All the heuristic cost are planned for            someone else (follow writeup for detail)
  2. own_optimal_path.py:
     I is same as that of the other_optimal_path.py except heuristic costs are according to my first planning
  3. travelling_salesman.py:
      Herd-Kard algorithm to determine the order of controls to visit.
      
  To get result execute the following script from the command line:
    python main.py file_name planning_type
    Inputs:
      (1) file_name: name of files containing control points e.g., "white.txt","eastesker.txt"
      (2) planning_type: "own" or "other" tells whehter the path costs are taken according to the original planning or                                 according to the planning for someone else
     Outputs:
     (1) Image of the map with the corresponding optimal path represented by red line. The controls are represnted by the            black lines
     (2) Path cost: Total cost to reach destination (in seconds)
     (3) Execution time (in seconds)
     (4) Time limit (optional only in Score-O)
     (5)Sequence points (optional only in Score-O): The sequence of controls to visit (output from the Herd-Kard algorithm)
    
 





 
