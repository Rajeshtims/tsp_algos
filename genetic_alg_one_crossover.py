import time
import random
import numpy as np
# from varname import nameof

def create_initial_population(pop_size, num_cities):
    population = []
    for _ in range(pop_size):
        individual = list(range(num_cities))
        random.shuffle(individual)
        population.append(individual)
    return population

# fitness function
def calculate_total_distance(adj_matrix, individual):
    total_distance = 0
    num_cities = len(individual)
    for i in range(num_cities - 1):
        total_distance += adj_matrix[individual[i]][individual[i + 1]]
    total_distance += adj_matrix[individual[-1]][individual[0]]  # Return to the starting city
    return total_distance

def tournament_selection(population, adj_matrix, tournament_size):
    selected = []
    pop_size = len(population)
    for _ in range(pop_size):
        tournament = random.sample(population, tournament_size)
        best_individual = min(tournament, key=lambda x: calculate_total_distance(adj_matrix, x))
        selected.append(best_individual)
    return selected

def ordered_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted([random.randint(0, size - 1) for _ in range(2)])
    child = [-1] * size
    for i in range(start, end + 1):
        child[i] = parent1[i]

    pointer = 0
    for i in range(size):
        if child[i] == -1:
            while parent2[pointer] in child:
                pointer += 1
            child[i] = parent2[pointer]
            pointer += 1
    return child

def swap_mutation(individual):
    size = len(individual)
    idx1, idx2 = sorted([random.randint(0, size - 1) for _ in range(2)])
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

def genetic_algorithm(adj_matrix, num_generations, pop_size, tournament_size, crossover_rate, mutation_rate):
    num_cities = len(adj_matrix)
    population = create_initial_population(pop_size, num_cities)
    
    for gen in range(num_generations):
        selected = tournament_selection(population, adj_matrix, tournament_size)
        next_population = []

        while len(next_population) < pop_size:
            if random.random() < crossover_rate:
                parent1, parent2 = random.sample(selected, 2)
                child = ordered_crossover(parent1, parent2)
                next_population.append(child)
            else:
                individual = random.choice(selected)
                mutated_individual = swap_mutation(list(individual))
                next_population.append(mutated_individual)

        population = next_population

    best_individual = min(population, key=lambda x: calculate_total_distance(adj_matrix, x))
    best_distance = calculate_total_distance(adj_matrix, best_individual)
    return best_individual, best_distance

if __name__ == "__main__":
    from tspInstances import *
    
    num_generations = 1000
    pop_size = 100
    tournament_size = 10
    crossover_rate = 0.8
    mutation_rate = 0.2

    tsp_instances = [graph5Nodes, graph6Nodes, graph7Nodes, graph8Nodes, graph9Nodes, graph10Nodes, graph11Nodes, graph12Nodes, graph13Nodes, graph50nodes, graph75Nodes, graph100Nodes]
    nodes = [5,6,7,8,9,10, 11, 12, 13, 50, 75, 100]

    for i, tsp_instance in enumerate(tsp_instances):
        print(f'instance = {nodes[i]}')
        start = time.time()
        best_route, best_distance = genetic_algorithm(tsp_instance, num_generations, pop_size, tournament_size, crossover_rate, mutation_rate)
        end = time.time()
        print(f'time taken = {end - start}')
        print(f"Best Route: {best_route}")
        print(f"Best Distance: {best_distance}")
        print('-'*50)
