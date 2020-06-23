import os, sys, io, string, random, time, math
from functools import partial
from enum import Enum, auto

class SelectionType(Enum):  
    ROULETTE = auto()
    TOURNAMENT = auto()

def read_distances(path: str):
    with open(path, "r") as stream:
        list_size = int(stream.readline())
        distance_list = [[0 for x in range(list_size)] for y in range(list_size)]
        for i, line in enumerate(stream):
            spl_line = line.strip().split(" ")
            for j, number in enumerate(spl_line):
                distance_list[i][j] = int(number)
                if distance_list[j][i] is None or distance_list[j][i] == 0:
                    distance_list[j][i] = int(number)
    return distance_list

# population represents order, in which salesman will travel between cities
def create_population(source: list, size=100):
    population = [[i for i in range(len(source))] for j in range(size)]
    for chromosome in population:
        random.shuffle(chromosome)
    return population

# by default fitness function assigns scores from 0 to 1, perhaps increasing weight would be good
def fitness_function_roulette(population: list, distance_list: list):
    distances = []
    ratings = []
    for chromosome in population:
        distance = sum(distance_list[chromosome[i-1]][chromosome[i]] for i in range(1, len(chromosome)))
        distances.append(distance)
    max_dist = max(distances)
    min_dist = min(distances)
    for distance in distances:
        if max_dist - min_dist == 0:
            ratings.append(1.0)
            break
        else:
            if distance - min_dist == 0:
                inverted_rating = 1 / (max_dist - min_dist)
            else:
                inverted_rating = (distance - min_dist) / (max_dist - min_dist)
            ratings.append(round(1 / inverted_rating * 10, 2))
    return ratings

def fitness_function_tournament(population: list, distance_list: list):
    distances = []
    sorted_distances = []
    ratings = []
    for chromosome in population:
        distance = sum(distance_list[chromosome[i-1]][chromosome[i]] for i in range(1, len(chromosome)))
        distances.append(distance)
    for i, value in enumerate(distances):
        sorted_distances.append((i, value))
        sorted_distances = sorted(sorted_distances, key= lambda x: x[1])
    ratings.append()
    return []

def selection(population: list, distance_list: list, selection_type: SelectionType = SelectionType.ROULETTE):
    if selection_type == SelectionType.ROULETTE:
        ratings = fitness_function_roulette(population, distance_list)
    elif selection_type == SelectionType.TOURNAMENT:
        ratings = fitness_function_tournament(population, distance_list)
    fitness_scores_sum = sum(rating for rating in ratings)

    # saving best element | elitism in practice
    best_element = population[max(range(len(ratings)), key=ratings.__getitem__)]
    best_outcome = sum(distance_list[best_element[i-1]][best_element[i]] for i in range(1, len(best_element)))
    print(f"Best outcome: {best_outcome}")
    new_population = [best_element]

    for __ in range(len(population) - 1):
        preceding_fitness_scores_sum = 0
        selection_point = random.uniform(0, fitness_scores_sum)
        for i, rating in enumerate(ratings):
            preceding_fitness_scores_sum += rating
            # following line means that selection point is in bucket of this chromosome
            if preceding_fitness_scores_sum >= selection_point:
                new_population.append(population[i])
                break
    return new_population

def crossover_single_point(population: list, crossover_chance: int = 80):
    new_population = []
    for crossover_subject in population:
        if random.randrange(100) < crossover_chance:
            crossover_target = population[random.randrange(len(population))]
            crossover_point = random.randrange(len(crossover_subject))
            chromosome = crossover_subject[0:crossover_point]
            for gene in crossover_target:
                if gene not in chromosome:
                    chromosome.append(gene)
            new_population.append(chromosome)
        else:
            new_population.append(crossover_subject)
    return new_population

# zamienia miejscami dwa geny
def mutation_permutation(population: list, permutation_chance: int = 5):
    new_population = population.copy()
    for i, chromosome in enumerate(population):
        if random.randrange(100) < permutation_chance:
            fir_pt = random.randrange(len(chromosome))
            sec_pt = random.randrange(len(chromosome))
            new_population[i][fir_pt], new_population[i][sec_pt] = new_population[
                i][sec_pt], new_population[i][fir_pt]
    return new_population

def evolve(population: list, distance_list: list, generations_quantity: int):
    for __ in range(generations_quantity):
        # print(f"Generation {i}")
        population = selection(population, distance_list, SelectionType.ROULETTE)
        population = crossover_single_point(population)
        population = mutation_permutation(population, 5)
    return population


input_file_path = os.path.dirname(sys.argv[0]) + r"\data\berlin52.txt"
distance_list = read_distances(input_file_path)
population = create_population(distance_list, 40)
population = evolve(population, distance_list, 50000)

pass