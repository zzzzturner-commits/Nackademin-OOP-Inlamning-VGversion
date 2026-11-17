from models.precondition import Precondition
from models.test_data import TestData
from models.step import Step


class CreateTestCaseDto:
    def __init__(self):
        self.tc_id: str
        self.title: str
        self.purpose: str
        self.acceptance_criteria: str
        self.preconditions: list[Precondition] = []
        self.test_data: list[TestData] = []
        self.steps: list[Step] = []
        self.expected_result: str