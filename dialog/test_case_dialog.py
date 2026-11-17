from utils.console_helper import pause, clear_screen, required_input
from services.test_case_service import TestCaseService
from models.test_case import TestCase


class TestCaseDialog:
    def __init__(self, test_case_service: TestCaseService):
        self.test_case_service = test_case_service

    def main_menu(self):

        while True:
            clear_screen()

            print("#### Main menu - Test case liberator ####")
            print("1. Create a test case.")
            print("2. Show a list of all test cases that have been registered.")
            print("0. Exit.")
            print("")

            option = input("Choose an option: ").strip()

            match option:

                case "1":
                    self.create_test_case_menu()

                case "2":
                    self.show_test_cases()

                case "0":
                    return

                case _:
                    print("Invalid option. Please try again")
                    pause()

    def create_test_case_menu(self):
        
        test_case = TestCase()
        test_case.tc_id = required_input("Enter an id for the test case, for example: TC-001.\n")
        test_case.title = required_input("Enter a title for the test case, for example: What is being tested? \n")
        test_case.purpose = required_input("Enter a purpose for the test case, for example: Why is this being tested? \n")
        test_case.acceptance_criteria = required_input("Enter a acceptance citeria for the test case, for example: Which acceptance criteria does the test cover?  \n")
        test_case.preconditions = required_input("Enter the preconditions for the test case, for example: Windows version? Browser type and version? \n")
        test_case.test_data = required_input("Enter the test data for the test case, for example: If you used a specific search word? \n")
        test_case.steps = required_input("Enter the steps to recreate the test case, for example: Which exact steps is off importance to the test? \n")
        test_case.expected_result = required_input("Enter the expected result of the test case, for example: What does the demands specify? \n")

        result = self.test_case_service.create_test_case(test_case)
        print(result.message)
        pause()


    def show_test_cases(self):

        while True:
            clear_screen()
            print("#### List of test cases - Test case liberator ####")
            print("These are the test cases registered for this session:\n")

            result = self.test_case_service.get_test_cases()

            if not result:
                print("No test cases registered.")
                pause()
                return

            counter = 1

            for test_case in result:
                print(f"{counter}. {test_case.tc_id}")
                counter +=1

            print("\n0. Back")

            option = input("\n Choose a test case to open: ").strip()

            if option == "0":
                return

            if not option.isdigit():
                print("Invalid input. Please try again.")
                pause()
                continue

            index = int(option) - 1

            test_case = self.test_case_service.get_test_case_by_index(index)

            if test_case is not None:
                self.show_test_case_details(test_case)
            else:
                print("Test case not found. Please try again.")
                pause()

    def show_test_case_details(self, test_case):
        while True:
            clear_screen()

            print("#### Test case details ####\n")

            print(f"UUID4: {test_case.id}")
            print(f"ID: {test_case.tc_id}")
            print(f"Title: {test_case.title}")
            print(f"Purpose: {test_case.purpose}")
            print(f"Acceptance criteria: {test_case.acceptance_criteria}")
            print(f"Preconditions: {test_case.preconditions}")
            print(f"Test Data: {test_case.test_data}")
            print(f"Steps: {test_case.steps}")
            print(f"Expected Result: {test_case.expected_result}")
            
            print("\n0.Back")

            option = input("Choose an option: ").strip()

            match option:

                case "0":
                    return
