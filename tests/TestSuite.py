from synergine.test.TestSuite import TestSuite as BaseTestSuite
from tests.core.display.TestZone import TestZone

class TestSuite(BaseTestSuite):

    def __init__(self):
        super().__init__()
        self.add_test_cases([TestZone])
