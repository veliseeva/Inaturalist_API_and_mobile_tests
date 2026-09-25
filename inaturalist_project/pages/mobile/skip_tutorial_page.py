import time
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be
from inaturalist_project.utils.gestures import swipe_left

SWIPE_TEXT_LOCATOR = (AppiumBy.ID, 'org.inaturalist.android:id/swipe_text')
SKIP_BUTTON_LOCATOR = (AppiumBy.ID, 'org.inaturalist.android:id/skip')


@allure.step("Пропуск онбординга (туториала)")
def skip_tutorial_safely():
    tutorial_trigger = browser.element(SWIPE_TEXT_LOCATOR)

    if not tutorial_trigger.with_(timeout=8.0).wait_until(be.visible):
        allure.attach("Skipped", name="Onboarding Status", attachment_type=allure.attachment_type.TEXT)
        return

    try:
        with allure.step("Инициализация туториала"):
            tutorial_trigger.click()

        with allure.step("Динамический поиск кнопки Skip"):
            skip_btn = browser.element(SKIP_BUTTON_LOCATOR)

            for _ in range(5):
                if skip_btn.with_(timeout=1.0).wait_until(be.visible):
                    break
                swipe_left()
                time.sleep(0.4)

        with allure.step("Подтверждение пропуска"):
            for step in range(1, 4):
                if skip_btn.with_(timeout=2.0).wait_until(be.visible):
                    allure.attach(f"Click Skip #{step}", name="Action", attachment_type=allure.attachment_type.TEXT)
                    browser.driver.find_element(*SKIP_BUTTON_LOCATOR).click()
                    time.sleep(1.0)
                else:
                    break

    except Exception as e:
        allure.attach(str(e), name="Tutorial Error", attachment_type=allure.attachment_type.TEXT)