from pyAmakCore.classes.tools.schedulerIHM import SchedulerIHM

from pyAmakCore.enumeration.executionPolicy import ExecutionPolicy
from pyAmakCore.exception.override import ToOverrideWarning
from pyAmakIHM.classes.fenetre import Fenetre
from sma_controller import ControleurSMA
from sma_amas import SimpleAmas

fenetre = Fenetre("Prototype Philosophers")

ToOverrideWarning.enable_warning(False)

amas = SimpleAmas(ExecutionPolicy.ONE_PHASE)

scheduler = SchedulerIHM(amas)

controleur = ControleurSMA(fenetre, scheduler)


def main():
    controleur.start()


main()