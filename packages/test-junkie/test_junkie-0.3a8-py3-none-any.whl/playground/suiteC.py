import time

from playground.suiteB import TestSuiteB
from test_junkie.decorators import Suite, test, beforeClass, beforeTest, afterTest, afterClass
from test_junkie.meta import meta, Meta
from tests.junkie_suites.TestListener import TestListener
from tests.junkie_suites.TestRules import TestRules


@Suite(retry=2,
       listener=TestListener,
       rules=TestRules,
       meta=meta(name="Test Suite",
                 known_bugs=[]),
       parameters=[1, 2],
       parallelized=False)
class TestSuiteC:

    @test(tags=["tag a", "tag d"], owner="Victor")
    def a(self):
        time.sleep(3)

    @test(tags=["tag a", "tag d"], owner="Mike")
    def b(self):
        time.sleep(3)
