from random import seed
from sma_scheduler import SimpleScheduler
from pyAmakIHM.classes.fenetre import Fenetre
from pyAmakCore.exception.override import ToOverrideWarning
from pyAmakCore.enumeration.executionPolicy import ExecutionPolicy
from sma_controller import ControleurSMA
from sma_amas import SimpleAmas
from sma_environnement import SimpleEnvironment

seed()

ToOverrideWarning.enable_warning(False)

fenetre = Fenetre("Prototype Ants")


env = SimpleEnvironment(0, fenetre.get_canvas_width(),
                        0, fenetre.get_canvas_height(), 5, 7)
amas = SimpleAmas(env, ExecutionPolicy.ONE_PHASE)
# amas = AntHillExample(env, ExecutionPolicy.TWO_PHASES)

scheduler = SimpleScheduler(amas)

controleur = ControleurSMA(fenetre, scheduler)


def main():
    controleur.start()


main()
