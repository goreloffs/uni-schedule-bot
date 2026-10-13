import os
from dotenv import load_dotenv
import httpx
from bs4 import BeautifulSoup
from uni_schedule_bot.parser.session import create_client
from pprint import pprint


def fetch_schedule(client: httpx.Client, base_url: str, group: str, date_from: str, date_to: str) -> str:
    
    schedule_url = f"{base_url}/public-schedule/group"
    params = {'id': group, 'dateFrom': date_from, 'dateTo': date_to}

    response = client.get(schedule_url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        raise RuntimeError(f"Failed to fetch schedule: status {response.status_code}")

def parse_schedule(html: str) -> list[dict]:
    # schedule = []

    # soup = BeautifulSoup(html, "lxml")

    # date = soup.find("div", class_="date-bar").text.strip()
    # number = int(soup.find("div", class_="lesson-number").contents[0].text.strip())

    # time_text = soup.find("div", class_="lesson-time").text.strip()
    # parts = time_text.split("–")
    # time_start = parts[0].strip()
    # time_end = parts[1].strip()

    # title = soup.find("div", class_="lesson-title").text.strip()
    # auditorium = soup.find("span", class_="lesson-auditorium").text.strip()

    # details_text = soup.find("div", class_="lesson-details").get_text(" ", strip=True)
    # teacher = ""
    # if "Преподаватель:" in details_text:
    #     teacher = details_text.split("Преподаватель:", 1)[1].strip()
    # else:
    #     teacher = None




    # lesson_type = soup.find("div", class_="lesson-type").text.strip()

    # schedule[0]["date"] = date
    # schedule[0]["number"] = number
    # schedule[0]["time_start"] = time_start
    # schedule[0]["time_end"] = time_end
    # schedule[0]["title"] = title
    # schedule[0]["auditorium"] = auditorium
    # schedule[0]["teacher"] = teacher
    # schedule[0]["lesson_type"] = lesson_type

    soup = BeautifulSoup(html, "lxml")
    all_tags = soup.find_all("div", class_=["date-bar", "lesson-item"])
    current_date = ""
    schedule = []


    for tag in all_tags:
        if tag.attrs.get('class') == ['date-bar']:
            current_date = tag.text.strip()
            continue
        else:
            number = int(tag.find("div", class_="lesson-number").contents[0].text.strip())   #contents[0].text.strip()

            time_text = soup.find("div", class_="lesson-time").text.strip()
            parts = time_text.split("–")
            time_start = parts[0].strip()
            time_end = parts[1].strip()

            title = soup.find("div", class_="lesson-title").text.strip()
            auditorium = soup.find("span", class_="lesson-auditorium").text.strip()

            details_text = soup.find("div", class_="lesson-details").get_text(" ", strip=True)
            teacher = ""
            if "Преподаватель:" in details_text:
                teacher = details_text.split("Преподаватель:", 1)[1].strip()
            else:
                teacher = None

            lesson_type = soup.find("div", class_="lesson-type").text.strip()

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
        

        

    # while current_date == date:
    #     number = int(soup.find("div", class_="lesson-number").contents[0].text.strip())

    #     time_text = soup.find("div", class_="lesson-time").text.strip()
    #     parts = time_text.split("–")
    #     time_start = parts[0].strip()
    #     time_end = parts[1].strip()

    #     title = soup.find("div", class_="lesson-title").text.strip()
    #     auditorium = soup.find("span", class_="lesson-auditorium").text.strip()

    #     details_text = soup.find("div", class_="lesson-details").get_text(" ", strip=True)
    #     teacher = ""
    #     if "Преподаватель:" in details_text:
    #         teacher = details_text.split("Преподаватель:", 1)[1].strip()
    #     else:
    #         teacher = None

    #     lesson_type = soup.find("div", class_="lesson-type").text.strip()

    #     schedule.append({
    #         "date": current_date,
    #         "number": number,
    #         "time_start": time_start,
    #         "time_end": time_end,
    #         "title": title,
    #         "auditorium" :auditorium,
    #         "teacher": teacher,
    #         "lesson_type": lesson_type,
    #     })
    #     current_date = 1

    # for i in range(2):

    #     current_date = soup.find_all("div", class_=["date-bar", "lesson-number"])
        


    #     time_text = soup.find_all("div", class_="lesson-time")[i].text.strip()
    #     parts = time_text.split("–")

    #     details_text = soup.find_all("div", class_="lesson-details")[i].get_text(" ", strip=True)
    #     teacher = ""
    #     if "Преподаватель:" in details_text:
    #         teacher = details_text.split("Преподаватель:", 1)[1].strip()
    #     else:
    #         teacher = None
            
    #     schedule.append({
    #         "date": current_date[i].text.strip(),
    #         "number": int(soup.find_all("div", class_="lesson-number")[i].contents[0].text.strip()),
    #         "time_start": parts[0].strip(),
    #         "time_end": parts[1].strip(),
    #         "title": soup.find_all("div", class_="lesson-title")[i].text.strip(),
    #         "auditorium": soup.find_all("span", class_="lesson-auditorium").text.strip(),
    #         "teacher": teacher,
    #         "lesson_type": soup.find_all("div", class_="lesson-type")[i].text.strip(),
    #     })

    return schedule

    
        
    



def main():
    # load_dotenv()
    # base_url = os.environ["UNI_BASE_URL"]
    # try:
    #     client = create_client()
    #     html_schedule = fetch_schedule(client, base_url, "МПИ26", "2026-10-07", "2026-10-13")
    # finally:
    #     client.close()
    with open("schedule.html", encoding="utf-8") as f:
        html_schedule = f.read()

    
    date = parse_schedule(html_schedule)

    pprint(date)
    



if __name__ == "__main__":
    main()