import pytest
import allure
from inaturalist_project.utils.request_helper import APIClient
from inaturalist_project.utils.auth import get_inat_jwt_token


@pytest.fixture(scope="session")
def api():
    token = get_inat_jwt_token()
    client = APIClient(base_url="https://api.inaturalist.org/v2", token=token)

    return client


@pytest.fixture(scope="session")
def public_api():
    return APIClient(base_url="https://api.inaturalist.org/v2")


@pytest.fixture
def temp_observation(api):
    obs_uuid = None

    with allure.step("Подготовка: Создаем временное наблюдение"):
        payload = {"observation": {"species_guess": "QA Test", "captive_flag": True}}
        response = api.post("/observations", json=payload)

        assert response.status_code in [200, 201], f"Ошибка создания! {response.text}"
        response_data = response.json()
        print(response_data)

        obs_uuid = response_data['results'][0]['uuid']

    yield obs_uuid

    if obs_uuid:
        with allure.step("Уборка: Удаляем временное наблюдение"):
            api.delete(f"/observations/{obs_uuid}")
