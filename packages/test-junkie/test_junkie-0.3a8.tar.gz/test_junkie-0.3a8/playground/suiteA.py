import time

from playground.suiteB import TestSuiteB
from test_junkie.decorators import Suite, test, beforeClass, beforeTest, afterTest, afterClass
from test_junkie.meta import meta, Meta
from tests.junkie_suites.TestListener import TestListener
from tests.junkie_suites.TestRules import TestRules


def test_func():
    print("evaluating...")
    time.sleep(2)
    return [{"key": "value"}, {"key2": "value2"}]


@Suite(retry=2,
       listener=TestListener,
       rules=TestRules,
       meta=meta(name="Test Suite",
                 known_bugs=[]),
       owner="Mike")
class TestSuiteA(object):

    @test(dependencies=[])
    def a(self):
        print("Finished SUITE A / TEST A")

    # @test(priority=1, pr=[TestSuiteB.a])
    # def b(self):
    #     # time.sleep(15)
    #     print("Finished SUITE A / TEST B")
    #
    # @test(skip=True)
    # def c(self):
    #     # time.sleep(15)
    #     print("Finished SUITE A / TEST C")
