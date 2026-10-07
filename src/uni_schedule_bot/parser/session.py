from dotenv import load_dotenv
import os
import httpx
from pprint import pprint
from bs4 import BeautifulSoup


def create_client(follow_redirects: bool = True, timeout: float = 10.0) -> httpx.Client:
    return httpx.Client(
        follow_redirects=follow_redirects,
        timeout=timeout
    )    

def main():
    load_dotenv()
    base_url = os.environ["UNI_BASE_URL"]
    schedule_url = f"{base_url}/public-schedule/group"


    try:
        client = create_client()#начало сессии
        schedule_page = client.get(schedule_url, params={'id':'МПИ26', 'dateFrom':'2026-10-07', 'dateTo':'2026-10-13',})

        with open("schedule.html", "w", encoding="utf-8") as f:
            f.write(schedule_page.text)
    finally:
        client.close()

if __name__ == "__main__":
    main()

    