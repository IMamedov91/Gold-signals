"""
quick_connect.py
----------------
Maak verbinding met de TopstepX / ProjectX-gateway, print je accounts en stopt.

❶  Zet je API-key & e-mail in Windows-omgevingsvariabelen,
    of vul ze hieronder direct in de code.
❷  python quick_connect.py
"""
from __future__ import annotations
import os, sys, json, requests

BASE_URL = "https://api.topstepx.com"        # prod-omgeving
USER     = os.getenv("PROJECTX_USER",    "<JOUW_EMAIL>")
API_KEY  = os.getenv("PROJECTX_API_KEY", "<44-tekens key>")

def login(user: str, key: str) -> str:
    """POST /api/Auth/loginKey → geeft session-token terug"""
    r = requests.post(
        f"{BASE_URL}/api/Auth/loginKey",
        json={"userName": user, "apiKey": key},
        timeout=15,
    )
    r.raise_for_status()
    data = r.json()
    if not data.get("success"):
        sys.exit(f"❌ login mislukt: {data}")
    return data["token"]

def list_accounts(token: str) -> None:
    hdr = {"Authorization": f"Bearer {token}"}
    r = requests.post(
        f"{BASE_URL}/api/Account/search",
        headers=hdr,
        json={"onlyActiveAccounts": True},
        timeout=15,
    )
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2))

if __name__ == "__main__":
    if "<" in USER or "<" in API_KEY:
        sys.exit("❗ Vul USER en API_KEY eerst in .env of code")
    token = login(USER, API_KEY)
    print("✅ Session-token verkregen (lengte:", len(token), ")")
    list_accounts(token)
