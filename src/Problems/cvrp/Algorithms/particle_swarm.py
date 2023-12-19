from src.Problems.cvrp.cvrp import CapacitatedVehicleRouting
from src.Problems.cvrp.Algorithms.utils import (calculate_total_cost)






class ParticleSwarm(CapacitatedVehicleRouting):
    def __init__(self, distance_matrix, demands, vehicle_capacities) -> None:
        super().__init__(distance_matrix, demands, vehicle_capacities)
    
    def solve(self):
        pass