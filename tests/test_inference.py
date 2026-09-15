import unittest

from src.inference import predict_machine


class TestPredictMachine(unittest.TestCase):

    def test_normal_machine_prediction(self):
        result = predict_machine(
            machine_type="L",
            air_temp=302.0,
            process_temp=311.0,
            rpm=1400,
            torque=55.0,
            tool_wear=180,
        )

        self.assertIn("failure_probability", result)
        self.assertIn("failure", result)
        self.assertIn("failure_types", result)
        self.assertIn("risk", result)
        self.assertIn("maintenance_action", result)

        self.assertIsInstance(
            result["failure_probability"],
            float
        )

        self.assertIsInstance(
            result["failure"],
            bool
        )

        self.assertIsInstance(
            result["failure_types"],
            list
        )

    def test_invalid_machine_type(self):
        with self.assertRaises(ValueError):
            predict_machine(
                machine_type="X",
                air_temp=302.0,
                process_temp=311.0,
                rpm=1400,
                torque=55.0,
                tool_wear=180,
            )

    def test_invalid_negative_rpm(self):
        with self.assertRaises(ValueError):
            predict_machine(
                machine_type="L",
                air_temp=302.0,
                process_temp=311.0,
                rpm=-100,
                torque=55.0,
                tool_wear=180,
            )


if __name__ == "__main__":
    unittest.main()