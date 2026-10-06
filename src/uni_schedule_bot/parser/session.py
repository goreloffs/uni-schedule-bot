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

    

def main():
    load_dotenv()
    login = os.environ["UNI_LOGIN"]
    password = os.environ["UNI_PASSWORD"]
    base_url = os.environ["UNI_BASE_URL"]
    login_url = f"{base_url}/user/sign-in/login"
    schedule_url = f"{base_url}/student/schedule?_referrer=%2Fstudent%2Findex"


    client = create_client()#начало сессии

    try:
        
        csrf = fetch_csrf(client, login_url) #Получаем csrf и client.get(url)

        response = post_login(client, login_url, login, password, csrf)
        role_url = str(response.url)
        if "/user/sign-in/login" in str(response.url):
            raise RuntimeError("Login failed: still on login page")
        print(response.url)
        
        response = client.get(role_url, params={'role': 'Student'})
        print(response.url)
        response = client.get(schedule_url)
        
        print(response.url)
        

                

    finally:
        client.close()



if __name__ == "__main__":
    main()

    