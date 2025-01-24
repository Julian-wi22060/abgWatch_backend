import unittest
import requests

BASE_URL = "http://localhost:50555"


class TestAPIEndpoints(unittest.TestCase):
    # --------------------
    # v_candidacy_mandates
    # --------------------
    def test_get_v_candidacy_mandates_list(self):
        """Tests GET /v_candidacy_mandates/"""
        r = requests.get(f"{BASE_URL}/v_candidacy_mandates/")
        self.assertEqual(r.status_code, 200)

        data = r.json()
        print("uccess: v_candidacy_mandates data snippet:", data[:2])

    def test_get_v_candidacy_mandates_by_id(self):
        """Tests GET /v_candidacy_mandates/<id>"""
        cm_id = 1
        r = requests.get(f"{BASE_URL}/v_candidacy_mandates/{cm_id}")
        if r.status_code == 404:
            print(f"Kein Eintrag in v_candidacy_mandates für ID={cm_id}. Test wird übersprungen.")
            self.skipTest(f"No entry found with ID={cm_id}")
        else:
            self.assertEqual(r.status_code, 200)
            data = r.json()
            print("uccess: Einzel-v_candidacy_mandates snippet:", data)


if __name__ == "__main__":
    unittest.main()

# RUN WITH: python -m unittest tests/unittest.py
