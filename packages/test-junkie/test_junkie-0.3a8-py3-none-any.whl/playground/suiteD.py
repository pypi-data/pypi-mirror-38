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
       parameters=[1, 2, 3],
       priority=2, pr=[TestSuiteB], feature="Login", owner="Mike")
class TestSuiteD:

    @test(tags=["tag a", "tag d"], owner="Artur")
    def a(self, suite_parameter):
        pass

    @test(component="OAuth", tags=["tag a", "tag d"])
    def b(self):
        pass
