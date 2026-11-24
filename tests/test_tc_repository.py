#Behövs inte i pytest, man kallar på fixturen conftest i testfunktionens parameter.
#from tests.conftest import valid_test_case_dto
#hade ett problem med test_case = TestCase.create delen. la till () efter TestCase så fungerade det.
from models.tc_test_case import TestCase
from repository.tc_repository import TestCaseRepository
from models.tc_create_test_case_dto import CreateTestCaseDto



# Hämta tom lista.
def test_get_all_test_cases__should_return_empty_list_initially():
    # Arrange
    repository = TestCaseRepository()
    

    #Act
    result = repository.get_all_test_cases()

    #Assert
    assert result == []

# Hämta en lista med ett test case inlagt.
def test_get_all_test_cases__should_return_a_list_of_test_cases(valid_test_case_dto):

    #Arrange
    repository = TestCaseRepository()
    test_case = TestCase().create(valid_test_case_dto)

    #Act
    repository.try_create_test_case(test_case)
    result = repository.get_all_test_cases()

    #Assert
    assert result == [test_case]

# Returnera en KOPIA av listan [TestCase].
def test_get_all_test_cases__should_return_a_copy_of_test_cases(valid_test_case_dto):

    #arrange
    repository = TestCaseRepository()
    test_case = TestCase().create(valid_test_case_dto)
    repository.try_create_test_case(test_case)

    #act
    result = repository.get_all_test_cases()
    result.clear()

    #assert
    assert len(result) == 0
    assert len(repository.get_all_test_cases()) == 1

# Lagra och hämta flera testfall i rätt ordning.
def test_get_all_test_cases__should_be_able_to_store_multiple_test_cases(valid_test_case_dto):

    #arrange
    repository = TestCaseRepository()

    first_test_case = TestCase().create(valid_test_case_dto)

    second_dto = CreateTestCaseDto()
    second_dto.tc_id = "TC-002"
    second_dto.title = "Testning av logout"
    second_dto.purpose = "Verifiering av logout funktion"
    second_dto.acceptance_criteria = "Användare ska kunna logga ut"
    second_dto.preconditions = "Användare är inloggad"
    second_dto.test_data = "Användaren ska existera"
    second_dto.steps = "1. Klicka på logout"
    second_dto.expected_result = "Användaren kan logga ut och återvänder till log in sidan"

    second_test_case = TestCase().create(second_dto)
    #act
    repository.try_create_test_case(first_test_case)
    repository.try_create_test_case(second_test_case)

    result = repository.get_all_test_cases()

    #assert
    assert len(result) == 2
    assert result == [first_test_case, second_test_case]