from models.tc_test_case import TestCase
from models.tc_create_test_case_result import CreateTestCaseResult
from models.tc_get_test_case_result import GetTestCaseResult
from repository.tc_repository import TestCaseRepository
from models.tc_create_test_case_dto import CreateTestCaseDto


class TestCaseService:
    __test__ = False
    
    def __init__(self, repository: TestCaseRepository):
        self.repository: TestCaseRepository = repository

    def create_test_case(self, test_case_dto: CreateTestCaseDto) -> CreateTestCaseResult:

        if not test_case_dto.tc_id.strip():
            return CreateTestCaseResult(False, "Id is required. Please follow the example")

        if not test_case_dto.title.strip():
            return CreateTestCaseResult(False, "Title is required. Please follow the example.\n")

        if not test_case_dto.purpose.strip():
            return CreateTestCaseResult(False, "Purpose is required. Please follow the example.\n")
        
        if not test_case_dto.acceptance_criteria.strip():
            return CreateTestCaseResult(False, "Acceptance criteria is required. Please follow the example.\n")

        if not test_case_dto.preconditions.strip():
            return CreateTestCaseResult(False, "Preconditions are required. Please follow the example.\n")

        if not test_case_dto.test_data.strip():
            return CreateTestCaseResult(False, "Test data is required. Please follow the example.\n")

        if not test_case_dto.steps.strip():
            return CreateTestCaseResult(False, "Steps are required. Please follow the example.\n")

        if not test_case_dto.expected_result.strip():
            return CreateTestCaseResult(False, "Expected result is required. Please follow the example.\n")

        test_case = TestCase().create(
            test_case_dto
        )
        
        self.repository.try_create_test_case(test_case)
        return CreateTestCaseResult(True, f"Test case with the id'{test_case.tc_id}' has been added successfully.", test_case)

    def get_test_cases(self) -> GetTestCaseResult:
        
        test_cases = self.repository.get_all_test_cases()

        if not test_cases:
            return GetTestCaseResult(True, "No test cases registered.", [])

        return GetTestCaseResult(True, "Test cases retrieved successfully.", test_cases)

    def get_test_case_by_index(self, index):

        test_cases = self.repository.get_all_test_cases()

        if 0 <= index < len(test_cases):
            return test_cases[index]

        return None