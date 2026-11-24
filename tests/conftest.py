import pytest
from models.tc_create_test_case_dto import CreateTestCaseDto

@pytest.fixture
def valid_test_case_dto():
    dto = CreateTestCaseDto()
    dto.tc_id = "TC-001"
    dto.title = "Testning av login"
    dto.purpose = "Verifiering av användare/user login"
    dto.acceptance_criteria = "Användare/user ska kunna logga in"
    dto.preconditions = "Användar konto existerar"
    dto.test_data = "inloggningsuppgifter"
    dto.steps = "1. Öpnna login sidan. 2. skriv in inloggningsuppgifter"
    dto.expected_result = "Användaren kan logga in med sina inloggningsuppgifter"

    return dto