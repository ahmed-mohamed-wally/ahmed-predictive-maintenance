import unittest

from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)


class TestAPI(unittest.TestCase):

    def test_root(self):
        response = client.get("/")

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn("message", data)

    def test_predict(self):
        payload = {
            "machine_type": "L",
            "air_temp": 302.0,
            "process_temp": 311.0,
            "rpm": 1400,
            "torque": 55.0,
            "tool_wear": 180
        }

        response = client.post(
            "/predict",
            json=payload
        )

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn("failure_probability", data)
        self.assertIn("failure", data)
        self.assertIn("failure_types", data)
        self.assertIn("risk", data)
        self.assertIn("maintenance_action", data)

    def test_invalid_machine_type(self):
        payload = {
            "machine_type": "X",
            "air_temp": 302.0,
            "process_temp": 311.0,
            "rpm": 1400,
            "torque": 55.0,
            "tool_wear": 180
        }

        response = client.post(
            "/predict",
            json=payload
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()