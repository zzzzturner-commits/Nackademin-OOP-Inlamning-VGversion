from models.tc_test_case import TestCase
from uuid import UUID

#Kontroll av att create returnerar ett test case
def test_create__should_return_a_test_case(valid_test_case_dto):

    #arrange
    test_case = TestCase()

    #act
    result = test_case.create(valid_test_case_dto)

    #assert
    assert isinstance(result, TestCase)

#kontroll av att informationen överförs korrekt mellan dto och test case
def test_create__should_copy_all_attributes_from_dto(valid_test_case_dto):

    #arrange
    test_case = TestCase()

    #act
    result = test_case.create(valid_test_case_dto)

    #assert
    assert result.tc_id == valid_test_case_dto.tc_id
    assert result.title == valid_test_case_dto.title
    assert result.purpose == valid_test_case_dto.purpose
    assert result.acceptance_criteria == valid_test_case_dto.acceptance_criteria
    assert result.preconditions == valid_test_case_dto.preconditions
    assert result.test_data == valid_test_case_dto.test_data
    assert result.steps == valid_test_case_dto.steps
    assert result.expected_result == valid_test_case_dto.expected_result

#Kontroll för att se så att UUID skapas för varje test case
def test_create__should_generate_a_uuid_for_every_test_case(valid_test_case_dto):

    #arrange
    test_case = TestCase()

    #act
    result = test_case.create(valid_test_case_dto)

    #assert
    assert isinstance(result.id, UUID)

#Kontroll för att se att varje test case får ett unikt UUID
def test_create__should_generate_a_unique_uuid_for_every_test_case(valid_test_case_dto):

    #arrange
    first_test_case = TestCase().create(valid_test_case_dto)
    second_test_case = TestCase().create(valid_test_case_dto)

    #act och assert
    assert first_test_case.id != second_test_case.id
