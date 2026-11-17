from uuid import uuid4, UUID
from models.test_data import TestData
from models.precondition import Precondition
from models.step import Step

class TestCase:
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

    def create_test_case(self, id: uuid4, tc_id: str, title: str, purpose: str, acceptance_criteria: str, preconditions: list, test_data: list, steps: list, expected_result: str) -> "TestCase":
        return self(
            id =(uuid4()),
            tc_id = str,
            title = str,
            acceptance_criteria = str,
            preconditions = list,
            test_data = list,
            steps = list,
            expected_result = str
        )

    def add_precondition(self, id: int, criteria: str):
        self.id: int
        self.criteria: str

    def add_test_data(self, key: str, value: str):
        self.key: str
        self.value: str

    def add_step(self, id: int, instruction: str):
        self.id: int
        self.instuction: str