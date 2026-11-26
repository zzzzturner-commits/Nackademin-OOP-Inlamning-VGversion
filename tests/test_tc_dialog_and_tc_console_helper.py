from unittest.mock import Mock, patch
from dialogs.tc_dialog import TestCaseDialog
from utils.tc_console_helper import required_input
from tests.conftest import valid_test_case_dto
from models.tc_test_case import TestCase


# kontroll av att dialogen skickar användarens inmatning till servicen.
def test_create_test_case_menu__should_send_user_input_to_service():

    #arrange
    # Här skapas en mock av servicen.
    #Anledningen till att en mock skapas är att kunna testa dialogens beteende utan att testa servicens logik en gång till.
    service = Mock()
    service.create_test_case.return_value.message = "Test case created successfully."

    #mock objektet skickas in som beroende till dialogen.
    dialog = TestCaseDialog(service)

    user_inputs = [
        "TC-001",
        "Login test",
        "Verifiera login",
        "Användare kan logga in",
        "Användarkonto existerar",
        "Inloggningsuppgifter",
        "Skriv in inloggningsuppgifter",
        "Användaren kan logga in"
    ]

    #act
        # patch är en funktion från Python biblioteket unittest.mock
         #2 Här simuleras requierd_input tillfälligt då den returnerar de fördefinierade testvärdena.
         #3 Här simuleras pause()
    with patch("builtins.input", side_effect=user_inputs), \
         patch("dialogs.tc_dialog.required_input", side_effect=user_inputs), \
         patch("dialogs.tc_dialog.pause"):

        dialog.create_test_case_menu()

    #assert
    # kontroll att dialogen anropade servicen en gång.
    service.create_test_case.assert_called_once()

    # första argumentet skickas till create_test_case.
    dto = service.create_test_case.call_args[0][0]

    #Kontroll över att värdet överförts korrekt
    assert dto.tc_id == "TC-001"
    #Kontroll över att värdet överförts korrekt
    assert dto.title == "Login test"
    #Kontroll över att värdet överförts korrekt
    assert dto.purpose == "Verifiera login"

# Kontroll att tom lista visas när inga testfall finns.
def test_show_test_cases__should_display_message_when_repository_is_empty():

    #arrange
    # Här skapas en mock av servicen.
    # Anledningen till att en mock skapas är att kunna testa dialogens beteende utan att testa servicens logik en gång till.
    service = Mock()
    # Här bestäms vad som ska returneras när dialogen anropar get_test_cases()
    # Vi simulerar att repositoryt är tomt
    service.get_test_cases.return_value.test_cases = []

    dialog = TestCaseDialog(service)

    #act
    # builtins.input simulerar att användaren matar in "0"
    # clear_screen förhindrar att terminalen rensas
    # pause förhindrar att testet väntar på en tangenttryckning
    # builtins.print gör det möjligt att kontrollera vad dialogen skriver ut.
    with patch("builtins.input", return_value="0"), \
         patch("dialogs.tc_dialog.clear_screen"), \
         patch("dialogs.tc_dialog.pause"), \
         patch("builtins.print") as mocked_print:
        
    #själva metoden som ska testas
        dialog.show_test_cases()

   #assert
    #kontrollerar att dialogen anropar servicen exakt en gång.
    service.get_test_cases.assert_called_once()
    #Kontroll att dialogen skriver ut rätt meddelande när listan är tom.
    mocked_print.assert_any_call("No test cases registered.")

# kontroll att registrerade testfall visas och ett testfall kan öppnas
def test_show_test_cases__should_display_registered_test_cases(valid_test_case_dto):

    #arrange
    # Här skapas en mock av servicen.
    # Anledningen till att en mock skapas är att kunna testa dialogens beteende utan att testa servicens logik en gång till.
    service = Mock()
    # här skapas ett riktigt testfall med hjälp av fixturen
    test_case = TestCase().create(valid_test_case_dto)

    # här skapas ett simulerat resultat från servicen
    # vilket motsvarar GetTestCaseResult
    get_result = Mock()
    get_result.test_cases = [test_case]
    # Här bestäms att mockservicen ska returnerar get_result när get_test_cases anropas.
    service.get_test_cases.return_value = get_result

    #Här skapas den simulerade dialogen och skickas till den simulerade servicen.
    dialog = TestCaseDialog(service)

    #act
    # builtins.input simulerar att användaren matar in "0".
    # clear_screen förhindrar att terminalen rensas.
    # pause förhindrar att testet väntar på en tangenttryckning.
    # builtins.print gör det möjligt att kontrollera vad dialogen skriver ut.
    with patch("builtins.input", return_value="0"), \
         patch("dialogs.tc_dialog.clear_screen"), \
         patch("dialogs.tc_dialog.pause"), \
         patch("builtins.print") as mocked_print:

        #själva metoden som ska testas.
        dialog.show_test_cases()

    #assert
    # kontrollerar att dialogen hämtar ut ett testfall från servicen, ecakt en gång.
    service.get_test_cases.assert_called_once()
    # kontrollerar att dialogen skrivit ut testfallet med rätt löpnummer och testfalls id.
    mocked_print.assert_any_call(f"1. {test_case.tc_id}")

# Kontroll att korrekta detaljer visas av ett testfall
def test_show_test_case_details__should_open_selected_test_case(valid_test_case_dto):

    #arrange
    # Här skapas en mock av servicen.
    # Anledningen till att en mock skapas är att kunna testa dialogens beteende utan att testa servicens logik en gång till.
    service = Mock()
    # här skapas ett riktigt testfall med hjälp av fixturen
    test_case = TestCase().create(valid_test_case_dto)

    # här skapas ett simulerat resultat från servicen
    # vilket motsvarar GetTestCaseResult
    get_result = Mock()
    get_result.test_cases = [test_case]
    # Här bestäms att mockservicen ska returnerar get_result när get_test_cases anropas.
    service.get_test_cases.return_value = get_result
    #När dialogen frågar servicen efter testfallet på ett visst index får den tillbaka testfallsobjektet.
    service.get_test_case_by_index.return_value = test_case

    #Här skapas den simulerade dialogen och skickas till den simulerade servicen.
    dialog = TestCaseDialog(service)

    #act
    # builtins.input simuleras två anvädarval "1"(väljer det första testfallet) och "0"(användaren går tillbaka från listan).
    # clear_screen förhindrar att terminalen rensas.
    # pause förhindrar att testet väntar på en tangenttryckning.
    # builtins.print gör det möjligt att kontrollera vad dialogen skriver ut.
    with patch("builtins.input", side_effect=["1", "0"]), \
         patch("dialogs.tc_dialog.clear_screen"), \
         patch("dialogs.tc_dialog.pause"), \
         patch("dialogs.tc_dialog.print", create=True), \
         patch.object(dialog, "show_test_case_details") as mocked_details:

        #själva metoden som ska testas.
        dialog.show_test_cases()


    #assert
    # kontrollerar att dialogen frågade efer rätt index.
    service.get_test_case_by_index.assert_called_once_with(0)
    # kontrollerar att dialogen försökte öppna detaljvyn med just det testfall som användaren valde.
    mocked_details.assert_called_once_with(test_case)

#Visa testfalls detaljer
def test_show_test_case_details__should_display_test_case_information(valid_test_case_dto):
    
    #arrange
    # Här skapas en mock av servicen.
    # Anledningen till att en mock skapas är att kunna testa dialogens beteende utan att testa servicens logik en gång till.
    service = Mock()
    # här skapas ett riktigt testfall med hjälp av fixturen
    test_case = TestCase().create(valid_test_case_dto)

    #Här skapas den simulerade dialogen och skickas till den simulerade servicen.
    dialog = TestCaseDialog(service)

    #act
    # builtins.input simulerar att användaren matar in "0".
    # clear_screen förhindrar att terminalen rensas.
    # pause förhindrar att testet väntar på en tangenttryckning.
    # builtins.print gör det möjligt att kontrollera vad dialogen skriver ut.
    with patch("builtins.input", return_value="0"), \
         patch("dialogs.tc_dialog.clear_screen"), \
         patch("builtins.print") as mocked_print:

        #själva metoden som ska testas
        dialog.show_test_case_details(test_case)

    #assert
    #1 Här kontrolleras att samtliga 9 infomationsfält visas korrekt
    mocked_print.assert_any_call(f"UUID4: {test_case.id}")
    #2 Här kontrolleras att samtliga 9 infomationsfält visas korrekt
    mocked_print.assert_any_call(f"ID: {test_case.tc_id}")
    #3 Här kontrolleras att samtliga 9 infomationsfält visas korrekt
    mocked_print.assert_any_call(f"Title: {test_case.title}")
    #4 Här kontrolleras att samtliga 9 infomationsfält visas korrekt
    mocked_print.assert_any_call(f"Purpose: {test_case.purpose}")
    #5 Här kontrolleras att samtliga 9 infomationsfält visas korrekt
    mocked_print.assert_any_call(f"Acceptance criteria: {test_case.acceptance_criteria}")
    #6 Här kontrolleras att samtliga 9 infomationsfält visas korrekt
    mocked_print.assert_any_call(f"Preconditions: {test_case.preconditions}")
    #7 Här kontrolleras att samtliga 9 infomationsfält visas korrekt
    mocked_print.assert_any_call(f"Test Data: {test_case.test_data}")
    #8 Här kontrolleras att samtliga 9 infomationsfält visas korrekt
    mocked_print.assert_any_call(f"Steps: {test_case.steps}")
    #9 Här kontrolleras att samtliga 9 infomationsfält visas korrekt
    mocked_print.assert_any_call(f"Expected Result: {test_case.expected_result}")

# Kontroll av registreringen av ett testfall via dialogen.
def test_create_test_case_menu__should_send_dto_to_service(valid_test_case_dto):
    
    #arrange
    # Här skapas en mock av servicen.
    # Anledningen till att en mock skapas är att kunna testa dialogens beteende utan att testa servicens logik en gång till.
    service = Mock()
    # Här bestämmer vi vad den simulerade servicen ska returnerar
    service.create_test_case.return_value.message = "Test case successfully created."

    #här skapas dialog objektet och skickar in vår mock service
    dialog = TestCaseDialog(service)

    #Här simuleras användarens inmatning
    #Görs pga required_input()
    #det simulerar användarens inmatning utan att testet behöver vänta på riktig tangentbordsinmatning.
    user_inputs = [
        valid_test_case_dto.tc_id,
        valid_test_case_dto.title,
        valid_test_case_dto.purpose,
        valid_test_case_dto.acceptance_criteria,
        valid_test_case_dto.preconditions,
        valid_test_case_dto.test_data,
        valid_test_case_dto.steps,
        valid_test_case_dto.expected_result
    ]

    #act
    #ersätter required_input() med en simulerad funktion
    #ersätter paus() så att testet inte stannar och väntar på användaren.
    #ersätter print med mocked print
    with patch("dialogs.tc_dialog.required_input", side_effect=user_inputs), \
         patch("dialogs.tc_dialog.pause"), \
         patch("builtins.print") as mocked_print:

        #Själva funktionen
        dialog.create_test_case_menu()

    #assert
    # kontrollerar att servicen endast anropas en gång.
    # det är vioktigt för att dialogen ska lämna över registreringen till servicen.
    service.create_test_case.assert_called_once()

    #hämtar dto-objektet som skickades till servicen.
    #call_args används för att hämta informationen som skickades vid anropet.
    #call args hämtar argumenten som skickades vid första anropet.
    #.args hämtar de positionella argumenten.
    #[0] hämtar det första argumentet.
    submitted_dto = service.create_test_case.call_args.args[0]

    #kontrollera dto:ts innehåll.
    assert submitted_dto.tc_id == valid_test_case_dto.tc_id
    assert submitted_dto.title == valid_test_case_dto.title
    assert submitted_dto.purpose == valid_test_case_dto.purpose
    assert submitted_dto.acceptance_criteria == valid_test_case_dto.acceptance_criteria
    assert submitted_dto.preconditions == valid_test_case_dto.preconditions
    assert submitted_dto.test_data == valid_test_case_dto.test_data
    assert submitted_dto.steps == valid_test_case_dto.steps
    assert submitted_dto.expected_result == valid_test_case_dto.expected_result

    # kontrollera meddelandet till användaren.
    mocked_print.assert_any_call("Test case successfully created.")

# kontroll av required_input.strip()
def test_required_input__should_return_value_whitout_surrounding_whitespace():

    #arrange
    #här skapas en lista med det värde som simuleras att användaren skriver in.
    #Anledningen till att det är en lista är att side_effect tillsammans med patch gör att flera anrop kan simuleras till input()
    #Här simuleras dock bara ett värde eftersom funktionen endast behöver ett användaranrop för att få giltig inmatning
    user_inputs = ["  Login test  "]

    #act
    # patch är en funktion från Python biblioteket unittest.mock
    # anvnds för att tillfälligt ersätta en funktion eller objekt under testets körning
    # Här ersätter det vanliga input() och simulerar ("Enter title")
    # input() är en inbyggd funktion från python. hittas under builtins.
    with patch ("builtins.input", side_effect=user_inputs) as mocked_input:
        result = required_input("Enter title")


    #assert
    # kontroll att funktionen returnerar rätt värde
    assert result == "Login test"

# kontroll att required_input repeterar att inmatningen är tom.
def test_required_input__should_repeat_when_input_is_empty():

    #arrange
    # här simuleras tre användarinmatningar.
    user_inputs = ["", "Press Enter", "Login test"]

    #act
    # mocked input sparar referens till vårt mock objekt i variabeln.
    #3 inputs
    with patch("builtins.input", side_effect=user_inputs) as mocked_input:
        result = required_input("Enter title")

    #assert
    # kontroll att funktionen till slut returnerade den giltiga inmatningen
    assert result == "Login test"
    # hur många ggr som den simulerade funktionen anropats.
    assert mocked_input.call_count == 3