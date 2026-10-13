import os
from dotenv import load_dotenv
import httpx
from bs4 import BeautifulSoup
from uni_schedule_bot.parser.session import create_client
from pprint import pprint

#функция отдает страницу с расписанием в html по заданному диапазону даты
def fetch_schedule(client: httpx.Client, base_url: str, group: str, date_from: str, date_to: str) -> str:
    
    schedule_url = f"{base_url}/public-schedule/group"
    params = {'id': group, 'dateFrom': date_from, 'dateTo': date_to}

    response = client.get(schedule_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        raise RuntimeError(f"Failed to fetch schedule: status {response.status_code}")

#парсит расписание в виде массива из словарей
def parse_schedule(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    #список где сначала идет дата, потом пары(каждая пара отдельный элемент)
    all_tags = soup.find_all("div", class_=["date-bar", "lesson-item"])
    current_date = ""
    schedule = []

    #проходимся по массиву, когда встречаем блок с датой, указываем текущую дату. если блок с парой, вынимаем необходимые значения и вносим новый словарь
    for tag in all_tags:
        if "date-bar" in tag["class"]:
            current_date = tag.text.strip()
        else:
            number = int(tag.find("div", class_="lesson-number").contents[0].text.strip())

            time_text = tag.find("div", class_="lesson-time").text.strip()
            parts = time_text.split("–")
            time_start = parts[0].strip()
            time_end = parts[1].strip()

            title = tag.find("div", class_="lesson-title").text.strip()
            auditorium_tag = tag.find("span", class_="lesson-auditorium")
            if auditorium_tag:
                auditorium = auditorium_tag.text.strip()
            else:
                auditorium = None

            details_text = tag.find("div", class_="lesson-details").get_text(" ", strip=True)
            if "Преподаватель:" in details_text:
                teacher = details_text.split("Преподаватель:", 1)[1].strip()
            else:
                teacher = None

            lesson_type = tag.find("div", class_="lesson-type").text.strip()

            schedule.append({
                "date": current_date,
                "number": number,
                "time_start": time_start,
                "time_end": time_end,
                "title": title,
                "auditorium" :auditorium,
                "teacher": teacher,
                "lesson_type": lesson_type,
            })
    return schedule  
        

def main():
    load_dotenv()
    base_url = os.environ["UNI_BASE_URL"]
    group = "МПИ26"
    date_from = "2026-10-12"
    date_to = "2026-10-18"
    with create_client() as client:
        html_schedule = fetch_schedule(client, base_url, group, date_from, date_to)
    


    # with open("schedule.html", encoding="utf-8") as f:
    #     html_schedule = f.read()

    
    schedule = parse_schedule(html_schedule)


    pprint(schedule)
    



if __name__ == "__main__":
    main()