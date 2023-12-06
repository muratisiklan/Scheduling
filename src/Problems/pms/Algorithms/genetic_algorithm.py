from src.Problems.pms.pms import ParallelMachineScheduling
from src.Problems.pms.Algorithms.utils import (calculate_tardiness,
                                               create_initial_solution,
                                               create_population,
                                               find_value_index)
import random


class GeneticAlgorithm(ParallelMachineScheduling):
    def __init__(self, process_times, ready_times, due_dates, setup_times) -> None:
        super().__init__(process_times, ready_times, due_dates, setup_times)

    def _eval_fitness(self):
        fitness: list = []
        for i in range(len(self.population)):
            fitness.append(calculate_tardiness(
                self.population[i], self.process_times, self.due_dates, self.ready_times, self.setup_times)[0])

        return fitness

    def _selection(self, fitness: list, selection_algorithm: str):
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
            return sorted_indexes[:2]

        # Tournament selection
        # Boltzman Selection

    def _crossover(self, paren1, parent2):

        n_jobs = len(self.process_times)
        n_machines = len(self.process_times[0])
        child = [[] for i in range(n_jobs)]

        for i in range(n_jobs):
            rand = random.random()
            if rand < 0.5:
                curr_i, curr_j = find_value_index(paren1, i)

    def solve(self, init_pop_size=100):
        self.population = create_population(self.process_times, init_pop_size)
        fitness = self._eval_fitness(self.population)
        parent_idx = self._selection(fitness)
