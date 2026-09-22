from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have
from config import settings
import allure


class MobileAuthorizationPage:
    def __init__(self):
        self.PKG = "org.inaturalist.android:id"
        self.menu_login_btn = browser.element((AppiumBy.ID, f"{self.PKG}/menu_login"))
        self.login_with_email_btn = browser.element((AppiumBy.ID, f"{self.PKG}/login_with_email"))

        self.username_field = browser.element((AppiumBy.ID, f"{self.PKG}/username"))
        self.password_field = browser.element((AppiumBy.ID, f"{self.PKG}/password"))
        self.sign_in_btn = browser.element((AppiumBy.ID, f"{self.PKG}/sign_up"))
        self.side_menu_username = browser.element((AppiumBy.ID, f"{self.PKG}/side_menu_username"))

    @allure.step("Переходим к форме авторизации по Email")
    def go_to_the_authorization_menu(self):
        self.menu_login_btn.click()
        self.login_with_email_btn.click()
        return self

    @allure.step("Вводим учетные данные")
    def login_with_credentials(self, username=settings.inat_username, password=settings.inat_password):
        self.username_field.type(username)
        self.password_field.type(password)
        self.sign_in_btn.click()
        return self

    @allure.step("Проверяем, что пользователь авторизован")
    def user_should_be_authorized(self, expected_username=settings.inat_username):
        self.side_menu_username.should(have.text(expected_username))
        return self


authorization_page = MobileAuthorizationPage()
