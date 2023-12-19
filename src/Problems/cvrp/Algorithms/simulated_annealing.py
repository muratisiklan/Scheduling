from src.Problems.cvrp.cvrp import CapacitatedVehicleRouting
from src.Problems.cvrp.Algorithms.utils import (
    calculate_total_cost,
    create_initial_solution,
    create_neighbor_solution
)
import copy
import random
import math


class SimulatedAnnealing(CapacitatedVehicleRouting):
    def __init__(self, distance_matrix, demands, vehicle_capacities) -> None:
        super().__init__(distance_matrix, demands, vehicle_capacities)
        self._construct_initial_solution()

    def _construct_initial_solution(self):
        self.initial_solution = create_initial_solution(
            self.distance_matrix, self.demands, self.vehicle_capacities)

    def solve(self, n_iter=1000, initial_temperature=100, cooling_factor=0.95):

        temperature = initial_temperature
        objectives = []
        incumbent_solution = copy.deepcopy(self.initial_solution)
        objectives.append(calculate_total_cost(
            incumbent_solution, self.distance_matrix, self.demands, self.vehicle_capacities)[0])
        global_best_solution = copy.deepcopy(incumbent_solution)

        while n_iter > 0:
            # create neighboring solution

            new_sol = create_neighbor_solution(incumbent_solution)

            # Energy of current solution
            incumbent_obj, _ = calculate_total_cost(
                incumbent_solution, self.distance_matrix, self.demands, self.vehicle_capacities)
            # Energy of candidate solution
            new_obj, _ = calculate_total_cost(
                new_sol, self.distance_matrix, self.demands, self.vehicle_capacities)

            delta_e = new_obj - incumbent_obj

            if (delta_e < 0) or (random.random() < math.exp(-delta_e/temperature)):
                incumbent_solution = copy.deepcopy(new_sol)
                incumbent_obj = new_obj

            if calculate_total_cost(incumbent_solution, self.distance_matrix, self.demands, self.vehicle_capacities)[0] < calculate_total_cost(global_best_solution, self.distance_matrix, self.demands, self.vehicle_capacities)[0]:
                global_best_solution = copy.deepcopy(incumbent_solution)

            temperature *= cooling_factor

            objectives.append(calculate_total_cost(
                incumbent_solution, self.distance_matrix, self.demands, self.vehicle_capacities)[0])
            n_iter -= 1

        obj, loads, final_solution = calculate_total_cost(
            global_best_solution, self.distance_matrix, self.demands, self.vehicle_capacities)

        self.final_solution = final_solution
        self.final_total_objective_value = obj
        self.objective_change_iteration = objectives
        self.vehicle_loads = loads

        return final_solution, obj, loads, objectives
