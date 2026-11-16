import json
import unittest
from pathlib import Path

import rm_advisor

ROOT = Path(__file__).resolve().parent.parent


class TestToolsCatalog(unittest.TestCase):
    def test_schema_is_valid(self) -> None:
        data = rm_advisor.load_data()
        errors = rm_advisor.validate_schema(data)
        self.assertEqual(errors, [])
        self.assertGreaterEqual(len(data["tools"]), 20)

    def test_docs_tools_json_in_sync(self) -> None:
        root_json = json.loads((ROOT / "tools.json").read_text(encoding="utf-8"))
        docs_json = json.loads((ROOT / "docs" / "tools.json").read_text(encoding="utf-8"))
        self.assertEqual(root_json, docs_json)

    def test_filter_open_source_and_reqif(self) -> None:
        tools = rm_advisor.load_data()["tools"]
        matches = rm_advisor.filter_tools(tools, license_type="open-source", reqif=True)
        ids = {t["id"] for t in matches}
        self.assertIn("strictdoc", ids)
        self.assertIn("sphinx-needs", ids)
        self.assertIn("eclipse-rmf", ids)

    def test_recommend_returns_ranked_results(self) -> None:
        tools = rm_advisor.load_data()["tools"]
        recs = rm_advisor.recommend_tools(
            tools, workflow="git-native", regulated=True, budget="free"
        )
        self.assertEqual(len(recs), 5)
        self.assertEqual(recs[0]["id"], "strictdoc")


if __name__ == "__main__":
    unittest.main()
