from models.tc_test_case import TestCase

class GetTestCaseResult:
    def __init__(self, succeeded: bool, message: str, test_cases: TestCase):
        self.succeeded: bool = succeeded
        self.message: str = message
        self.test_cases: list[TestCase] = test_cases