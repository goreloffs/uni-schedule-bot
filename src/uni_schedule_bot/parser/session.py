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

def fetch_csrf(client: httpx.Client, url: str) -> str:
    soup = BeautifulSoup(client.get(url).text, "lxml")
    tag = soup.find("input", attrs={"name": "_csrf"})
    if tag is None:
        raise RuntimeError(f"CSRF token not found at {url}")
    return tag.get("value")


def post_login(client: httpx.Client, login_url: str, login: str, password: str, csrf: str, remember_me=0) -> httpx.Response:
    data = {'_csrf': csrf,
            'LoginForm[identity]': login,
            'LoginForm[password]': password,
            'LoginForm[rememberMe]': remember_me}
    return client.post(login_url, data=data)

def open_shedule_page(client, base_url, login, password) -> httpx.Response:
    login_url = f"{base_url}/user/sign-in/login"
    schedule_url = f"{base_url}/student/schedule?_referrer=%2Fstudent%2Findex"

    csrf = fetch_csrf(client, f"{base_url}/user/sign-in/login") #Получаем csrf
    response = post_login(client, login_url, login, password, csrf)
    role_url = str(response.url)
    client.get(role_url, params={'role': 'Student'})
    schedule_url = f"{base_url}/student/schedule?_referrer=%2Fstudent%2Findex"
    return client.get(schedule_url)
    

def main():
    load_dotenv()
    login = os.environ["UNI_LOGIN"]
    password = os.environ["UNI_PASSWORD"]
    base_url = os.environ["UNI_BASE_URL"]

    try:
        client = create_client()#начало сессии
        schedule_page = open_shedule_page(client, base_url, login, password)
        schedule_page.text
    finally:
        client.close()

if __name__ == "__main__":
    main()

    