from allure_commons.types import Severity
import allure
from inaturalist_project.pages.mobile.mobile_observations_page import observation_page


@allure.epic("Mobile tests")
@allure.feature("Search")
@allure.title("Поиск объекта и проверка его отображения в результатах поиска")
@allure.severity(Severity.BLOCKER)
def test_search():
    observation_page.open_the_navigation_panel()
    observation_page.search_for_an_object(common_name='Marsh frog')
    observation_page.common_and_scientific_name_should_be_visible(
        common_name='Marsh frog',
        scientific_name='Pelophylax ridibundus')
