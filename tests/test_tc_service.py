from services.tc_service import TestCaseService
from repository.tc_repository import TestCaseRepository
from models.tc_test_case import TestCase
# import av pytest för att få parametrize att fungera.
import pytest

#Lyckad registrering av testfall.
def test_create_test_case__should_create_and_store_test_case(valid_test_case_dto):

    #arrange
    #Här skapas ett nytt repository och en service som använder repositoryt.
    repository = TestCaseRepository()
    service = TestCaseService(repository)

    #act
    result = service.create_test_case(valid_test_case_dto)

    #assert
    #1 kontroll av att registreringen rapporteras som lyckad (CreateTestCaseResult) True = Lyckad registrering.
    assert result.succeeded is True
    #2 kontroll av att test_case faktiskt innehåller ett objekt av typen TestCase. En säkerställning av att
    # rätt typ av objektet returneras.
    assert isinstance(result.test_case, TestCase)
    #3 kotroll av att repository innehåller exakt 1 testfall.
    assert len(repository.get_all_test_cases()) == 1
    #4 verifiering av att samma objekt som returneras är det faktiska objektet som lagrades i repository.
    # == jämför om två objekt har samma värde.
    # is kontrollerar om två variabler refererar till exakt samma objekt i minnet.
    assert repository.get_all_test_cases()[0] is result.test_case

#Validering av obligatoriska fält.

# funktion i pytest. gör det möjligt att köra samma testfunktion flera gånger med olika värden.
# istället för att skriva 8st separata testfunktioner skrivs testet en gång och låter pytest utföra det 8 gånger.
# "field" är namnet på parametern som ska ta emot värdena från listan.
@pytest.mark.parametrize("field",[
        "tc_id",
        "title",
        "purpose",
        "acceptance_criteria",
        "preconditions",
        "test_data",
        "steps",
        "expected_result"
    ])

    #Stötte på ett problem med detta test och fick testa många olika saker. det visade sig att jag hade stavat fel i 
    # parametrize på acceptance criteria. Två r istället för ett. 
def test_create_test_case__should_fail_when_required_input_field_is_missing(valid_test_case_dto, field):

    #arrange
    #Här skapas ett nytt repository och en service som använder repositoryt.
    repository = TestCaseRepository()
    service = TestCaseService(repository)

    # setattr() är en inbyggd funktion i Pyrhon som används för att tilldela ett värde till ett attribut på ett objekt.
    # Här använder vi field från parametrize för att välja vilket attribut på valid_test_case_dto som ska ändras.
    # Vi tilldelar sedan en tom sträng ("") till det attributet för att simulera att ett obligatoriskt fält saknas.
    setattr(valid_test_case_dto, field, "")

    #act
    result = service.create_test_case(valid_test_case_dto)
 
    #assert
    #1 kontroll ifall service rapporterar vid misslyckad registrering.
    assert result.succeeded is False
    #2 kontroll av att inget TestCase objekt returneras.
    assert result.test_case is None
    #3  kontroll att repositoryn är tom.
    assert repository.get_all_test_cases() == []

#Kontroll av att servicen inte registrerar ett testfall när valideringen misslyckas.
def test_create_test_case__should_not_store_test_cases_when_validation_fails(valid_test_case_dto):

    #arrange
    #Här skapas ett nytt repository och en service som använder repositoryt.
    repository = TestCaseRepository()
    service = TestCaseService(repository)

    #titeln ändras här till en tom sträng för att medvetet trigga valideringen i servicen.
    valid_test_case_dto.title = ""

    #act
    result = service.create_test_case(valid_test_case_dto)

    #assert
    #1 Servicen ska upptäcka att title saknas och returnera ett misslyckat resultat
    assert result.succeeded is False
    #2 Kontroll att listan från repositoryt är tom.
    #  Verifiering att servicen inte har sparat något testfall trots att registreringen påbörjades.
    assert repository.get_all_test_cases() == []

#Hämtning av testfall när repositoryt är tomt.
def test_get_test_cases__should_return_empty_list_when_no_test_cases_exists():

    #arrange
    #Här skapas ett nytt repository och en service som använder repositoryt.
    repository = TestCaseRepository()
    service = TestCaseService(repository)

    #act
    result = service.get_test_cases()

    #assert
    #1 Kontroll att operationen genomförts korrekt.
    assert result.succeeded is True
    #2 Kontroll att resultatet innehåller en tom lista.
    assert result.test_cases == []
    #3 Kontroll av att rätt meddelande returneras vid en tom lista.
    # fick ett assertion error till en början. Hade glömt punkten.
    assert result.message == "No test cases registered."

#Kontroll att servicen returnerar samtliga registrerade testfall.
def test_get_test_cases__should_return_all_registered_test_cases(valid_test_case_dto):

    #arrange
   #Här skapas ett nytt repository och en service som använder repositoryt.
    repository = TestCaseRepository()
    service = TestCaseService(repository)

    #Här skapas två testfalls objekt med hjälp av samma dto.
    #även ifall de innehåller samma information så får de olika UUID då varje TestCase få ett eget ID.
    test_case_1 = TestCase().create(valid_test_case_dto)
    test_case_2 = TestCase().create(valid_test_case_dto)

    #Här sparas objekten in i repositoryns interna lista.
    repository.try_create_test_case(test_case_1)
    repository.try_create_test_case(test_case_2)

    #act
    result = service.get_test_cases()

    #assert
    #1 Kontroll att hämtningen genomförts framgångsrikt. 
    assert result.succeeded is True
    #2 len används för att kontrollera antalet objekt i listan. 2st objekt i listan test_cases.
    assert len(result.test_cases) == 2
    #3 Här används is för att kontrollera objektens identitet. kontroll att objekten som skpades är samma som returneras.
    assert result.test_cases[0] is test_case_1
    #4 Här används is för att kontrollera objektens identitet. kontroll att objekten som skpades är samma som returneras.
    assert result.test_cases[1] is test_case_2
    #5 Kontroll av att rätt meddelande retuneras.
    assert result.message == "Test cases retrieved successfully."

# Kontroll att servicen avvisar fält som bara innehåller mellanslag.
# avancerat negativt test.
# Då detta test failade med ett assertion error och identifierade en brist i nuvarande kod ändrades koden i tc_service
# från if not test_case_dto.title
# till if not test_case_dto.title.strip()
# då precondition,test_data och step tekniskt sett är listor i nuvarande iteration så fungerar dock inte .strip() på dem.
def test_create_test_case__should_fail_when_required_field_contains_only_whitespace(valid_test_case_dto):

    #arrange
    #Här skapas ett nytt repository och en service som använder repositoryt.
    repository = TestCaseRepository()
    service = TestCaseService(repository)

    # Här ändrar vi så att valid_test_case_dto titeln blir "   " istället för tidigare värde.
    valid_test_case_dto.title = "   "

    #act
    result = service.create_test_case(valid_test_case_dto)

    #assert
    #1 Kontroll av att registreringen avvisas då titeln inte innehåller någon text.
    assert result.succeeded is False
    #2 kontroll av att inget TestCase objekt returneras
    assert result.test_case is None
    #3 kontroll av att inget testfall har sparats.
    assert repository.get_all_test_cases() == []

# Kontroll av att samtliga fält avvisar enbart blanksteg.
# här togs valet att ändra om i dto så att precondition, test data och step blir strings. 
# Orginal iden i TestCase visas fortfarande men för att få ett pass på detta test ändrades dto.
# Anledningen till att ändringen gjordes var för att fortsätta lära mig mer om testning.

@pytest.mark.parametrize("field", [
    "tc_id",
    "title",
    "purpose",
    "acceptance_criteria",
    "preconditions",
    "test_data",
    "steps",
    "expected_result"
    ])

def test_create_test_case__should_fail_when_required_field_contains_only_whitespace(valid_test_case_dto, field):
    
    #arrange
    #Här skapas ett nytt repository och en service som använder repositoryt.
    repository = TestCaseRepository()
    service = TestCaseService(repository)

    # Här anger vi att carje fält i dto ska innehålla 3st mellanslag
    setattr(valid_test_case_dto, field, "   ")

    #act
    result = service.create_test_case(valid_test_case_dto)

    #assert
    #1 servicen ska upptäcka att fältet saknar innehåll då vi nu har .strip() med i valideringen.
    # registreringen ska misslyckas.
    assert result.succeeded is False
    #2 inget testfall ska returneras.
    assert result.test_case is None
    #3 inget testfall ska ha sparats.
    assert repository.get_all_test_cases() == []

# Kontroll att get_test_cases() inte exponerar reåpositoryts interna lista.
def test_get_test_cases__should_return_copy_of_repository_list(valid_test_case_dto):

    #arrange
    #Här skapas ett nytt repository och en service som använder repositoryt.
    repository = TestCaseRepository()
    service = TestCaseService(repository)

    # här skapar vi ett testfall och registrerar det i repositoryt
    test_case = TestCase().create(valid_test_case_dto)
    repository.try_create_test_case(test_case)

    #act
    result = service.get_test_cases()

    #assert
    # clear() är en inbyggd listmetod i Python som tar bort samtliga element ur listan.
    result.test_cases.clear()

    #1 Kontroll av att listan som retuneras av servicen faktiskt är tom
    assert result.test_cases == []
    #2 kontroll av att repositoryt fortfarande innehåller vårt testfall
    assert repository.get_all_test_cases() == [test_case]
    # Testar en "shallow copy"
    # innebär att vi får en ny lista men objektet inuti listan är fortfarande samma objekt.
    # en shallow copy skyddar inte själva testcase objektet från att ändras. den skyddar bara listans struktur.

# kontroll av att informationen från dto överförs korrekt till TestCase objektet.
def test_create_test_case__should_transfer_dto_data_to_test_case(valid_test_case_dto):

    #arrange
    #Här skapas ett nytt repository och en service som använder repositoryt.
    repository = TestCaseRepository()
    service = TestCaseService(repository)

    #act
    result = service.create_test_case(valid_test_case_dto)

    #assert
    #1 kontroll att registreringen lyckats
    assert result.succeeded is True
    #2 Här jämförs informationen så att den överensstämmer
    assert result.test_case.tc_id == valid_test_case_dto.tc_id
    #3 Här jämförs informationen så att den överensstämmer
    assert result.test_case.title == valid_test_case_dto.title
    #4 Här jämförs informationen så att den överensstämmer
    assert result.test_case.purpose == valid_test_case_dto.purpose
    #5 Här jämförs informationen så att den överensstämmer
    assert result.test_case.acceptance_criteria == valid_test_case_dto.acceptance_criteria
    #6 Här jämförs informationen så att den överensstämmer
    assert result.test_case.preconditions == valid_test_case_dto.preconditions
    #7 Här jämförs informationen så att den överensstämmer
    assert result.test_case.test_data == valid_test_case_dto.test_data
    #8 Här jämförs informationen så att den överensstämmer
    assert result.test_case.steps == valid_test_case_dto.steps
    #9 Här jämförs informationen så att den överensstämmer
    assert result.test_case.expected_result == valid_test_case_dto.expected_result

#Hämta testfall med giltigt index.
def test_get_test_cases_by_index__should_return_test_case_when_index_is_valis(valid_test_case_dto):

    #arrange
    #Här skapas ett nytt repository och en service som använder repositoryt.
    repository = TestCaseRepository()
    service = TestCaseService(repository)

    # här skapas och registreras ett testfall.
    test_case = TestCase().create(valid_test_case_dto)
    repository.try_create_test_case(test_case)

    #act
    result = service.get_test_case_by_index(0)

    #assert
    #1 Kontroll av att det returnerade objektet är samma objekt som registrerades.
    # is för att kontrollera objektidentitet.
    assert result is test_case

# Hämta testfall med ogiltigt index
def test_get_test_cases_by_index__should_return_none_when_index_is_invalid(valid_test_case_dto):

    #arrange
    #Här skapas ett nytt repository och en service som använder repositoryt.
    repository = TestCaseRepository()
    service = TestCaseService(repository)

    # här skapas och registreras ett testfall.
    test_case = TestCase().create(valid_test_case_dto)
    repository.try_create_test_case(test_case)

    #act
    result = service.get_test_case_by_index(5)

    #assert
    #1 kontroll av att metoden returnerar None när indexet inte finns.
    assert result is None