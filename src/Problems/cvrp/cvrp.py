from abc import ABC, abstractmethod


class CapacitatedVehicleRouting(ABC):
    def __init__(self,
                 distance_matrix,
                 demands,
                 vehicle_capacities,
                 ) -> None:

        self.distance_matrix = distance_matrix
        self.demands = demands
        self.vehicle_capacities = vehicle_capacities

     # Distance (cost) matrix nXn N(number of nodes) Assumin 0 is source node
     # demands nx1 representing demand amount in each node (assumin source node have no demand)
     # Vechile capacity mx1 M(total number of vechiles) representing capacity of each vechile

    @abstractmethod
    def solve(self):
        pass

    def random(self):
        print("Capacitated Vechile Routing Problem")
