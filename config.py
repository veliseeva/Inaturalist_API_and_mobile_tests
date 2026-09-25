import logging
from typing import Literal
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from appium.options.android import UiAutomator2Options

CURRENT_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = CURRENT_DIR / ".env"
APP_PATH = str(CURRENT_DIR / "iNaturalist-release.apk")

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    bs_user: str = ""
    bs_key: str = ""
    bs_app_id: str = ""
    bs_url_api: str = "https://api-cloud.browserstack.com/app-automate/sessions/"
    bs_platform_version: str = "13.0"
    bs_device_name: str = "OnePlus 11R"

    my_local_udid: str = ""
    my_emulator_name: str = "emulator-5554"

    timeout: float = 15.0
    local_url: str = "http://127.0.0.1:4723"
    bstack_url: str = "http://hub.browserstack.com/wd/hub"

    inat_username: str = ""
    inat_password: str = ""
    inat_app_id: str = ""
    inat_app_secret: str = ""

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, env_file_encoding='utf-8')


settings = Settings()


def get_mobile_options(context: Literal["bstack", "emulator", "real", "selenoid"]) -> UiAutomator2Options:
    options = UiAutomator2Options()

    options.set_capability("appium:autoGrantPermissions", True)
    options.set_capability("appium:newCommandTimeout", 120)
    options.set_capability("appium:disableWindowAnimation", True)
    options.set_capability("appium:waitForIdleTimeout", 5000)
    options.set_capability("appium:appWaitActivity", "*")
    options.set_capability("appium:noReset", False)

    if context == "bstack":
        options.set_capability("appium:appPackage", "org.inaturalist.android")
        options.set_capability("appium:deviceName", settings.bs_device_name)
        options.set_capability("appium:platformVersion", settings.bs_platform_version)
        options.set_capability("appium:app", settings.bs_app_id)
        options.set_capability("bstack:options", {
            "userName": settings.bs_user,
            "accessKey": settings.bs_key,
            "projectName": "iNaturalist Mobile",
            "buildName": "Android Build",
            "sessionName": "Test Run"
        })

    elif context == "emulator":
        options.set_capability("appium:deviceName", settings.my_emulator_name)
        options.set_capability("appium:app", APP_PATH)
        options.set_capability("appium:appWaitDuration", 40000)

    elif context == "real":
        options.set_capability("appium:udid", settings.my_local_udid)
        options.set_capability("appium:appPackage", "org.inaturalist.android")
        options.set_capability("appium:appActivity", ".ObservationListActivity")
        options.set_capability("appium:uiautomator2ServerLaunchTimeout", 90000)
        options.set_capability("appium:adbExecTimeout", 60000)

    return options
