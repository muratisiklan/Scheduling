from src.Problems.pms.pms import ParallelMachineScheduling
from src.Problems.pms.Algorithms.utils import (calculate_tardiness,
                                               create_population,
                                               find_value_index,
                                               create_neighbor_solution)
import random
import copy


class GeneticAlgorithm(ParallelMachineScheduling):
    def __init__(self, process_times, ready_times, due_dates, setup_times) -> None:
        super().__init__(process_times, ready_times, due_dates, setup_times)

    def _eval_fitness(self):
        fitness: list = []
        for i in range(len(self.population)):
            fitness.append(calculate_tardiness(
                self.population[i], self.process_times, self.due_dates, self.ready_times, self.setup_times)[0])

        return fitness

    def _selection(self, fitness: list, selection_algorithm: str = "roulette_wheel"):
        # Roulette wheel selection
        if selection_algorithm == "roulette_wheel":
            total_fitness = sum(fitness)
            selection_probabilities = [
                1 / (value / total_fitness) for value in fitness]

            # Select two parents' indexes using roulette wheel selection
            selected_parents_indexes = random.choices(
                range(len(self.population)), weights=selection_probabilities, k=2)

            return selected_parents_indexes
        else:
            sorted_indexes = sorted(
                range(len(fitness)), key=lambda k: fitness[k])
            return tuple(sorted_indexes[:2])

        # Tournament selection
        # Boltzman Selectiong
    @staticmethod
    def _crossover(parent1, parent2):

        p1 = copy.deepcopy(parent1)
        p2 = copy.deepcopy(parent2)

        n_jobs = sum(len(row) for row in parent1)


        num_jobs_inserted = random.randint(0, n_jobs-1)
        jobs_to_inserted = random.sample(range(n_jobs), num_jobs_inserted)
        for i in jobs_to_inserted:
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
        self.population = create_population(
            self.process_times, generation_size)
        global_best_solution = self.population[0]
        global_best_obj = calculate_tardiness(
            global_best_solution, self.process_times, self.due_dates, self.ready_times, self.setup_times)[0]

        objectives = []
        while n_iter > 0:
            fitness = self._eval_fitness()
            p1_idx,p2_idx = self._selection(fitness)
            parent1 = self.population[p1_idx]
            parent2 = self.population[p2_idx]
            candidate_solution_obj = calculate_tardiness(
                parent1, self.process_times, self.due_dates, self.ready_times, self.setup_times)[0]
            if candidate_solution_obj < global_best_obj:
                global_best_solution = copy.deepcopy(parent1)
                global_best_obj = candidate_solution_obj
            self.population = self.generate_population(
                parent1, parent2, generation_size, mutation_prob)
            objectives.append(global_best_obj)
            n_iter -= 1

        obj, seq, compt, stime = calculate_tardiness(
            global_best_solution, self.process_times, self.due_dates, self.ready_times, self.setup_times)

        self.final_solution = seq
        self.final_total_objective_value = obj
        self.objective_change_iteration = objectives
        self.final_compt = compt
        self.final_stime = stime

        return seq, obj, objectives, compt, stime
