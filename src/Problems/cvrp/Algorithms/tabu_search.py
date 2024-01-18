import copy
from src.Problems.cvrp.Algorithms.utils import (create_initial_solution,
                                                create_neighbor_solution,
                                                calculate_total_cost)
from src.Problems.cvrp.cvrp import CapacitatedVehicleRouting


class TabuSearch(CapacitatedVehicleRouting):
    def __init__(self, distance_matrix, demands, vehicle_capacities) -> None:
        super().__init__(distance_matrix, demands, vehicle_capacities)
        self._construct_initial_solution()

    def _construct_initial_solution(self):
        self.initial_solution = create_initial_solution(
            self.distance_matrix,
            self.demands,
            self.vehicle_capacities
        )

    @staticmethod
    def _create_neighborhood(solution, n_solutions):
        neighborhood = [create_neighbor_solution(
            copy.deepcopy(solution)) for _ in range(n_solutions)]
        return neighborhood


    def solve(self,
            n_iter: int = 100,
            aspiration: bool = True,
            tabu_tenure: int = 10,
            n_neighbors: int = 20):

        if aspiration:

            global_best_solution = copy.deepcopy(self.initial_solution)

            tabuList = []
            best_sol = copy.deepcopy(self.initial_solution)
            best_obj, _, _ = calculate_total_cost(
                best_sol, self.distance_matrix, self.demands, self.vehicle_capacities)
            objectives = []

            for i in range(n_iter):

                neighbor_set = self._create_neighborhood(
                    best_sol, n_neighbors)
                neigh_obj = []
                for j in range(len(neighbor_set)):
                    neigh_obj.append(calculate_total_cost(
                        neighbor_set[j], self.distance_matrix, self.demands, self.vehicle_capacities)[0])

                # Chek for solutions better than current best in neighborhood

                bettersol_set = [n for n in neighbor_set if calculate_total_cost(
                    n, self.distance_matrix, self.demands, self.vehicle_capacities)[0] < best_obj]
                bettersol_obj = [calculate_total_cost(n, self.distance_matrix, self.demands, self.vehicle_capacities)[
                    0] for n in bettersol_set]

                for k in range(len(bettersol_set)):
                    bettersol_obj.append(calculate_total_cost(
                        bettersol_set[k], self.distance_matrix, self.demands, self.vehicle_capacities)[0])

                # If there exists better solutions, choose best one regardless of being in tabu list
                if bettersol_set:
                    best_index = bettersol_obj.index(min(bettersol_obj))
                    best_sol = copy.deepcopy(bettersol_set[best_index])
                    best_obj = copy.deepcopy(bettersol_obj[best_index])
                # If no better solutions, choose best among solutions which are not in tabu list
                else:
                    non_tabu_set = [
                        n for n in neighbor_set if n not in tabuList]
                    if non_tabu_set:
                        non_tabu_obj = [calculate_total_cost(n, self.distance_matrix, self.demands,self.vehicle_capacities)[
                            0] for n in non_tabu_set]
                        best_index = non_tabu_obj.index(min(non_tabu_obj))
                        best_sol = copy.deepcopy(non_tabu_set[best_index])
                        best_obj = copy.deepcopy(non_tabu_obj[best_index])

                # Add the  new solution to the tabu list
                tabuList.append(best_sol)

                # Remove the oldest entry from the tabu list if it has reached its maximum size
                if len(tabuList) > tabu_tenure:
                    tabuList.pop(0)

                objectives.append(best_obj)

                if calculate_total_cost(global_best_solution, self.distance_matrix, self.demands, self.vehicle_capacities)[0] > calculate_total_cost(best_sol, self.distance_matrix, self.demands, self.vehicle_capacities)[0]:
                    global_best_solution = copy.deepcopy(best_sol)

            obj, loads, final_solution = calculate_total_cost(
                global_best_solution, self.distance_matrix, self.demands, self.vehicle_capacities)

            return final_solution, obj, objectives,loads
        else:
            global_best_solution = copy.deepcopy(self.initial_solution)

            tabuList = []
            best_sol = copy.deepcopy(self.initial_solution)
            objectives = []

            for i in range(n_iter):
                neighbor_set = self._create_neighborhood(
                    best_sol, n_neighbors)
                neigh_obj = []

                for j in range(len(neighbor_set)):
                    neigh_obj.append(calculate_total_cost(
                        neighbor_set[j], self.distance_matrix, self.demands, self.vehicle_capacities)[0])

                best_candidate = neigh_obj.index(min(neigh_obj))

                if neighbor_set[best_candidate] not in tabuList:

                    best_sol = copy.deepcopy(neighbor_set[best_candidate])

                else:

                    non_tabu_set = [
                        n for n in neighbor_set if n not in tabuList]
                    if non_tabu_set:
                        non_tabu_obj = [calculate_total_cost(n, self.distance_matrix, self.demands, self.vehicle_capacities)[
                            0] for n in non_tabu_set]
                        best_candidate = non_tabu_obj.index(min(non_tabu_obj))
                        best_sol = copy.deepcopy(non_tabu_set[best_candidate])

                tabuList.append(best_sol)

                if len(tabuList) > tabu_tenure:
                    tabuList.pop(0)

                obj, _, _ = calculate_total_cost(
                    best_sol, self.distance_matrix, self.demands, self.vehicle_capacities)
                objectives.append(obj)

                if calculate_total_cost(global_best_solution, self.distance_matrix, self.demands, self.vehicle_capacities)[0] > calculate_total_cost(best_sol, self.distance_matrix, self.demands, self.vehicle_capacities)[0]:
                    global_best_solution = copy.deepcopy(best_sol)

            obj, loads, final_solution = calculate_total_cost(
                global_best_solution, self.distance_matrix, self.demands, self.vehicle_capacities)

            self.final_solution = final_solution
            self.final_total_objective_value = obj
            self.objective_change_iteration = objectives
            self.vehicle_loads = loads

            return final_solution, obj, objectives, loads