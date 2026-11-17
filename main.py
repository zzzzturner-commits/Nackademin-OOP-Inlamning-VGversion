from services.test_case_service import TestCaseService
from repository.test_case_repository import TestCaseRepository
from dialog.test_case_dialog import TestCaseDialog

def main():

    test_case_repository = TestCaseRepository()
    test_case_service = TestCaseService(test_case_repository)
    test_case_dialogs = TestCaseDialog(test_case_service)

    test_case_dialogs.main_menu()

    
if __name__ == "__main__":
    main()