from pyAmakCore.classes.tools.schedulerIHM import SchedulerIHM
from time import sleep


class SimpleScheduler(SchedulerIHM):

    def last_part(self):
        super().last_part()
        if self.amas.get_cycle() == 100:
            self.save()
            sleep(10)
            self.exit_program()
