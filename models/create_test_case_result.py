from models.test_case import TestCase

class CreateTestCaseResult:
    def __init__(self, succeded: bool, message: str, test_case: TestCase):
        self.succeded: bool = succeded
        self.message: str = message
        self.test_case: TestCase = test_case