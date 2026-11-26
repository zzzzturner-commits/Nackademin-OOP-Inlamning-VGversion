from models.tc_test_case import TestCase
from uuid import UUID

#Kontroll av att create returnerar ett test case. återigen med hjälp av en fixture som gör att man slipper skapa och fylla i en dto för vare test.
def test_create__should_return_a_test_case(valid_test_case_dto):

    #arrange
    #skapar ett nytt objekt av klassen TestCase
    test_case = TestCase()

    #act
    #här anropar vi create och skickar in dton som argument som sparas i variabeln result.
    result = test_case.create(valid_test_case_dto)

    #assert
    # kontroll av att result är ett objekt av typen TestCase.
    # isinstance kontrollerar om ett objekt är av en viss klass eller dess underklass.
    assert isinstance(result, TestCase)

#kontroll av att informationen överförs korrekt mellan dto och test case
def test_create__should_copy_all_attributes_from_dto(valid_test_case_dto):

    #arrange
    # skapar ett nytt objekt av klassen TestCase
    test_case = TestCase()

    #act
    # dton skickas till create och sparar det returnerade objektet i result.
    result = test_case.create(valid_test_case_dto)

    #assert
    #Här jämförs attributen med det returnerade testfallet i dton en efter en.
    # om något failar vet man vart man ska titta för att hitta felet.
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
    # skapar ett nytt objekt av klassen TestCase
    test_case = TestCase()

    #act
    # dton skickas till create och sparar det returnerade objektet i result.
    result = test_case.create(valid_test_case_dto)

    #assert
    # kontroll för att se om id är av typen UUID
    assert isinstance(result.id, UUID)

#Kontroll för att se att varje test case får ett unikt UUID
def test_create__should_generate_a_unique_uuid_for_every_test_case(valid_test_case_dto):

    #arrange
    # här skapas två likadana testfall, TestCase objekt
    first_test_case = TestCase().create(valid_test_case_dto)
    second_test_case = TestCase().create(valid_test_case_dto)

    #act och assert
    # här kontrolleras och jämförs de två UUID som skapats för att se så att varje testfall får ett unikt UUID.
    assert first_test_case.id != second_test_case.id
