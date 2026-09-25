import time
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be
from inaturalist_project.utils.gestures import swipe_left

SWIPE_TEXT_LOCATOR = (AppiumBy.ID, 'org.inaturalist.android:id/swipe_text')
SKIP_BUTTON_LOCATOR = (AppiumBy.ID, 'org.inaturalist.android:id/skip')


@allure.step("Пропуск онбординга (туториала)")
@allure.step("Пропуск онбординга (туториала)")
def skip_tutorial_safely():
    time.sleep(3.0)

    tutorial_trigger = browser.element(SWIPE_TEXT_LOCATOR)
    if not tutorial_trigger.with_(timeout=10.0).wait_until(be.visible):
        allure.attach(
            "Passed",
            name="Onboarding Status",
            attachment_type=allure.attachment_type.TEXT
        )
        return

    try:
        with allure.step("Инициализация туториала"):
            tutorial_trigger.click()
            time.sleep(1.5)

        with allure.step("Листаем экраны"):
            for _ in range(4):
                swipe_left()
                time.sleep(1.2)

        with allure.step("Закрываем онбординг"):
            skip_btn = browser.element(SKIP_BUTTON_LOCATOR)

            for step in range(1, 4):
                if not skip_btn.with_(timeout=4.0).wait_until(be.visible):
                    break

                allure.attach(
                    f"Skip #{step}",
                    name="Onboarding Step",
                    attachment_type=allure.attachment_type.TEXT
                )
                skip_btn.click()
                time.sleep(1.5)

    except Exception as e:
        allure.attach(
            str(e),
            name="Error",
            attachment_type=allure.attachment_type.TEXT
        )