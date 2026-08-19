import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv('INAT_APP_ID')
APP_SECRET = os.getenv('INAT_APP_SECRET')
USERNAME = os.getenv('INAT_USERNAME')
PASSWORD = os.getenv('INAT_PASSWORD')
USER_AGENT = "QA_Automation_Portfolio/1.0 (Testing by veliseeva)"


def get_inat_jwt_token():
    oauth_payload = {
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "grant_type": "password",
        "username": USERNAME,
        "password": PASSWORD
    }
    oauth_response = requests.post("https://www.inaturalist.org/oauth/token", data=oauth_payload,
                                   headers={"User-Agent": USER_AGENT})
    assert oauth_response.status_code == 200, "Не удалось получить OAuth токен!"
    oauth_token = oauth_response.json()['access_token']

    jwt_response = requests.get("https://www.inaturalist.org/users/api_token",
                                headers={"Authorization": f"Bearer {oauth_token}", "User-Agent": USER_AGENT})
    assert jwt_response.status_code == 200, "Не удалось обменять OAuth на JWT!"

    return jwt_response.json()['api_token']


my_token = get_inat_jwt_token()

print("МОЙ СВЕЖИЙ ТОКЕН:")
print(my_token)
