from models.test_case import TestCase
from models.create_test_case_result import CreateTestCaseResult
from models.get_test_case_result import GetTestCaseResult
from repository.test_case_repository import TestCaseRepository
from models.create_test_case_dto import CreateTestCaseDto


class TestCaseService:
    def __init__(self, repository: TestCaseRepository):
        self.repository: TestCaseRepository = repository

    def create_test_case(self, test_case: CreateTestCaseDto) -> CreateTestCaseResult:

        if not test_case.id:
           return CreateTestCaseResult(False, "Id is required. Please follow the example.\n")

        if not test_case.title:
            return CreateTestCaseResult(False, "Title is required. Please follow the example.\n")

        if not test_case.purpose:
            return CreateTestCaseResult(False, "Purpose is required. Please follow the example.\n")
        
        if not test_case.acceptance_criteria:
            return CreateTestCaseResult(False, "Acceptance criteria is required. Please follow the example.\n")

        if not test_case.preconditions:
            return CreateTestCaseResult(False, "Preconditions are required. Please follow the example.\n")

        if not test_case.test_data:
            return CreateTestCaseResult(False, "Test data is required. Please follow the example.\n")

        if not test_case.steps:
            return CreateTestCaseResult(False, "Steps are required. Please follow the example.\n")

        if not test_case.expected_result:
            return CreateTestCaseResult(False, "Expected result is required. Please follow the example.\n")
        
        self.repository.try_create_test_case(test_case)
        return CreateTestCaseResult(True, f"Test case with the id'{test_case.tc_id}' has been added successfully.", test_case)

    def get_test_cases(self) -> GetTestCaseResult:
        return self.repository.get_all_test_cases()

    def get_test_case_by_index(self, index):

        test_cases = self.repository.get_all_test_cases()

        if 0 <= index < len(test_cases):
            return test_cases[index]

        return None