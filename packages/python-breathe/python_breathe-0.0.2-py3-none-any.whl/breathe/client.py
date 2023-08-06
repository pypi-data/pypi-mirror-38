import requests

from breathe.exceptions import IncorrectlyConfigured, ConnectionError
from breathe.models import courses, employees

PROD_URL = "https://api.breathehr.com:443/v1/"
SANDBOX_URL = "https://api.sandbox.breathehr.info:443/v1/"


class Client:
    def __init__(self, api_key: str, mode: str = "production"):
        if mode != "production" and mode != "sandbox":
            raise IncorrectlyConfigured("Mode must be one of: production or sandbox")
        if len(api_key) < 48:
            raise IncorrectlyConfigured("Incorrect API key provided")
        self.url = PROD_URL
        if mode == "sandbox":
            self.url = SANDBOX_URL
        self.api_key = api_key

        self.session = requests.Session()
        self.session.headers.update({'X-API-KEY': self.api_key})
        self.employees = employees.Employee(self)
        self.courses = courses.Course(self)
        self._test_connect()

    def _test_connect(self):
        resp = self.request("GET", "divisions")
        if resp.status_code != requests.codes.ok:
            raise ConnectionError(resp.json())

    def request(self, method, endpoint: str, data: dict = None, headers: dict = None, json: dict = None, full_url=False) -> requests.Response:
        if full_url:
            url = endpoint
        else:
            url = self.url + endpoint
        return self.session.request(method, url, data=data, headers=headers, json=json)

