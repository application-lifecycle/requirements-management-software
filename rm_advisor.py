#!/usr/bin/env python3
"""Requirements Management Software — Open Source Directory & Comparison CLI.

Zero-dependency CLI tool to search, filter, compare, and recommend requirements
management tools from tools.json, and validate PR contributions.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DATA_PATH = Path(__file__).resolve().parent / "tools.json"

REQUIRED_CAPABILITIES = {
    "traceability_matrix",
    "reqif",
    "baselines",
    "impact_analysis",
    "git_integration",
    "test_linking",
    "web_ui",
}


def load_data(path: Path = DATA_PATH) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def filter_tools(
    tools: list[dict[str, Any]],
    *,
    job: str | None = None,
    license_type: str | None = None,
    deployment: str | None = None,
    reqif: bool = False,
    git_native: bool = False,
    compliance: str | None = None,
    query: str | None = None,
) -> list[dict[str, Any]]:
    results = tools
    if job:
        results = [t for t in results if job in t.get("jobs", [])]
    if license_type:
        results = [t for t in results if t.get("license_type") == license_type]
    if deployment:
        results = [t for t in results if deployment in t.get("deployment", [])]
    if reqif:
        results = [t for t in results if t.get("capabilities", {}).get("reqif")]
    if git_native:
        results = [
            t for t in results if t.get("capabilities", {}).get("git_integration")
        ]
    if compliance:
        needle = compliance.lower()
        results = [
            t
            for t in results
            if any(needle in c.lower() for c in t.get("compliance", []))
        ]
    if query:
        q = query.lower()
        results = [
            t
            for t in results
            if q in t.get("name", "").lower()
            or q in t.get("tagline", "").lower()
            or q in t.get("best_for", "").lower()
        ]
    return results


def recommend_tools(
    tools: list[dict[str, Any]],
    *,
    workflow: str,
    regulated: bool,
    budget: str,
) -> list[dict[str, Any]]:
    scored: list[tuple[int, dict[str, Any]]] = []
    for tool in tools:
        score = 0
        jobs = set(tool.get("jobs", []))
        caps = tool.get("capabilities", {})
        if workflow in jobs:
            score += 4
        if regulated:
            if tool.get("compliance"):
                score += 3
            if caps.get("traceability_matrix") and caps.get("baselines"):
                score += 2
            if caps.get("reqif"):
                score += 1
        else:
            if "agile" in jobs or "git-native" in jobs:
                score += 2
        if budget == "free" and tool.get("license_type") == "open-source":
            score += 4
        elif budget == "freemium" and tool.get("license_type") in {
            "open-source",
            "freemium",
        }:
            score += 3
        elif budget == "enterprise" and tool.get("category") == "enterprise-alm":
            score += 2
        scored.append((score, tool))

    scored.sort(
        key=lambda pair: (
            -pair[0],
            -len(pair[1].get("compliance", [])),
            -sum(1 for v in pair[1].get("capabilities", {}).values() if v),
            pair[1]["name"],
        )
    )
    return [tool for _, tool in scored[:5]]


def validate_schema(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    tools = data.get("tools")
    if not isinstance(tools, list) or not tools:
        return ["'tools' must be a non-empty list"]

    seen_ids: set[str] = set()
    for idx, tool in enumerate(tools):
        tid = tool.get("id", f"index-{idx}")
        for field in (
            "id",
            "name",
            "tagline",
            "category",
            "jobs",
            "license_type",
            "deployment",
            "pricing",
            "website",
            "capabilities",
            "best_for",
        ):
            if field not in tool or tool[field] in (None, ""):
                errors.append(f"{tid}: missing required field '{field}'")

        if tid in seen_ids:
            errors.append(f"{tid}: duplicate tool id")
        seen_ids.add(tid)

        website = tool.get("website", "")
        if not isinstance(website, str) or not website.startswith("https://"):
            errors.append(f"{tid}: website must start with https://")

        caps = tool.get("capabilities", {})
        missing_caps = REQUIRED_CAPABILITIES - set(caps.keys())
        if missing_caps:
            errors.append(f"{tid}: missing capabilities {sorted(missing_caps)}")

    return errors


def print_table(tools: list[dict[str, Any]]) -> None:
    if not tools:
        print("No matching requirements management tools found.")
        return
    header = f"{'ID':<20} {'Name':<28} {'License':<12} {'ReqIF':<6} {'Git':<5} {'Pricing'}"
    print(header)
    print("-" * len(header))
    for t in tools:
        caps = t.get("capabilities", {})
        reqif = "Yes" if caps.get("reqif") else "No"
        git = "Yes" if caps.get("git_integration") else "No"
        print(
            f"{t['id']:<20} {t['name'][:27]:<28} {t['license_type']:<12} {reqif:<6} {git:<5} {t['pricing']}"
        )


def print_comparison(tools: list[dict[str, Any]]) -> None:
    if not tools:
        print("No matching IDs found to compare.")
        return
    cols = tools[:3]
    labels = [
        ("License", lambda t: f"{t['license_type']} ({t['license_name']})"),
        ("Deployment", lambda t: ", ".join(t["deployment"])),
        ("Pricing", lambda t: t["pricing"]),
        ("Traceability Matrix", lambda t: "Yes" if t["capabilities"]["traceability_matrix"] else "No"),
        ("ReqIF Support", lambda t: "Yes" if t["capabilities"]["reqif"] else "No"),
        ("Baselines", lambda t: "Yes" if t["capabilities"]["baselines"] else "No"),
        ("Impact Analysis", lambda t: "Yes" if t["capabilities"]["impact_analysis"] else "No"),
        ("Git Integration", lambda t: "Yes" if t["capabilities"]["git_integration"] else "No"),
        ("Test Linking", lambda t: "Yes" if t["capabilities"]["test_linking"] else "No"),
        ("Compliance", lambda t: ", ".join(t["compliance"]) or "General"),
        ("Website", lambda t: t["website"]),
    ]
    print(f"{'Attribute':<22} " + " | ".join(f"{t['name'][:26]:<26}" for t in cols))
    print("-" * (23 + 29 * len(cols)))
    for label, fn in labels:
        row = " | ".join(f"{str(fn(t))[:26]:<26}" for t in cols)
        print(f"{label:<22} {row}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Requirements Management Software Directory & Comparison CLI"
    )
    parser.add_argument("--job", choices=["regulated", "git-native", "agile", "systems-engineering", "open-source"])
    parser.add_argument("--license", dest="license_type", choices=["open-source", "commercial", "freemium"])
    parser.add_argument("--deployment", choices=["cloud-saas", "self-hosted", "local-cli"])
    parser.add_argument("--reqif", action="store_true", help="Only tools supporting ReqIF")
    parser.add_argument("--git", dest="git_native", action="store_true", help="Only tools with Git integration")
    parser.add_argument("--compliance", help="Filter by standard (e.g. 'ISO 26262', 'IEC 62304')")
    parser.add_argument("--query", help="Keyword search across name, tagline, best_for")
    parser.add_argument("--compare", nargs="+", metavar="ID", help="Compare 2-3 tools by ID")
    parser.add_argument("--recommend", action="store_true", help="Run guided recommendation")
    parser.add_argument("--workflow", default="git-native", choices=["git-native", "regulated", "agile", "systems-engineering"])
    parser.add_argument("--regulated", action="store_true", help="Used with --recommend for regulated environments")
    parser.add_argument("--budget", default="free", choices=["free", "freemium", "enterprise"])
    parser.add_argument("--validate", action="store_true", help="Validate tools.json schema")
    parser.add_argument("--json", dest="as_json", action="store_true", help="Output JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    data = load_data()

    if args.validate:
        errors = validate_schema(data)
        if errors:
            for err in errors:
                print(f"ERROR: {err}", file=sys.stderr)
            return 1
        print(f"OK: validated {len(data['tools'])} tools in {DATA_PATH.name}")
        return 0

    tools = data["tools"]
    if args.compare:
        wanted = {tid.lower() for tid in args.compare}
        selected = [t for t in tools if t["id"].lower() in wanted]
        if args.as_json:
            print(json.dumps(selected, indent=2))
        else:
            print_comparison(selected)
        return 0

    if args.recommend:
        recs = recommend_tools(
            tools,
            workflow=args.workflow,
            regulated=args.regulated,
            budget=args.budget,
        )
        if args.as_json:
            print(json.dumps(recs, indent=2))
        else:
            print_table(recs)
        return 0

    filtered = filter_tools(
        tools,
        job=args.job,
        license_type=args.license_type,
        deployment=args.deployment,
        reqif=args.reqif,
        git_native=args.git_native,
        compliance=args.compliance,
        query=args.query,
    )
    if args.as_json:
        print(json.dumps(filtered, indent=2))
    else:
        print_table(filtered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
