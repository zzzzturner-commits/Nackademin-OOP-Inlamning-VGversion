#Behövs inte i pytest, man kallar på fixturen conftest i testfunktionens parameter.
#from tests.conftest import valid_test_case_dto
#hade ett problem med test_case = TestCase.create delen. la till () efter TestCase så fungerade det.
from models.tc_test_case import TestCase
from repository.tc_repository import TestCaseRepository
from models.tc_create_test_case_dto import CreateTestCaseDto



# Hämta tom lista.
def test_get_all_test_cases__should_return_empty_list_initially():

    #arrange
    #skapar en instans av repository
    repository = TestCaseRepository()

    #act
    #anropar och sparar det returnerade värdet i variuabeln result.
    result = repository.get_all_test_cases()

    #assert
    #kontroll att result är lika med en tom lista.
    assert result == []

# Hämta en lista med ett test case inlagt.
# pytest-fixture (valid_test_case_dto) används. den förbereder en giltig CreateTestCaseDto åt testet.
def test_get_all_test_cases__should_return_a_list_of_test_cases(valid_test_case_dto):

    #arrange
    #skapar en instans av repository
    repository = TestCaseRepository()
    #skapar ett TestCase objekt med hjälp av fixturen i pytest. create() överför värdena från dto till testfallsobjektet
    # och returnerar det.
    test_case = TestCase().create(valid_test_case_dto)

    #act
    # här lagrar vi testfallet i repository listan.
    repository.try_create_test_case(test_case)
    # hämtar listan från repositoryt och sparar den i result.
    result = repository.get_all_test_cases()

    #assert
    #Kontrollerar att den returnerade listan innehåller exakt det testfall som lagrades.
    assert result == [test_case]

# Returnera en KOPIA av listan [TestCase]. Säkerställning av att ändringar i den returnerade listan inte påverkar repositoryts interna lista.
def test_get_all_test_cases__should_return_a_copy_of_test_cases(valid_test_case_dto):

    #arrange
    #skapar ett nytt repository.
    repository = TestCaseRepository()
    #skapar ett testfallsobjekt från den giltiga dton.
    test_case = TestCase().create(valid_test_case_dto)
    #lägger in testfallsobjektet i repositoryts interna lista.
    repository.try_create_test_case(test_case)

    #act
    #hämtar listan från repositoryt och sparar den i result.
    result = repository.get_all_test_cases()
    #clear rensar listan.
    result.clear()

    #assert
    # kontrollerar att listan är tom.
    assert len(result) == 0
    # kontrollerar att repository fortfarande innehåller ett testfall
    assert len(repository.get_all_test_cases()) == 1

# Lagra och hämta flera testfall i rätt ordning.
def test_get_all_test_cases__should_be_able_to_store_multiple_test_cases(valid_test_case_dto):

    #arrange
    #skapar tomt repository.
    repository = TestCaseRepository()
    #skapar det första testfallet från fixturen (valid_test_case_dto)
    first_test_case = TestCase().create(valid_test_case_dto)

    #skapar en ny dto för det andra testfallet.Det behövs en separat dto eftersom det andra testfallet ska ha egna värden.
    second_dto = CreateTestCaseDto()
    second_dto.tc_id = "TC-002"
    second_dto.title = "Testning av logout"
    second_dto.purpose = "Verifiering av logout funktion"
    second_dto.acceptance_criteria = "Användare ska kunna logga ut"
    second_dto.preconditions = "Användare är inloggad"
    second_dto.test_data = "Användaren ska existera"
    second_dto.steps = "1. Klicka på logout"
    second_dto.expected_result = "Användaren kan logga ut och återvänder till log in sidan"

    #här skapar vi det andra TestCase objektet från den andra dton
    second_test_case = TestCase().create(second_dto)

    #act
    #här lagras båda testcasen i repositoryt.
    repository.try_create_test_case(first_test_case)
    repository.try_create_test_case(second_test_case)
    #Hämtar listan med båda testfallen
    result = repository.get_all_test_cases()

    #assert
    # kontrollerar att listan innehåller exakt 2st testfall
    assert len(result) == 2
    # kontrollerar både att rätt objekt finns i listan och att de ligger i rätt ordning.
    assert result == [first_test_case, second_test_case]