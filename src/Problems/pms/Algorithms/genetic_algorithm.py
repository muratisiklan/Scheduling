from src.Problems.pms.pms import ParallelMachineScheduling
from src.Problems.pms.Algorithms.utils import (calculate_tardiness,
                                               create_initial_solution,
                                               create_population)
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
    def _selection(self,fitness):
        #Roulette wheel selection
        total_fitness = sum(fitness)
        selection_probabilities = [fitness / total_fitness for fitness in fitness]

        # Select two parents' indexes using roulette wheel selection
        selected_parents_indexes = random.choices(range(len(self.population)), weights=selection_probabilities, k=2)

        return selected_parents_indexes
    

        #Tournament selection
        #Boltzman Selection

    def solve(self,init_pop_size=100):
        self.population = create_population(self.process_times,init_pop_size)
        fitness = self._eval_fitness(self.population)
        parent_idx = self._selection(fitness)
