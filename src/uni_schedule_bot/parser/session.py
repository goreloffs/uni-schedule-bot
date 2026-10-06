from dotenv import load_dotenv
import os
import httpx
from pprint import pprint
from bs4 import BeautifulSoup


def create_client(follow_redirects: bool = True, timeout: float = 10.0):
    return httpx.Client(
        follow_redirects=follow_redirects,
        timeout=timeout
    )

def fetch_csrf(client: httpx.Client, url: str) -> str:
    response = client.get(url)
    soup = BeautifulSoup(client.get(url).text, "lxml")
    tag = soup.find("input", attrs={"name": "_csrf"})
    if tag is None:
        raise RuntimeError(f"CSRF token not found at {url}")
    return tag.get("value")

    

def main():
    load_dotenv()
    base_url = os.environ["UNI_BASE_URL"]
    login_url = f"{base_url}/user/sign-in/login"


    client = create_client()

    try:
        
        csrf = fetch_csrf(client, login_url)
        print(csrf)
        pprint(client.cookies)

                

    finally:
        client.close()



if __name__ == "__main__":
    main()

    