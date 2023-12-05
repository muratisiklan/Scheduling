import random
import numpy as np
import copy

# General functions regarding parallel machine scheduling


def create_initial_solution(
        process_times: list) -> list:
    """process times n x m list,
    represents process time of "job n" on "machine m"

    Returns:
        random solution if process_times doesnt provided
        feasible solution if process_times provided and feasible solution exists.
    """
    n_jobs = len(process_times)
    n_machines = len(process_times[0])

    solution = [[] for _ in range(n_machines)]

    machine_assignment = np.zeros(n_jobs)

    # Assign jobs based on process times (maybe some improvements can make)
    for i in range(n_jobs):
        if process_times[i][1] > 10000 and process_times[i][2] > 1000:
            machine_assignment[i] = np.argmin(process_times[i])
        else:
            rand = random.randint(0, n_machines-1)
            machine_assignment[i] = rand

    for index, value in enumerate(machine_assignment):
        solution[int(value)].append(index)

    return solution


def calculate_tardiness(solution, process_times, due_dates, ready_times, setup_times):
    sequence = copy.deepcopy(solution)
    n_machines = len(process_times[0])
    tardiness = np.zeros(len(process_times))

    completion_times = np.zeros(len(process_times))
    start_times = np.zeros(len(process_times))
    for i in range(len(sequence)):
        comptime = 0
        for index, value in enumerate(sequence[i]):
            if index == 0:
                completion_times[value] = comptime + \
                    process_times[value][i] + ready_times[value]+45
                comptime += process_times[value][i] + ready_times[value]+45
            else:

                if comptime >= ready_times[value]:
                    current_job = value
                    previous_job = sequence[i][index-1]

                    completion_times[value] = comptime + \
                        process_times[value][i] + \
                        setup_times[previous_job][current_job]
                    comptime += process_times[value][i] + \
                        setup_times[previous_job][current_job]

                else:
                    current_job = value
                    previous_job = sequence[i][index-1]

                    completion_times[value] = ready_times[value] + \
                        process_times[value][i] + \
                        setup_times[previous_job][current_job]
                    comptime += process_times[value][i] + setup_times[previous_job][current_job] + (
                        ready_times[value]-comptime)

            start_times[value] = completion_times[value] - \
                process_times[value][i]

    for i in range(len(process_times)):
        tardiness[i] = max(completion_times[i]-due_dates[i], 0)

    return tardiness.sum(), sequence, completion_times, start_times


def create_neighbor_solution(solution):

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

        m1 = random.randint(0, 2)
        m2 = random.randint(0, 2)
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


# For Genetic Algorithm

def create_population(process_times: list, size=100):
    population = []

    while size > 0:
        population.append(create_initial_solution(process_times))
        size -= 1

    return population
