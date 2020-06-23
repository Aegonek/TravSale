import os, sys, io, string, random
from functools import partial

def load_dist_arr(path: str):
    with open(path, "r") as stream:
        arr_dim = int(stream.readline())
        dist_arr = [[0 for x in range(arr_dim)] for y in range(arr_dim)]
        for i, line in enumerate(stream):
            spl_line = line.strip().split(" ")
            for j, number in enumerate(spl_line):
                dist_arr[i][j] = int(number)
                if dist_arr[j][i] is None or dist_arr[j][i] == 0:
                    dist_arr[j][i] = int(number)
    return dist_arr

def create_population(dist_arr: list, size=100):
    population = [[i for i in range(len(dist_arr))] for j in range(size)]
    for chromosome in population:
        random.shuffle(chromosome)
    return population

# returns tuple of a chromosome and a fitness score
def fitness_function(chromosome: list, dist_arr: list):
    dist_sum = sum(dist_arr[chromosome[i-1]][chromosome[i]] for i in range(1, len(chromosome)))
    fit_score = 30000/dist_sum
    return (chromosome, fit_score)

def roulette_selection(old_population: list):
    # print("Selecting")
    fit_sum = sum(fit_score for chromosome, fit_score in old_population)
    new_population = []
    for __ in range(100):
        temp = 0
        rnd = random.uniform(0, fit_sum)
        for chr, value in old_population:
            temp += value
            if temp >= rnd:
                new_population.append(chr)
                break
    return new_population

def crossover_one_point(population: list):
    # print("Crossovering")
    new_population = []
    for chromosome in population:
        crossover_target = population[random.randrange(len(population))]
        crossover_point = random.randrange(len(chromosome))
        # swap this shit to generator expression
        new_chromosome = chromosome[0:crossover_point]
        for gene in crossover_target:
            # change to ternary operator
            if gene not in new_chromosome:
                new_chromosome.append(gene)
        new_population.append(new_chromosome)
    return new_population

def mutation_by_permutation(old_population: list):
    # print("Mutating")
    new_population = old_population.copy()
    for index, chromosome in enumerate(old_population):
        if random.randrange(100) < 5:
            # swaps two variables in a chromosome
            new_population[index][second_point], new_population[index][first_point] = new_population[index][(
                    first_point := random.randrange(len(chromosome)))], new_population[index][(
                    second_point := random.randrange(len(chromosome)))]
            # print(f"Made a mutation between [{first_point}] and [{second_point}]")
    return new_population

def iterate_gen(population: list, dist_arr: list, generation_qty: int = 300):
    for i in range(generation_qty):
        print(f"Generation {i+1}")
        # print("Evaluating fitness")
        population = list(map(partial(fitness_function, dist_arr=dist_arr), population))
        population = sorted(population, key=lambda tup: tup[1], reverse=True)
        population = roulette_selection(population)
        population = crossover_one_point(population)
        population = mutation_by_permutation(population)
    population = list(map(partial(fitness_function, dist_arr=dist_arr), population))
    population = sorted(population, key=lambda tup: tup[1], reverse=True)
    return population

# # ooc algen
# # gotta make better tests
# dir = os.path.dirname(sys.argv[0]) + r"\data\berlin52.txt"
# dist_arr = load_dist_arr(dir)
# population = create_population(dist_arr)
# # population = list(map(partial(fitness_function, dist_arr=dist_arr), population))
# # population = sorted(population, key=lambda tup: tup[1])
# # population = roulette_selection(population)
# # population = crossover_one_point(population)
# # population = mutation_by_permutation(population)
# population = iterate_gen(population, dist_arr, 10000)
# print(f"""List of cities: {population[0][0]}; Distance: {sum(
#         dist_arr[population[0][0][i-1]][population[0][0][i]] for i in range(1, len(population[0][0])))}""")
# pass
