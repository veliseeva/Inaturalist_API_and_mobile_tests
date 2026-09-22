from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, be

import allure


class MobileObservationPage:
    def __init__(self):
        self._nav_up_button = (AppiumBy.ACCESSIBILITY_ID, "Navigate up")
        self._explore_tab = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Explore")')
        self._search_button = (AppiumBy.ACCESSIBILITY_ID, 'Search')
        self._taxon_input = (AppiumBy.ID, 'org.inaturalist.android:id/taxon_edit_text')

    def _by_text(self, text: str):
        return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")'

    @allure.step("Открываем панель навигации")
    def open_the_navigation_panel(self):
        browser.element(self._nav_up_button).click()
        return self

    @allure.step("Находим объект")
    def search_for_an_object(self, common_name: str):
        browser.element(self._explore_tab).click()
        browser.element(self._search_button).click()
        browser.element(self._taxon_input).type(common_name)
        return self

    @allure.step("Проверяем нахождения объекта через общеупотребимое и и общее название")
    def common_and_scientific_name_should_be_visible(self, common_name: str, scientific_name: str):
        browser.element(self._by_text(common_name)).should(be.visible)
        browser.element(self._by_text(scientific_name)).should(be.visible)
        return self


observation_page = MobileObservationPage()
