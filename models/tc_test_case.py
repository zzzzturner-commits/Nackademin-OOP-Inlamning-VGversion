from uuid import uuid4, UUID
from models.tc_test_data import TestData
from models.tc_precondition import Precondition
from models.tc_step import Step
from models.tc_create_test_case_dto import CreateTestCaseDto

class TestCase:
    __test__ = False
    
    def __init__(self):
        self.id: UUID = uuid4()
        self.tc_id: str
        self.title: str
        self.purpose: str
        self.acceptance_criteria: str
        self.preconditions: list[Precondition] = []
        self.test_data: list[TestData] = []
        self.steps: list[Step] = []
        self.expected_result: str

    def create(self, test_case_dto: CreateTestCaseDto) -> "TestCase":
        test_case = TestCase()
        
        test_case.id =(uuid4())
        test_case.tc_id = test_case_dto.tc_id  
        test_case.title = test_case_dto.title
        test_case.purpose = test_case_dto.purpose
        test_case.acceptance_criteria = test_case_dto.acceptance_criteria
        test_case.preconditions = test_case_dto.preconditions
        test_case.test_data = test_case_dto.test_data
        test_case.steps = test_case_dto.steps
        test_case.expected_result = test_case_dto.expected_result
        
        return test_case
    

    def add_precondition(self, id: int, criteria: str):
        self.id: int
        self.criteria: str

    def add_test_data(self, key: str, value: str):
        self.key: str
        self.value: str

    def add_step(self, id: int, instruction: str):
        self.id: int
        self.instuction: str