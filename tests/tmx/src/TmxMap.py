import unittest
from os import getcwd
from synergine.synergy.Simulation import Simulation
from synergine.synergy.collection.SynergyCollection import SynergyCollection
from synergine.synergy.object.SynergyObject import SynergyObject


class AntObj:
    pass


class EggObj:
    pass


class RockObj:
    pass


class FoodObj:
    pass


class TmxMap(unittest.TestCase):

    _map_file_path = getcwd()+"/tests/tmx/src/map.tmx"
    _map_config = {
        'simulation': {
            'base': Simulation
        },
        'collection': {
            'ant': SynergyCollection,
            'env': SynergyCollection
        },
        'object': {
            'ant': AntObj,
            'egg': EggObj,
            'rock': RockObj,
            'food': FoodObj
        }
    }
