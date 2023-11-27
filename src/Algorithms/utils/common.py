import random
import numpy as np
import copy


def create_initial_solution(
        n_jobs: int,
        n_machines: int,
        process_times: list = None) -> list:
    """process times n x m list,
    represents process time of "job n" on "machine m"

    Returns:
        random solution if process_times doesnt provided
        feasible solution if process_times provided and feasible solution exists.
    """

    solution = [[] for _ in range(n_machines)]

    machine_assignment = np.zeros(n_jobs)

    if not process_times:
        # Assign jobs randomly to machines
        machine_assignment = np.random.randint(0, n_machines, n_jobs)
    else:
        # Assign jobs based on process times
        for i in range(n_jobs):
            if process_times[i][1] > 10000 and process_times[i][2] > 1000:
                machine_assignment[i] = np.argmin(process_times[i])
            else:
                rand = random.randint(0, n_machines-1)
                machine_assignment[i] = rand

    for index, value in enumerate(machine_assignment):
        solution[int(value)].append(index)

    return solution


def calculate_tardienss(solution, process_times, duedates, readytimes, setuptimes):
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
                    process_times[value][i] + readytimes[value]+45
                comptime += process_times[value][i] + readytimes[value]+45
            else:

                if comptime >= readytimes[value]:
                    current_job = value
                    previous_job = sequence[i][index-1]

                    completion_times[value] = comptime + \
                        process_times[value][i] + \
                        setuptimes[previous_job][current_job]
                    comptime += process_times[value][i] + \
                        setuptimes[previous_job][current_job]

                else:
                    current_job = value
                    previous_job = sequence[i][index-1]

                    completion_times[value] = readytimes[value] + \
                        process_times[value][i] + \
                        setuptimes[previous_job][current_job]
                    comptime += process_times[value][i] + setuptimes[previous_job][current_job] + (
                        readytimes[value]-comptime)

            start_times[value] = completion_times[value] - \
                process_times[value][i]

    for i in range(len(process_times)):
        tardiness[i] = max(completion_times[i]-duedates[i], 0)

    return tardiness.sum(), sequence, completion_times, start_times
