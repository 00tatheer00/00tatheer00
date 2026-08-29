from __future__ import annotations
import os
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
USERNAME = "00tatheer00"

def github_api(path: str):
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(f"https://api.github.com{path}", headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()

def main() -> None:
    # Keep this script intentionally lightweight: the README's third-party stats
    # services render live graphs, while this action can be extended later for
    # custom SVGs or GitHub GraphQL contribution data.
    profile = github_api(f"/users/{USERNAME}")
    text = (ASSETS / "profile-data.txt")
    lines = [
        f"name={profile.get('name') or 'Syed Tatheer Hussain'}",
        f"login={profile.get('login', USERNAME)}",
        f"public_repos={profile.get('public_repos', 0)}",
        f"followers={profile.get('followers', 0)}",
        f"following={profile.get('following', 0)}",
        f"updated_utc={__import__('datetime').datetime.utcnow().isoformat()}Z",
    ]
    text.write_text("\n".join(lines) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
