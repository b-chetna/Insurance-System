import unittest

import app as insurance_app


app = insurance_app.app


class TestInsuranceApp(unittest.TestCase):

    def setUp(self):

        self.client = app.test_client()

        insurance_app.claims.clear()

        insurance_app.next_claim_id = 1

    def add_sample_claim(self):

        return self.client.post(
            "/add",
            data={
                "claimant": "Chetna",
                "policy_number": "POL123",
                "amount": "5000",
                "description": "Vehicle damage"
            }
        )

    def test_homepage(self):

        response = self.client.get("/")

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertIn(
            b"Insurance Claim System",
            response.data
        )

    def test_health(self):

        response = self.client.get("/health")

        self.assertEqual(
            response.status_code,
            200
        )

    def test_add_claim(self):

        response = self.add_sample_claim()

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertEqual(
            len(insurance_app.claims),
            1
        )

        self.assertEqual(
            insurance_app.claims[0]["status"],
            "Pending"
        )

    def test_view_claims(self):

        self.add_sample_claim()

        response = self.client.get("/claims")

        self.assertEqual(
            response.status_code,
            200
        )

        self.assertEqual(
            len(response.json),
            1
        )

        self.assertEqual(
            response.json[0]["claimant"],
            "Chetna"
        )

    def test_update_claim_status(self):

        self.add_sample_claim()

        response = self.client.post(
            "/update/1",
            data={
                "status": "Approved"
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertEqual(
            insurance_app.claims[0]["status"],
            "Approved"
        )

    def test_invalid_status(self):

        self.add_sample_claim()

        response = self.client.post(
            "/update/1",
            data={
                "status": "Invalid"
            }
        )

        self.assertEqual(
            response.status_code,
            400
        )

    def test_nonexistent_claim(self):

        response = self.client.post(
            "/update/999",
            data={
                "status": "Approved"
            }
        )

        self.assertEqual(
            response.status_code,
            404
        )


if __name__ == "__main__":

    unittest.main()