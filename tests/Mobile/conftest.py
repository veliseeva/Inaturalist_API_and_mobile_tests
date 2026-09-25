import logging
import pytest
import allure
from appium import webdriver
from selene import browser

from config import settings, get_mobile_options
from inaturalist_project.utils import attach
from inaturalist_project.pages.mobile.skip_tutorial_page import skip_tutorial_safely

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default="emulator",
        choices=["bstack", "emulator", "real"],
        help="Окружение для запуска тестов: bstack, emulator или real"
    )


@pytest.fixture(scope="session")
def context(request):
    return request.config.getoption("--context")


@pytest.fixture(scope="function", autouse=True)
def mobile_management(context):

    with allure.step(f"Инициализация Appium сессии [{context}]"):
        options = get_mobile_options(context)
        remote_url = settings.bstack_url if context == "bstack" else settings.local_url

        browser.config.driver = webdriver.Remote(remote_url, options=options)
        browser.config.timeout = settings.timeout
        session_id = browser.driver.session_id

    skip_tutorial_safely()

    yield

    with allure.step("Сбор артефактов (скриншоты, логи)"):
        try:
            attach.add_screenshot(browser)
            attach.add_xml(browser)
        except Exception as e:
            logger.warning(f"Не удалось прикрепить скриншот/XML: {e}")

        if context == "bstack":
            try:
                attach.add_bstack_video(session_id)
            except Exception as e:
                logger.warning(f"Не удалось прикрепить видео из BrowserStack: {e}")

    with allure.step("Закрытие сессии Appium"):
        try:
            browser.quit()
        except Exception as e:
            logger.error(f"Ошибка при закрытии сессии драйвера: {e}")