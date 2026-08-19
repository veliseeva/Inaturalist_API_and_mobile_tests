import allure
from allure_commons.types import Severity


@allure.epic("API Tests")
@allure.feature("Search")
@allure.title("Проверка глобального поиска (Поиск таксона)")
@allure.severity(Severity.BLOCKER)
def test_global_search_taxa(api):
    with allure.step("Отправляем поисковый запрос 'Огарь' (только по таксонам)"):
        params = {
            "q": "Огарь",
            "sources": "taxa",
            "fields": "taxon.name,taxon.preferred_common_name"
        }
        response = api.get("/search", params=params)

    with allure.step("Проверяем успешный ответ"):
        assert response.status_code == 200
        body = response.json()
        assert body['total_results'] > 0, "Ничего не найдено!"

    with allure.step("Проверяем наличие запрошенных полей в ответе"):
        first_result = body['results'][0]['taxon']
        assert 'name' in first_result
        assert 'preferred_common_name' in first_result
        assert "Огарь" in first_result.get('preferred_common_name', '')
