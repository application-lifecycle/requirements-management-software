<div align="center">

# Requirements management software: open-source directory and comparison tool

**Compare 22 open-source and commercial requirements management tools by engineering workflow, ReqIF support, Git integration, compliance standards, and pricing.**

[![Verified Tools](https://img.shields.io/badge/Verified_Tools-22_Active-1d4ed8?style=flat-square)](#-open-source-requirements-management-software)
[![Open Source](https://img.shields.io/badge/Open_Source-9_Tools-10b981?style=flat-square)](#-open-source-requirements-management-software)
[![ReqIF Capable](https://img.shields.io/badge/ReqIF_Support-15_Tools-3b82f6?style=flat-square)](#-commercial-and-enterprise-requirements-management-software)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

[Interactive web directory](https://application-lifecycle.github.io/requirements-management-software/) • [Decision matrix](#decision-matrix-by-workflow) • [Open source tools](#open-source-requirements-management-software) • [Commercial ALM](#commercial-and-enterprise-requirements-management-software) • [CLI](#interactive-cli-comparison-and-matcher) • [Submit a tool](#propose-a-new-tool-via-github-pull-request)

</div>

![Requirements Management Software Directory Preview](docs/assets/preview.png)

## Why this directory exists

Teams evaluating requirements management software have very different workflows depending on their product and regulatory environment. Software teams writing specs in Markdown, YAML, or SDoc usually want requirements stored in Git and reviewed in pull requests. Hardware, automotive, aerospace, and medical device teams working under ISO 26262, IEC 62304, DO-178C, or FDA 21 CFR Part 11 need immutable baselines, electronic sign-off, and ReqIF exchange. Agile product teams often prefer adding traceability directly inside Jira, Azure DevOps, or GitLab.

This repository maintains a verified dataset ([`tools.json`](tools.json)), an interactive GitHub Pages directory ([`docs/index.html`](docs/index.html)), and a zero-dependency Python CLI ([`rm_advisor.py`](rm_advisor.py)) to compare those options side by side.

## Decision matrix by workflow

| Engineering context | Recommended tools | Why it fits | Links |
| :--- | :--- | :--- | :--- |
| Git-native and docs-as-code (open source) | StrictDoc, Doorstop | Plain-text SDoc or YAML in Git, PR reviews, CI traceability checks, no license cost | [StrictDoc](https://github.com/strictdoc-project/strictdoc) • [Doorstop](https://github.com/doorstop-dev/doorstop) |
| Lightweight ReqIF without server setup | ReqView, Eclipse RMF | Native ReqIF import and export, DOORS-style tables, offline or Git-backed JSON | [ReqView](https://www.reqview.com/) • [Eclipse RMF](https://github.com/eclipse/rmf) |
| Automotive, aerospace, and defense ALM | Jama Connect, Codebeamer, Polarion, IBM DOORS Next | V-model traceability, variant management, ISO 26262 / DO-178C / ASPICE support | [Jama](https://www.jamasoftware.com/platform/jama-connect/) • [Codebeamer](https://www.ptc.com/en/products/codebeamer) • [Polarion](https://plm.sw.siemens.com/en-US/polarion/) |
| Medical device QMS (IEC 62304 / FDA) | MatrixALM, Jama Connect, SpiraTeam | Design controls, risk FMEA, and 21 CFR Part 11 electronic signatures | [MatrixALM](https://www.matrixreq.com/) • [SpiraTeam](https://www.inflectra.com/SpiraTeam/) |
| Jira or Azure DevOps native | R4J, Modern Requirements4DevOps | Tree hierarchies, baselines, and suspect-link matrices inside Jira or ADO | [R4J](https://easesolutions.com/r4j-requirements-management-for-jira/) • [Modern Req](https://www.modernrequirements.com/) |
| Agile PRDs and self-hosted tracking | Plane, GitLab Requirements | Self-hosted issue and PRD workspace or CI-linked GitLab requirements | [Plane](https://github.com/makeplane/plane) • [GitLab](https://docs.gitlab.com/ee/user/project/requirements/) |

## Open source requirements management software

| Tool | License | Deployment | ReqIF | Traceability | Git native | Official site | GitHub |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| StrictDoc | Apache-2.0 | Local CLI, Self-Hosted | Yes | Yes | Yes | [strictdoc.readthedocs.io](https://strictdoc.readthedocs.io/) | [strictdoc-project/strictdoc](https://github.com/strictdoc-project/strictdoc) |
| Doorstop | LGPL-3.0 | Local CLI | No | Yes | Yes | [doorstop.readthedocs.io](https://doorstop.readthedocs.io/) | [doorstop-dev/doorstop](https://github.com/doorstop-dev/doorstop) |
| Sphinx-Needs | MIT | Local CLI, Self-Hosted | Yes | Yes | Yes | [sphinx-needs.com](https://sphinx-needs.com/) | [useblocks/sphinx-needs](https://github.com/useblocks/sphinx-needs) |
| TReqs | MIT | Local CLI | No | Yes | Yes | [treqs-on-git.github.io](https://treqs-on-git.github.io/) | [treqs-on-git/treqs-ng](https://github.com/treqs-on-git/treqs-ng) |
| Eclipse RMF (ProR) | EPL-2.0 | Desktop | Yes | Yes | Yes | [eclipse.dev/rmf](https://eclipse.dev/rmf/) | [eclipse/rmf](https://github.com/eclipse/rmf) |
| Plane | AGPL-3.0 | Cloud, Self-Hosted | No | No | Yes | [plane.so](https://plane.so/) | [makeplane/plane](https://github.com/makeplane/plane) |
| Redmine | GPL-2.0 | Self-Hosted | No | No | Yes | [redmine.org](https://www.redmine.org/) | [redmine/redmine](https://github.com/redmine/redmine) |
| OSRMT | GPL-2.0 | Desktop, Self-Hosted | No | Yes | No | [sourceforge.net/projects/osrmt](https://sourceforge.net/projects/osrmt/) | [osrmt/osrmt](https://github.com/osrmt/osrmt) |

## Commercial and enterprise requirements management software

| Tool | Category | Pricing model | ReqIF | Compliance standards | Official website |
| :--- | :--- | :--- | :---: | :--- | :--- |
| ReqView | Systems / Git-JSON | Free Viewer / ~$29/user/mo | Yes | ISO 26262, IEC 62304, DO-178C, FDA 21 CFR Part 11 | [reqview.com](https://www.reqview.com/) |
| Jama Connect | Enterprise ALM | Custom Enterprise Quote | Yes | ISO 26262, DO-178C, IEC 62304, FDA 21 CFR Part 11, ASPICE | [jamasoftware.com](https://www.jamasoftware.com/platform/jama-connect/) |
| IBM DOORS Next | Enterprise ALM | Custom Enterprise Quote | Yes | ISO 26262, DO-178C, ASPICE, MIL-STD | [ibm.com](https://www.ibm.com/products/requirements-management) |
| Siemens Polarion | Enterprise ALM | Custom Enterprise Quote | Yes | ISO 26262, DO-178C, IEC 62304, FDA 21 CFR Part 11, ASPICE | [plm.sw.siemens.com](https://plm.sw.siemens.com/en-US/polarion/) |
| PTC Codebeamer | Enterprise ALM | Custom Enterprise Quote | Yes | ISO 26262, DO-178C, IEC 62304, ASPICE | [ptc.com](https://www.ptc.com/en/products/codebeamer) |
| Visure Requirements ALM | Enterprise ALM | Custom Quote / Trial | Yes | ISO 26262, DO-178C, IEC 62304, EN 50128 | [visuresolutions.com](https://visuresolutions.com/) |
| Perforce Helix RM | Enterprise ALM | Custom Quote | Yes | ISO 26262, IEC 62304, FDA 21 CFR Part 11 | [perforce.com](https://www.perforce.com/products/helix-alm) |
| Modern Requirements4DevOps | Azure DevOps | From ~$35/user/mo | Yes | FDA 21 CFR Part 11, ISO 13485, IEC 62304 | [modernrequirements.com](https://www.modernrequirements.com/) |
| R4J (Requirements for Jira) | Jira Marketplace | Tiered Marketplace | Yes | ASPICE, ISO 26262 | [easesolutions.com](https://easesolutions.com/r4j-requirements-management-for-jira/) |
| MatrixALM | MedTech QMS | Tiered SaaS | No | IEC 62304, ISO 13485, FDA 21 CFR Part 11 | [matrixreq.com](https://www.matrixreq.com/) |
| Valispace (Altium) | Systems / Hardware | Custom Quote | Yes | ECSS, DO-178C, ISO 26262 | [valispace.com](https://www.valispace.com/) |
| Innoslate | MBSE / Systems | Free Tier / ~$95/mo+ | Yes | DO-178C, ISO 26262 | [innoslate.com](https://www.innoslate.com/) |
| SpiraTeam | Integrated ALM | From ~$38/user/mo | Yes | FDA 21 CFR Part 11, IEC 62304, ISO 26262 | [inflectra.com](https://www.inflectra.com/SpiraTeam/) |
| GitLab Requirements | DevSecOps | GitLab Ultimate ($99/user/mo) | No | SOC 2, HIPAA | [docs.gitlab.com](https://docs.gitlab.com/ee/user/project/requirements/) |

## Interactive CLI comparison and matcher

Run the Python 3.10+ CLI locally with no external dependencies:

```bash
# Filter open-source tools with ReqIF support
python3 rm_advisor.py --license open-source --reqif

# Filter by compliance standard
python3 rm_advisor.py --compliance "ISO 26262"

# Compare up to 3 tools side-by-side
python3 rm_advisor.py --compare strictdoc reqview jama-connect

# Get top recommendations for your workflow
python3 rm_advisor.py --recommend --workflow git-native --regulated --budget free

# Validate tools.json schema
python3 rm_advisor.py --validate
```

## Propose a new tool via GitHub Pull Request

If a requirements management tool is missing or has outdated pricing or capabilities:

1. Edit [`tools.json`](tools.json) and copy it to `docs/tools.json` (`cp tools.json docs/tools.json`).
2. Run `python3 rm_advisor.py --validate` and `python3 -m unittest discover -s tests -v`.
3. Open a Pull Request following [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT License. See [`LICENSE`](LICENSE).
