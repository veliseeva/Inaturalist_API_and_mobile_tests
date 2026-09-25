from inaturalist_project.pages.mobile.mobile_observations_page import observation_page
from inaturalist_project.pages.mobile.mobile_settings_page import settings_page
from allure_commons.types import Severity
import allure


@allure.epic("Mobile tests")
@allure.feature("Settings")
@allure.title("Проверка смены языка")
@allure.severity(Severity.CRITICAL)
def test_language_change():
    observation_page.open_the_navigation_panel()
    settings_page.change_language(language='Русский')
    settings_page.observation_bar_should_be_in_the_selected_language(partial_text='Мои наблю')
