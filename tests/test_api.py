import requests
import subprocess
import time
import unittest


APP_URL = "http://127.0.0.1:5000"
APP_CMD = ["python", "../app.py", "test"]


class TestAPI(unittest.TestCase):
    def setUp(self) -> None:
        self.app_process = subprocess.Popen(APP_CMD)
        time.sleep(1)

    def tearDown(self) -> None:
        self.app_process.terminate()

    def test_index(self) -> None:
        response = requests.get(f"{APP_URL}/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_scraps(self) -> None:
        response = requests.get(f"{APP_URL}/scraps")
        correct_response = [
            {
                "_id": {"$oid": "65298964b01cdb8f5179dc82"},
                "color": "red",
                "fabric_class": "natural",
            },
            {
                "_id": {"$oid": "652af1d1313595d1f4b9a72f"},
                "color": "blue",
                "fabric_class": "synthetic",
            },
        ]
        self.assertEqual(response.json(), correct_response)
        self.assertEqual(response.status_code, 200)

    def test_scrap_by_id(self) -> None:
        response = requests.get(f"{APP_URL}/scraps/65298964b01cdb8f5179dc82")
        correct_response = [
            {
                "_id": {"$oid": "65298964b01cdb8f5179dc82"},
                "color": "red",
                "fabric_class": "natural",
            },
        ]
        self.assertEqual(response.json(), correct_response)
        self.assertEqual(response.status_code, 200)

    def test_scrap_by_id_invalid_id(self) -> None:
        response = requests.get(f"{APP_URL}/scraps/invalid_id")
        print(response.text)
        self.assertEqual(response.text, "")
        self.assertEqual(response.status_code, 204)
