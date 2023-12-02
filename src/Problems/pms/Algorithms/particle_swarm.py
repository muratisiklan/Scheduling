from src.Problems.pms.pms import ParallelMachineScheduling


class ParticleSwarm(ParallelMachineScheduling):
    def __init__(self, process_times, ready_times, due_dates, setup_times) -> None:
        super().__init__(process_times, ready_times, due_dates, setup_times)