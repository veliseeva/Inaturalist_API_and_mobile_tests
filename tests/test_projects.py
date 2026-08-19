import allure
import pytest
from allure_commons.types import Severity
from jsonschema import validate
from schemas.project_members import members


VALID_PROJECT_IDS = [1234, 3457]


@allure.epic("API Tests")
@allure.feature("Projects")
@pytest.mark.parametrize("project_id", VALID_PROJECT_IDS)
@allure.title("Проверка списка участников проекта (ID: {project_id})")
@allure.severity(Severity.NORMAL)
def test_get_project_members(api, project_id):
    response = api.get(f"/projects/{project_id}/members")

    with allure.step("Проверяем статус 200"):
        assert response.status_code == 200, f"Сервер вернул ошибку: {response.text}"

    body = response.json()

    with allure.step("Проверяем структуру ответа (JSON Schema)"):
        validate(body, members)

    with allure.step("Проверяем наличие участников и их счетчики наблюдений"):
        assert len(body['results']) > 0, "Список участников пуст"

        for item in body['results']:
            assert item['observations_count'] >= 0
            assert item['user']['id'] is not None
