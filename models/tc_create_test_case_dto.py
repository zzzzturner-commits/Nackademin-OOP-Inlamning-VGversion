from models.tc_precondition import Precondition
from models.tc_test_data import TestData
from models.tc_step import Step


class CreateTestCaseDto:
    def __init__(self):
        self.tc_id: str
        self.title: str
        self.purpose: str
        self.acceptance_criteria: str
        self.preconditions: str
        self.test_data: str
        self.steps: str
        self.expected_result: str