import json
import logging
from typing import Any, Optional, Tuple
from urllib.parse import urljoin

import allure
import requests
from requests import Response

logger = logging.getLogger(__name__)


class AllureLogger:

    @staticmethod
    def _parse_payload(data: Any) -> Tuple[str, allure.attachment_type]:
        if isinstance(data, (bytes, bytearray)):
            data = data.decode("utf-8")
        try:
            parsed = json.loads(data) if isinstance(data, str) else data
            return json.dumps(parsed, indent=4, ensure_ascii=False), allure.attachment_type.JSON
        except (ValueError, TypeError):
            return str(data), allure.attachment_type.TEXT

    @classmethod
    def attach_request_response(cls, response: Response) -> None:
        req = response.request
        duration = round(response.elapsed.total_seconds(), 2)

        logger.info(f"[{response.status_code}] {req.method} {req.url} ({duration}s)")

        allure.attach(
            f"URL: {req.url}\nMethod: {req.method}\nStatus: {response.status_code}\nDuration: {duration}s",
            name="Request Info",
            attachment_type=allure.attachment_type.TEXT,
        )
        if req.body:
            body, attach_type = cls._parse_payload(req.body)
            allure.attach(body, name="Request Body", attachment_type=attach_type)

        if response.text:
            body, attach_type = cls._parse_payload(response.text)
            allure.attach(body, name="Response Body", attachment_type=attach_type)


class APIClient:

    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url.rstrip("/") + "/"
        self.session = requests.Session()
        self._setup_headers(token)

    def _setup_headers(self, token: Optional[str]) -> None:
        self.session.headers.update({
            "User-Agent": "QA_Automation_Portfolio/1.0",
            "Content-Type": "application/json",
        })
        if token:
            self.session.headers["Authorization"] = token

    def _send_request(self, method: str, endpoint: str, **kwargs) -> Response:
        url = urljoin(self.base_url, endpoint.lstrip("/"))

        with allure.step(f"{method.upper()} {endpoint}"):
            response = self.session.request(method, url, **kwargs)
            AllureLogger.attach_request_response(response)
            return response

    def get(self, endpoint: str, **kwargs) -> Response:
        return self._send_request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Response:
        return self._send_request("POST", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Response:
        return self._send_request("DELETE", endpoint, **kwargs)
