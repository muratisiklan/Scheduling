from src.Problems.cvrp.cvrp import CapacitatedVehicleRouting
from src.Problems.cvrp.Algorithms.utils import (calculate_total_cost,
                                                find_value_index,
                                                create_neighbor_solution,
                                                create_init_population)
import copy
import random


class GeneticAlgorithm(CapacitatedVehicleRouting):
    def __init__(self, distance_matrix, demands, vehicle_capacities) -> None:
        super().__init__(distance_matrix, demands, vehicle_capacities)

    def _eval_fitness(self):
        fitness: list = []
        for i in range(len(self.population)):
            fitness.append(calculate_total_cost(
                self.population[i], self.distance_matrix, self.demands, self.vehicle_capacities)[0])

        return fitness

    def _selection(self, fitness: list, selection_algorithm: str = None):
        # Roulette wheel selection

        # select best 2 solutions
        sorted_indexes = sorted(
            range(len(fitness)), key=lambda k: fitness[k])
        return tuple(sorted_indexes[:2])

    @staticmethod
    def _crossover(parent1, parent2):
        # Interesting crossover methodology?

        p1 = copy.deepcopy(parent1)
        p2 = copy.deepcopy(parent2)

        n_nodes = sum(len(row) for row in p1)

        num_nodes_inserted = random.randint(1, n_nodes - 1)
        nodes_to_inserted = random.sample(
            range(1, n_nodes), num_nodes_inserted)
        # print(nodes_to_inserted)
        # print("----------------")
        # print(p1)
        for i in nodes_to_inserted:
            row1, column1 = find_value_index(p1, i)
            row2, column2 = find_value_index(p2, i)

            p2[row2].pop(column2)
            p2[row1].insert(column1, i)

        return p2


    def generate_population(self, parent1, parent2, population_size, mutation_prob):
        population = []
        while population_size > 0:
            child = copy.deepcopy(self._crossover(parent1, parent2))
            if random.random() <= mutation_prob:
                mutated_child = create_neighbor_solution(child)
                population.append(mutated_child)
            else:
                population.append(child)

            population_size -= 1
        return population

    def solve(self, n_iter=100, generation_size=100, mutation_prob=1):
        self.population = create_init_population(
            self.distance_matrix, self.demands, self.vehicle_capacities, generation_size)
        global_best_solution = self.population[0]
        global_best_obj = calculate_total_cost(
            global_best_solution, self.distance_matrix, self.demands, self.vehicle_capacities)[0]

        objectives = []
        while n_iter > 0:
            fitness = self._eval_fitness()
            p1_idx, p2_idx = self._selection(fitness)

            parent1 = self.population[p1_idx]
            parent2 = self.population[p2_idx]
            candidate_solution_obj = calculate_total_cost(
                parent1, self.distance_matrix, self.demands, self.vehicle_capacities)[0]
            if candidate_solution_obj < global_best_obj:
                global_best_solution = copy.deepcopy(parent1)
                global_best_obj = candidate_solution_obj
            self.population = self.generate_population(
                parent1, parent2, generation_size, mutation_prob)
            objectives.append(global_best_obj)
            n_iter -= 1

        obj, load_each_vehicle, final_sol = calculate_total_cost(
            global_best_solution, self.distance_matrix, self.demands, self.vehicle_capacities)

        self.final_solution = final_sol
        self.final_total_objective_value = obj
        self.objective_change_iteration = objectives
        self.vehicle_loads = load_each_vehicle

        return final_sol, obj, objectives, load_each_vehicle
