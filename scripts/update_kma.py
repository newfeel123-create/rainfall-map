from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
import requests

URLS = [
    "https://www.weather.go.kr/w/forecast/overall/short-term.do",
    "https://www.weather.go.kr/w/forecast/notice.do",
]
OUT = Path(__file__).resolve().parents[1] / "kma_forecast.json"

def fetch(url: str) -> str:
    response = requests.get(
        url,
        timeout=20,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 Chrome/124 Safari/537.36",
            "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.6",
        },
    )
    response.raise_for_status()
    response.encoding = response.apparent_encoding or "utf-8"
    return response.text

def main() -> None:
    docs = []
    for url in URLS:
        try:
            raw = fetch(url)
            if raw and len(raw) > 1000:
                docs.append({"url": url, "raw": raw})
        except Exception as exc:
            print(f"fetch failed: {url}: {exc}")

    if not docs:
        raise SystemExit("No KMA document could be downloaded.")

    OUT.write_text(
        json.dumps(
            {
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "docs": docs,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(f"updated {OUT} with {len(docs)} documents")

if __name__ == "__main__":
    main()
