import time

from test_junkie.decorators import Suite, test, beforeClass, beforeTest, afterTest, afterClass
from test_junkie.meta import meta, Meta
from tests.junkie_suites.TestListener import TestListener
from tests.junkie_suites.TestRules import TestRules


@Suite(retry=2,
       listener=TestListener,
       rules=TestRules,
       meta=meta(name="Test Suite",
                 known_bugs=[]),
       parameters=[1, 2], priority=1, feature="Login",
       owner="George")
class TestSuiteB:

    @test(priority=2)
    def a(self):
        time.sleep(2)
        print("Finished SUITE B / TEST A")

    @test(priority=1, tags=["tag 1", "tag c"])
    def b(self):
        time.sleep(2)
        print("Finished SUITE B / TEST B")
