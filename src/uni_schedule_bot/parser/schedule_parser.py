import os
from dotenv import load_dotenv
import httpx
from bs4 import BeautifulSoup
from uni_schedule_bot.parser.session import create_client


def fetch_schedule(client: httpx.Client, base_url: str, group: str, date_from: str, date_to: str) -> str:
    
    schedule_url = f"{base_url}/public-schedule/group"
    params = {'id': group, 'dateFrom': date_from, 'dateTo': date_to}

    response = client.get(schedule_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        raise RuntimeError(f"Failed to fetch schedule: status {response.status_code}")


def main():
    load_dotenv()
    base_url = os.environ["UNI_BASE_URL"]
    try:
        client = create_client()
        html_schedule = fetch_schedule(client, base_url, "МПИ26", "2026-10-07", "2026-10-13")
    finally:
        client.close()
    



if __name__ == "__main__":
    main()