#!/usr/bin/env python3
"""
scan_ecosystem.py
Scans Anuradha Wickramarachchi's published software packages across:
- Crates.io (Rust crates)
- PyPI (Python packages)
- Bioconda / Anaconda
- GitHub (recent non-fork repositories)
- Starter Templates & Blueprints for src/pages/templates.astro
"""

import sys
import json
import urllib.request
import urllib.error

USER_AGENT = "anuradhawick-site-sync (info@anuradhawick.com)"
CRATES_USER_ID = "266446"
GITHUB_USER = "anuradhawick"

KNOWN_TEMPLATES = [
    {
        "name": "icebreak",
        "category": "Full-Stack & Web Applications",
        "badge": "Go · React · AWS Terraform",
        "url": "https://github.com/anuradhawick/icebreak",
        "live": "https://icebreak.anuradhawick.com",
        "purpose": "Full-stack Go backend & React frontend with AWS Terraform infrastructure"
    },
    {
        "name": "tf_template",
        "category": "Full-Stack & Web Applications",
        "badge": "Angular · Python · Docker · AWS Terraform",
        "url": "https://github.com/anuradhawick/tf_template",
        "purpose": "Angular frontend + Python Lambda & Docker container microservice on AWS"
    },
    {
        "name": "avcarcare.com.au",
        "category": "Full-Stack & Web Applications",
        "badge": "React · Vercel · Supabase · Quote System",
        "url": "https://github.com/anuradhawick/avcarcare.com.au",
        "live": "https://avcarcare.com.au",
        "purpose": "Service provider web template with Vercel, Supabase, and dynamic quote estimator"
    },
    {
        "name": "rs_template",
        "category": "Cloud & Serverless Infrastructure",
        "badge": "Rust · AWS Lambda · Terraform · cargo-lambda",
        "url": "https://github.com/anuradhawick/rs_template",
        "purpose": "Cold-start-free Rust Lambda function with lambdamux routing and Terraform"
    },
    {
        "name": "aws-lambda-serverless-boilerplate",
        "category": "Cloud & Serverless Infrastructure",
        "badge": "Python · AWS Lambda · Serverless Framework",
        "url": "https://github.com/anuradhawick/aws-lambda-serverless-boilerplate",
        "purpose": "Battle-tested Python serverless boilerplate for rapid prototyping"
    },
    {
        "name": "rs-avl",
        "category": "Database Engines & Low-Level Toolkits",
        "badge": "Rust · Data Structures · Storage Engines · PyPI",
        "url": "https://github.com/anuradhawick/rs-avl",
        "purpose": "Generic AVL tree for database development, indexing, and ordered key-value storage"
    },
    {
        "name": "sqlite-functions",
        "category": "Database Engines & Low-Level Toolkits",
        "badge": "Rust · SQLite · UDFs · CLI",
        "url": "https://github.com/anuradhawick/sqlite-functions",
        "purpose": "Toolkit for authoring custom Rust user-defined functions for SQLite and CLIs"
    },
    {
        "name": "casechange",
        "category": "Package Publishing & Developer Blueprints",
        "badge": "Python · PyPI · Packaging · Poetry",
        "url": "https://github.com/anuradhawick/casechange",
        "purpose": "Modern reference starter for structuring, building, and publishing Python libraries to PyPI"
    }
]

def fetch_json(url, custom_headers=None):
    headers = {"User-Agent": USER_AGENT}
    if custom_headers:
        headers.update(custom_headers)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None

def get_crates():
    url = f"https://crates.io/api/v1/crates?user_id={CRATES_USER_ID}"
    data = fetch_json(url)
    crates = []
    if data and "crates" in data:
        for c in data["crates"]:
            crates.append({
                "name": c.get("name"),
                "description": c.get("description"),
                "max_version": c.get("max_version"),
                "downloads": c.get("downloads"),
                "repository": c.get("repository"),
                "crate_url": f"https://crates.io/crates/{c.get('name')}"
            })
    return crates

def get_pypi_packages(candidate_names):
    packages = []
    for name in candidate_names:
        url = f"https://pypi.org/pypi/{name}/json"
        data = fetch_json(url)
        if data and "info" in data and data["info"].get("name"):
            info = data["info"]
            packages.append({
                "name": info.get("name"),
                "version": info.get("version"),
                "summary": info.get("summary"),
                "home_page": info.get("home_page") or info.get("project_url"),
                "pypi_url": f"https://pypi.org/project/{info.get('name')}/",
                "author": info.get("author") or info.get("author_email")
            })
    return packages

def get_bioconda():
    url = "https://api.anaconda.org/package/bioconda/kmertools"
    data = fetch_json(url)
    if data and data.get("name"):
        return [{
            "name": data.get("name"),
            "summary": data.get("summary"),
            "latest_version": data.get("latest_version"),
            "home": data.get("home"),
            "conda_url": "https://anaconda.org/channels/bioconda/packages/kmertools/overview"
        }]
    return []

def get_github_repos():
    url = f"https://api.github.com/users/{GITHUB_USER}/repos?sort=pushed&per_page=100"
    data = fetch_json(url)
    repos = []
    if data and isinstance(data, list):
        for r in data:
            if not r.get("fork", False):
                repos.append({
                    "name": r.get("name"),
                    "description": r.get("description"),
                    "language": r.get("language"),
                    "stars": r.get("stargazers_count", 0),
                    "url": r.get("html_url"),
                    "homepage": r.get("homepage"),
                    "topics": r.get("topics", []),
                    "pushed_at": r.get("pushed_at")
                })
    return repos

def main():
    print(f"Scanning ecosystem for user: {GITHUB_USER}...\n")

    # 1. Fetch Crates
    crates = get_crates()
    print(f"=== Crates.io ({len(crates)} found) ===")
    for c in crates:
        print(f"  • {c['name']} (v{c['max_version']}): {c['description']}")
        print(f"    URL: {c['crate_url']}")

    # 2. Fetch GitHub Repos
    repos = get_github_repos()
    print(f"\n=== Recent GitHub Repositories ({len(repos)} non-fork) ===")
    for r in repos[:15]:
        desc = r['description'] or 'No description'
        print(f"  • {r['name']} ({r['language'] or 'Unknown'}, {r['stars']}★): {desc}")
        print(f"    Pushed: {r['pushed_at'][:10]} | URL: {r['url']}")

    # 3. Check candidate PyPI packages
    candidates = list(set([
        "avldb", "s3-avldb", "pykmertools", "cogent3-pykmertools",
        "rs-avl", "rsbio-seq", "casechange", "casechange_wic"
    ] + [r["name"].lower() for r in repos[:20]]))
    pypi_pkgs = get_pypi_packages(candidates)
    print(f"\n=== PyPI Packages ({len(pypi_pkgs)} found) ===")
    for p in pypi_pkgs:
        print(f"  • {p['name']} (v{p['version']}): {p['summary']}")
        print(f"    URL: {p['pypi_url']}")

    # 4. Bioconda
    bioconda = get_bioconda()
    print(f"\n=== Bioconda / Anaconda ({len(bioconda)} found) ===")
    for b in bioconda:
        print(f"  • {b['name']} (v{b['latest_version']}): {b['summary']}")
        print(f"    URL: {b['conda_url']}")

    # 5. Templates & Starter Blueprints
    print(f"\n=== Templates & Starters ({len(KNOWN_TEMPLATES)} audited) ===")
    for t in KNOWN_TEMPLATES:
        print(f"  • [{t['category']}] {t['name']} ({t['badge']})")
        print(f"    Purpose: {t['purpose']}")
        print(f"    Repo: {t['url']}")

    # Summary
    result = {
        "crates": crates,
        "pypi": pypi_pkgs,
        "bioconda": bioconda,
        "templates": KNOWN_TEMPLATES,
        "recent_github": repos[:20]
    }
    
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        with open("ecosystem_snapshot.json", "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2)
        print("\nSaved snapshot to ecosystem_snapshot.json")

if __name__ == "__main__":
    main()
