from src.Problems.pms.pms import ParallelMachineScheduling
from src.Problems.pms.Algorithms.utils import (create_initial_solution,
                                               create_neighbor_solution,
                                               calculate_tardiness)
import copy
import math
import random


class SimulatedAnnealing(ParallelMachineScheduling):
    def __init__(self, process_times, ready_times, due_dates, setup_times) -> None:
        super().__init__(process_times, ready_times, due_dates, setup_times)
        self._construct_initial_solution()

    def _construct_initial_solution(self):
        self.initial_solution = create_initial_solution(
            len(self.process_times.T[0]),
            len(self.process_times[0]),
            self.process_times
        )

    def solve(self, n_iter=1000, initial_temperature=100, cooling_factor=0.95):
        # maybe energy threshold can be added to terminate if certain objective value achieved
        # Initial solution already created
        temperature = initial_temperature
        objectives = []
        incumbent_solution = copy.deepcopy(self.initial_solution)
        objectives.append(calculate_tardiness(incumbent_solution, self.process_times,
                          self.due_dates, self.ready_times, self.setup_times)[0])
        global_best_solution = copy.deepcopy(incumbent_solution)
        while n_iter > 0:
            # create neighboring solution

            new_sol = create_neighbor_solution(incumbent_solution)

            # Energy of current solution
            incumbent_obj, _, _, _ = calculate_tardiness(
                incumbent_solution, self.process_times, self.due_dates, self.ready_times, self.setup_times)
            # Energy of candidate solution
            new_obj, _, _, _ = calculate_tardiness(
                new_sol, self.process_times, self.due_dates, self.ready_times, self.setup_times)

            delta_e = new_obj - incumbent_obj

            if (delta_e < 0) or (random.random() < math.exp(-delta_e/temperature)):
                incumbent_solution = copy.deepcopy(new_sol)
                incumbent_obj = new_obj

            if calculate_tardiness(incumbent_solution, self.process_times, self.due_dates, self.ready_times, self.setup_times)[0] < calculate_tardiness(global_best_solution, self.process_times, self.due_dates, self.ready_times, self.setup_times)[0]:
                global_best_solution = copy.deepcopy(incumbent_solution)

            temperature *= cooling_factor
            n_iter -= 1

            objectives.append(calculate_tardiness(
                incumbent_solution, self.process_times, self.due_dates, self.ready_times, self.setup_times)[0])

        obj, seq, compt, stime = calculate_tardiness(
            global_best_solution, self.process_times, self.due_dates, self.ready_times, self.setup_times)

        self.final_solution = seq
        self.final__total_objective_value = obj
        self.objective_change_iteration = objectives
        self.final_compt = compt
        self.final_stime = stime

        return seq, obj, objectives, compt, stime
