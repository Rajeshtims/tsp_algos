import numpy as np
from tspInstances import *
import time

def two_opt(route, cost_matrix):
     best = route
     improved = True
     while improved:
          improved = False
          for i in range(1, len(route)-2):
               for j in range(i+1, len(route)):
                    if j-i == 1: continue
                    new_route = route[:]
                    new_route[i:j] = route[j-1:i-1:-1] #
                    if cost(cost_matrix, new_route) < cost(cost_matrix, best):
                         best = new_route
                         improved = True
          route = best
     return best

def cost(cost_mat, route):
   return cost_mat[np.roll(route, 1), route].sum()

def nearest_neighbor_tsp(distance_matrix):
    nodes = distance_matrix.shape[0]
    unvisited_nodes = set(range(nodes))
    path = []
    
    current_node = np.random.choice(nodes)
    path.append(current_node)
    unvisited_nodes.remove(current_node)
    
    while unvisited_nodes:
        nearest_node = min(unvisited_nodes, key=lambda city: distance_matrix[current_node][city])
        path.append(nearest_node)
        current_node = nearest_node
        unvisited_nodes.remove(nearest_node)
    
    path.append(path[0])
    
    return path

def main():
     cost_mat = np.array([
          [0, 5, 2, 7, 1, 4, 7, 2, 2, 7], 
          [5, 0, 1, 5, 4, 10, 6, 6, 4, 4], 
          [2, 1, 0, 6, 8, 6, 6, 4, 6, 5], 
          [7, 5, 6, 0, 8, 3, 5, 5, 10, 4], 
          [1, 4, 8, 8, 0, 6, 3, 4, 4, 5], 
          [4, 10, 6, 3, 6, 0, 6, 8, 2, 1], 
          [7, 6, 6, 5, 3, 6, 0, 4, 2, 5], 
          [2, 6, 4, 5, 4, 8, 4, 0, 3, 5], 
          [2, 4, 6, 10, 4, 2, 2, 3, 0, 8], 
          [7, 4, 5, 4, 5, 1, 5, 5, 8, 0]
     ])
     tsp_instances = [graph5Nodes, graph6Nodes, graph7Nodes, graph8Nodes, graph9Nodes, graph10Nodes, graph11Nodes, graph12Nodes, graph13Nodes, graph50nodes, graph75Nodes, graph100Nodes]
     nodes = [5,6,7,8,9,10, 11, 12, 13, 50, 75, 100]

     for cost_mat in tsp_instances:
          cost_mat = np.asarray(cost_mat)
          start = time.time()
          route = nearest_neighbor_tsp(cost_mat)
          end = time.time()
          print(route)
          print(f'nearest neighbor tsp. time = {end - start}')
          
          start = time.time()
          best_route = two_opt(route,cost_mat)
          # result = two_opt(route, cost_mat)
          end = time.time()
          print(f'2-OPT tsp. time = {end - start}')

          print(cost(cost_mat,best_route))
          print('-'*50)


if __name__=='__main__':
    main()