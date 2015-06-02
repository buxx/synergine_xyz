from os import getcwd
from synergine.synergy.Simulation import Simulation
from synergine.synergy.collection.SynergyCollection import SynergyCollection
from synergine_xyz.SynergyObject import SynergyObject
from synergine.test.TestSimulation import TestSimulation


class AntObj(SynergyObject):
    pass


class EggObj(SynergyObject):
    pass


class RockObj(SynergyObject):
    pass


class FoodObj(SynergyObject):
    pass


class AntCollection(SynergyCollection):
    pass


class EnvCollection(SynergyCollection):
    pass


class TmxMap(TestSimulation):

    _map_file_path = getcwd()+"/tests/tmx/src/map.tmx"
    _map_config = {
        'simulation': {
            'base': Simulation
        },
        'collection': {
            'ant': AntCollection,
            'env': EnvCollection
        },
        'object': {
            'ant': AntObj,
            'egg': EggObj,
            'rock': RockObj,
            'food': FoodObj
        }
    }
