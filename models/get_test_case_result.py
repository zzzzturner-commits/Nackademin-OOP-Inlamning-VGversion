from models.test_case import TestCase

class GetTestCaseResult:
    def __init__(self, succeded: bool, message: str, test_cases: TestCase):
        self.succeded: bool = succeded
        self.message: str = message
        self.test_cases: list[TestCase] = test_cases