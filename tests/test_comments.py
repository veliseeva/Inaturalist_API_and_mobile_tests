import allure
from allure_commons.types import Severity


@allure.epic("API Tests")
@allure.feature("Comments")
@allure.title("Успешное создание комментария к наблюдению")
@allure.severity(Severity.CRITICAL)
def test_create_a_comment(api, temp_observation):
    with allure.step("Отправляем комментарий"):
        comment_payload = {
            "comment": {
                "parent_type": "Observation",
                "parent_id": temp_observation,
                "body": "This is an automated test comment"
            }
        }
        response = api.post("/comments", json=comment_payload)

    with allure.step("Проверяем успешную публикацию (статус 200)"):
        assert response.status_code == 200, f"Неверный статус-код: {response.status_code}"

    with allure.step("Проверяем, что сервер вернул UUID нового комментария"):
        response_data = response.json()

    results = response_data.get('results', [])
    assert results, f"В ответе нет результатов или массив пуст. Ответ сервера: {response_data}"

    comment_uuid = results[0].get('uuid')
    assert comment_uuid, "Сервер не вернул UUID созданного комментария"
