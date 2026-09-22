from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have
from inaturalist_project.utils.gestures import scroll_to_text
import allure


class MobileSettingPage:
    def __init__(self):
        self._menu_settings = (AppiumBy.ID, 'org.inaturalist.android:id/menu_settings')
        self._language_tab = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Language")')
        self._text_view = (AppiumBy.CLASS_NAME, 'android.widget.TextView')
        self._log_out_button = (AppiumBy.ID, 'android:id/button1')

    @allure.step("Меняем язык")
    def change_language(self, language: str):
        browser.element(self._menu_settings).click()
        browser.element(self._language_tab).click()
        scroll_to_text(language).click()
        return self

    @allure.step("Проверяем, что в навигации сменился язык")
    def observation_bar_should_be_in_the_selected_language(self, widget_text: str):
        browser.element(self._text_view).should(have.text(widget_text))
        return self


settings_page = MobileSettingPage()
