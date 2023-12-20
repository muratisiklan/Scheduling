import random
import copy
import numpy as np


def calculate_total_cost(solution, distances, demands, vehicle_capacities):
    total_cost = 0
    visited_customers = set()

    current_vehicle = 0
    total_loads = []  # Indicates total load of each single vehicles

    for vehicle_route in solution:
        if not vehicle_route:
            current_vehicle += 1
            continue

        current_load = 0
        current_node = 0

        for customer in vehicle_route:

            if customer in visited_customers:
                total_cost += float('inf')
            else:

                distance_to_customer = distances[current_node][customer]

                total_cost += distance_to_customer

                current_node = customer

                current_load += demands[customer]

                visited_customers.add(customer)

        total_loads.append(current_load)

        total_cost += distances[current_node][0]

        if current_load > vehicle_capacities[current_vehicle]:
            total_cost += float('inf')

        current_vehicle += 1

    return total_cost, total_loads,copy.deepcopy(solution)

def create_initial_solution(distances, demands, vehicle_capacities):

    n_nodes = len(distances)
    n_vehicles = len(vehicle_capacities)

    # array composed of customer nodes
    customers = np.arange(1, n_nodes)
    np.random.shuffle(customers)

    solution = [[] for _ in range(n_vehicles)]

    remaining_capacity = vehicle_capacities.copy()

    for customer in customers:

        max_index = np.argmax(remaining_capacity)

        solution[max_index].append(int(customer))
        remaining_capacity[max_index] -= demands[customer]

    return solution




def create_neighbor_solution(solution):
    n_nodes = len(solution)

    sequence = copy.deepcopy(solution)

    if any(not sub_list for sub_list in sequence):

        max_length_index = max(range(len(sequence)),
                               key=lambda i: len(sequence[i]))

        empty_index = None
        for i, sublist in enumerate(sequence):
            if not sublist:
                empty_index = i
                break

        rand = random.randint(0, len(sequence[max_length_index])-1)
        sequence[empty_index].append(sequence[max_length_index][rand])
        sequence[max_length_index].pop(rand)

    else:
        # modified randoms, debug if necessary
        m1 = random.randint(0, n_nodes-1)
        m2 = random.randint(0, n_nodes-1)
        dec = random.random()

        if dec >= 0.5:

            for_m1 = random.randint(0, len(sequence[m1])-1)
            for_m2 = random.randint(0, len(sequence[m2])-1)

            temp = sequence[m1][for_m1]
            sequence[m1][for_m1] = sequence[m2][for_m2]
            sequence[m2][for_m2] = temp
        else:
            for_m1 = random.randint(0, len(sequence[m1])-1)
            for_m2 = random.randint(0, len(sequence[m1])-1)

            element = sequence[m1].pop(for_m1)
            sequence[m2].append(element)

    return sequence
