from models.tc_test_case import TestCase

class CreateTestCaseResult:
    def __init__(self, succeeded: bool, message: str, test_case: TestCase | None = None):
        self.succeeded: bool = succeeded
        self.message: str = message
        self.test_case: TestCase = test_case