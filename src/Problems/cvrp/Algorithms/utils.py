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

    return total_cost, total_loads
