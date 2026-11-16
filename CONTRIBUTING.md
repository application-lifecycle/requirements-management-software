# Contributing to Requirements Management Software Directory

Contributions are welcome via **GitHub Pull Request** or **Issue**!

## How to Submit a New Tool via Pull Request

1. Fork this repository and create a branch (e.g. `add-tool-name`).
2. Add your tool entry to `tools.json` following the schema below.
3. Sync `docs/tools.json` with `tools.json`:
   ```bash
   cp tools.json docs/tools.json
   ```
4. Validate your changes locally:
   ```bash
   python3 rm_advisor.py --validate
   python3 -m unittest discover -s tests -v
   ```
5. Open a Pull Request! GitHub Actions will automatically run the validation suite.

## Entry Schema (`tools.json`)

```json
{
  "id": "unique-kebab-slug",
  "name": "Tool Name",
  "tagline": "Concise one-line description of what the tool does",
  "category": "git-native | systems-alm | enterprise-alm | agile-pm",
  "jobs": ["git-native", "regulated", "agile", "systems-engineering", "open-source"],
  "license_type": "open-source | freemium | commercial",
  "license_name": "Apache-2.0 / MIT / Proprietary / etc.",
  "deployment": ["local-cli", "self-hosted", "cloud-saas"],
  "pricing": "Free (Open Source) / From $X/user/mo / Custom Quote",
  "website": "https://official-website.example/",
  "github": "https://github.com/org/repo (or null)",
  "github_stars_approx": "1k+ (or null)",
  "capabilities": {
    "traceability_matrix": true,
    "reqif": false,
    "baselines": true,
    "impact_analysis": false,
    "git_integration": true,
    "test_linking": true,
    "web_ui": false
  },
  "compliance": ["ISO 26262", "IEC 62304"],
  "best_for": "One-sentence summary of the ideal team and use case."
}
```
