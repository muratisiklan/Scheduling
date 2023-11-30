from abc import ABC, abstractmethod


class ParallelMachineScheduling(ABC):
    def __init__(self,
                 process_times,
                 ready_times,
                 due_dates,
                 setup_times) -> None:

        self.process_times = process_times
        self.ready_times = ready_times
        self.due_dates = due_dates
        self.setup_times = setup_times

    @abstractmethod
    def solve(self):
        pass
    
    def random(self):
        print("it works")