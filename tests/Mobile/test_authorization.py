from inaturalist_project.pages.mobile.mobile_authorization_page import authorization_page
from inaturalist_project.pages.mobile.mobile_observations_page import observation_page
from allure_commons.types import Severity
import allure


@allure.epic("Mobile tests")
@allure.feature("Authorization")
@allure.title("Успешная авторизация")
@allure.severity(Severity.BLOCKER)
def test_successful_authorization():
    observation_page.open_the_navigation_panel()
    authorization_page.go_to_the_authorization_menu()
    authorization_page.login_with_credentials()
    authorization_page.user_should_be_authorized()