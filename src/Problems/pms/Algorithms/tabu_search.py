import copy
from src.Problems.pms.Algorithms.utils import (create_initial_solution,
                                               create_neighbor_solution,
                                               calculate_tardiness)
from src.Problems.pms.pms import ParallelMachineScheduling


class TabuSearch(ParallelMachineScheduling):
    def __init__(self, process_times, ready_times, due_dates, setup_times) -> None:
        super().__init__(process_times, ready_times, due_dates, setup_times)
        self._construct_initial_solution()

    def _construct_initial_solution(self):
        self.initial_solution = create_initial_solution(
            self.process_times
        )

    @staticmethod
    def _create_neighborhood(solution, n_solutions):
        neighborhood = [create_neighbor_solution(
            copy.deepcopy(solution)) for _ in range(n_solutions)]
        return neighborhood

    def solve(self,
              n_iterations: int = 20,
              aspiration: bool = True,
              tabu_tenure: int = 10,
              n_neighbors: int = 20):

        if aspiration:

            global_best_solution = copy.deepcopy(self.initial_solution)

            tabuList = []
            best_sol = copy.deepcopy(self.initial_solution)
            best_obj, _, compt, startt = calculate_tardiness(
                best_sol, self.process_times, self.due_dates, self.ready_times, self.setup_times)
            objectives = []

            for i in range(n_iterations):

                neighbor_set = self._create_neighborhood(
                    best_sol, n_neighbors)
                neigh_obj = []
                for j in range(len(neighbor_set)):
                    neigh_obj.append(calculate_tardiness(
                        neighbor_set[j], self.process_times, self.due_dates, self.ready_times, self.setup_times)[0])

                # Chek for solutions better than current best in neighborhood

                bettersol_set = [n for n in neighbor_set if calculate_tardiness(
                    n, self.process_times, self.due_dates, self.ready_times, self.setup_times)[0] < best_obj]
                bettersol_obj = [calculate_tardiness(n, self.process_times, self.due_dates, self.ready_times, self.setup_times)[
                    0] for n in bettersol_set]

                for k in range(len(bettersol_set)):
                    bettersol_obj.append(calculate_tardiness(
                        bettersol_set[k], self.process_times, self.due_dates, self.ready_times, self.setup_times)[0])

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
                        non_tabu_obj = [calculate_tardiness(n, self.process_times, self.due_dates, self.ready_times, self.setup_times)[
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

                if calculate_tardiness(global_best_solution, self.process_times, self.due_dates, self.ready_times, self.setup_times)[0] > calculate_tardiness(best_sol, self.process_times, self.due_dates, self.ready_times, self.setup_times)[0]:
                    global_best_solution = copy.deepcopy(best_sol)

            tardiness, sequence, comptime, starttime = calculate_tardiness(
                global_best_solution, self.process_times, self.due_dates, self.ready_times, self.setup_times)

            return sequence, tardiness, objectives, comptime, starttime
        else:
            global_best_solution = copy.deepcopy(self.initial_solution)

            tabuList = []
            best_sol = copy.deepcopy(self.initial_solution)
            objectives = []

            for i in range(n_iterations):
                neighbor_set = self._create_neighborhood(
                    best_sol, n_neighbors)
                neigh_obj = []

                for j in range(len(neighbor_set)):
                    neigh_obj.append(calculate_tardiness(
                        neighbor_set[j], self.process_times, self.due_dates, self.ready_times, self.setup_times)[0])

                best_candidate = neigh_obj.index(min(neigh_obj))

                if neighbor_set[best_candidate] not in tabuList:

                    best_sol = copy.deepcopy(neighbor_set[best_candidate])

                else:

                    non_tabu_set = [
                        n for n in neighbor_set if n not in tabuList]
                    if non_tabu_set:
                        non_tabu_obj = [calculate_tardiness(n, self.process_times, self.due_dates, self.ready_times, self.setup_times)[
                            0] for n in non_tabu_set]
                        best_candidate = non_tabu_obj.index(min(non_tabu_obj))
                        best_sol = copy.deepcopy(non_tabu_set[best_candidate])

                tabuList.append(best_sol)

                if len(tabuList) > tabu_tenure:
                    tabuList.pop(0)

                obj, seq, compt, stime = calculate_tardiness(
                    best_sol, self.process_times, self.due_dates, self.ready_times, self.setup_times)
                objectives.append(obj)

                if calculate_tardiness(global_best_solution, self.process_times, self.due_dates, self.ready_times, self.setup_times)[0] > calculate_tardiness(best_sol, self.process_times, self.due_dates, self.ready_times, self.setup_times)[0]:
                    global_best_solution = copy.deepcopy(best_sol)

            obj, seq, compt, stime = calculate_tardiness(
                global_best_solution, self.process_times, self.due_dates, self.ready_times, self.setup_times)

            self.final_solution = seq
            self.final__total_objective_value = obj
            self.objective_change_iteration = objectives
            self.final_compt = compt
            self.final_stime = stime

            return seq, obj, objectives, compt, stime
