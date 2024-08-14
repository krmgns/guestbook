from fastapi.testclient import TestClient
from unittest import TestCase
from main import app
from __util import JSONResponse, parse_dotenv
import time

client = TestClient(app)

# Add test data for once.
res = client.get("/users")
if len(res.json()["users"]) == 0:
    client.post("/entries", json={
        "name": "Kerem",
        "subject": "Kerem's subject",
        "message": "Kerem's message"
    })

class AppTest(TestCase):
    def test_get_users(self):
        res = client.get("/users")
        ret = res.json()

        self.assertIn("users", ret)
        self.assertIsInstance(ret["users"], list)
        self.assertIn("username", ret["users"][0])
        self.assertIn("last_entry", ret["users"][0])
        self.assertIn("total_count_of_messages", ret["users"][0])

    def test_get_entries(self):
        res = client.get("/entries")
        ret = res.json()

        self.assertIn("count", ret)
        self.assertIn("page_size", ret)
        self.assertIn("total_pages", ret)
        self.assertIn("current_page_number", ret)
        self.assertIn("links", ret)
        self.assertIn("entries", ret)
        self.assertIsInstance(ret["entries"], list)
        self.assertIn("user", ret["entries"][0])
        self.assertIn("subject", ret["entries"][0])
        self.assertIn("message", ret["entries"][0])

    def test_add_entry(self):
        identifier = int(time.time())
        name = f"Test user {identifier}"
        subject = f"Test subject {identifier}"
        message = f"Test message {identifier}"

        res = client.post("/entries", json={
            "name": name, "subject": subject, "message": message
        })
        ret = res.json()

        self.assertIn("id", ret)
        self.assertEqual(200, res.status_code)

        # Bad request (invalid entry data).
        res = client.post("/entries", json={
            "name": "name"
        })
        ret = res.json()

        self.assertNotIn("id", ret)
        self.assertEqual(422, res.status_code)

class UtilTest(TestCase):
    def test_json_response(self):
        res = JSONResponse(200, {"msg":"ok"}, indent=0)

        self.assertEqual(200, res.status_code)
        self.assertEqual(b'{\n"msg": "ok"\n}', res.body)

    def test_parse_dotenv(self):
        ops = parse_dotenv()

        self.assertEqual("localhost", ops["DB_HOST"])
