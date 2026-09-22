from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser
import allure


def swipe_left():
    with allure.step("Свайп справа-налево"):
        size = browser.driver.get_window_size()
        width = size['width']
        height = size['height']

        start_x = int(width * 0.9)
        end_x = int(width * 0.1)
        y = int(height * 0.5)

        actions = ActionChains(browser.driver)
        actions.w3c_actions = ActionBuilder(
            browser.driver,
            mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
        )
        actions.w3c_actions.pointer_action.move_to_location(start_x, y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.2)
        actions.w3c_actions.pointer_action.move_to_location(end_x, y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


def scroll_to_text(target_text: str):
    with allure.step(f"Скроллим экран до текста: '{target_text}'"):
        locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("{target_text}"))'
        )
        return browser.element(locator)
