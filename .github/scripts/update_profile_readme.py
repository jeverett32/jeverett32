#!/usr/bin/env python3
import datetime
import json
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUOTE_FILE = ROOT / ".sisyphus" / "quotes" / "profile_quotes.json"
README_FILE = ROOT / "README.md"


def load_quotes(path: Path) -> list[str]:
    if not path.exists():
        return ["Code is poetry in motion."]

    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    quotes = payload.get("quotes", []) if isinstance(payload, dict) else []
    if not isinstance(quotes, list):
        return ["Code is poetry in motion."]

    sanitized = [q.strip() for q in quotes if isinstance(q, str) and q.strip()]
    return sanitized or ["Code is poetry in motion."]


def quote_of_the_day(quotes: list[str]) -> str:
    index = datetime.date.today().toordinal() % len(quotes)
    return quotes[index]


def render_block(quote: str) -> str:
    return f"<!-- PROFILE_QUOTE_START -->\n{quote}\n<!-- PROFILE_QUOTE_END -->"


def update_readme(readme_path: Path, quote: str) -> None:
    content = (
        readme_path.read_text(encoding="utf-8")
        if readme_path.exists()
        else "# Hey, I'm John Everett 👋\n"
    )
    pattern = re.compile(
        r"<!-- PROFILE_QUOTE_START -->.*?<!-- PROFILE_QUOTE_END -->", re.DOTALL
    )
    block = render_block(quote)

    if pattern.search(content):
        updated = pattern.sub(block, content)
    else:
        updated = content.rstrip() + "\n\n## Quote of the Day\n" + block + "\n"

    readme_path.write_text(updated, encoding="utf-8")


def main() -> None:
    quotes = load_quotes(QUOTE_FILE)
    quote = quote_of_the_day(quotes)
    update_readme(README_FILE, quote)


if __name__ == "__main__":
    main()
