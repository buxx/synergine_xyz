from synergine.test.TestSuite import TestSuite as BaseTestSuite
from tests.core.display.TestZone import TestZone
from tests.tmx.TestExtracts import TestExtracts
from tests.tmx.TestLoadMap import TestLoadMap


class TestSuite(BaseTestSuite):

    def __init__(self):
        super().__init__()
        self.add_test_cases([TestZone, TestLoadMap, TestExtracts])
