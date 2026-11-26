from models.tc_test_case import TestCase

class TestCaseRepository:
    __test__ = False
    
    def __init__(self):
        self.__cases: list[TestCase] = []

    def try_create_test_case(self, test_case: TestCase) -> None:
        self.__cases.append(test_case)

    def get_all_test_cases(self) -> list[TestCase]:
        return self.__cases.copy()