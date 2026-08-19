import allure
from allure_commons.types import Severity
from jsonschema import validate
from schemas.error_users import non_existing_users


@allure.epic("API Tests")
@allure.feature("Users")
@allure.title("Успешная блокировка и разблокировка пользователя")
@allure.severity(Severity.CRITICAL)
def test_remove_a_user_block(api):
    dummy_user_id = 10906574

    with allure.step("Блокируем пользователя (Первый раз)"):
        block_response = api.post(f"/users/{dummy_user_id}/block")
        assert block_response.status_code == 200, f"Сервер вернул ошибку: {block_response.text}"

    with allure.step("Пытаемся заблокировать ещё (Негативный кейс)"):
        block_response_2 = api.post(f"/users/{dummy_user_id}/block")
        assert block_response_2.status_code == 200

    with allure.step("Разблокируем пользователя (Уборка)"):
        unblock_response = api.delete(f"/users/{dummy_user_id}/block")
        assert unblock_response.status_code == 200, f"Сервер вернул ошибку: {unblock_response.text}"

    with allure.step("Пытаемся разблокировать ещё раз (Негативный кейс)"):
        unblock_2 = api.delete(f"/users/{dummy_user_id}/block")
        assert unblock_2.status_code == 422


@allure.epic("API Tests")
@allure.feature("Users")
@allure.title("Негативный: Запрос несуществующего пользователя")
@allure.severity(Severity.NORMAL)
def test_get_non_existent_user(api):
    with allure.step("Отправляем запрос с фейковым ID"):
        response = api.get("/users/9999999999")

    with allure.step("Проверяем статус 404 (Not Found)"):
        assert response.status_code == 404, f"Сервер вернул ошибку: {response.text}"

    with allure.step("Проверяем схему сообщения об ошибке"):
        validate(response.json(), non_existing_users)
