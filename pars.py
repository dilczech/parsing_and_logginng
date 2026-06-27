from bs4 import BeautifulSoup
import lxml
import csv
import requests
import logging
import time
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler('logi.log', encoding="utf-8"), 
        logging.StreamHandler()       
    ]
)

# url = "https://winrating.ru/stats/league/1457"
# header = {
#     "Accept" : "*/*",
#     "user-agent":"Mozilla/5.0 (Linux; Android 15; Pixel 9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Mobile Safari/537.36"}

# req = requests.get(url, headers=header) 
# scr = req.text

with open("index.html", encoding="utf-8") as file:
    logging.info('Файл открыт')
    scr = file.read()

soup = BeautifulSoup(scr, "lxml")

table = soup.find(class_="stats__table league_table scroller__content")

# zagolovki
th_list = table.find("thead").find("tr").find_all("th")
logging.info('Получаю заголовки')
number_h = th_list[0].get_text(strip=True)      # No.
team_h = th_list[1].get_text(strip=True)        # Komanda
games_h = th_list[2].get_text(strip=True)       # Igry
wins_h = th_list[3].get_text(strip=True)        # Vyigryshi
draws_h = th_list[4].get_text(strip=True)       # Nichyi
losses_h = th_list[5].get_text(strip=True)      # Proigryshi
goal_diff_h = th_list[6].get_text(strip=True)   # Raznitsa Golov
goals_h = th_list[7].get_text(strip=True)       # Goly
points_h = th_list[8].get_text(strip=True)      # Ochki
form_h = th_list[9].get_text(strip=True)        # Forma
time.sleep(1)
logging.info('Заголовки успешно получены')

with open("data/output.csv", "w", newline="", encoding="utf-8") as f:
    cnt=1
    writer = csv.writer(f)
    writer.writerow((number_h, team_h, games_h, wins_h, draws_h, losses_h, goal_diff_h, goals_h, points_h))

    rows = table.find("tbody").find_all("tr")
    for row in rows:
        logging.info(f'Обрабатываю данные по команде {cnt}')
        cells = row.find_all("td")

        number = cells[0].text.strip()
        a = cells[1].find("a")
        full_span = a.find("span", class_="spoil-text__full")
        if full_span:
            team = full_span.get_text(strip=True).replace('"', '')
        else:
            team = a.get_text(strip=True).replace('"', '')
        games = cells[2].text.strip()
        wins = cells[3].text.strip()
        draws = cells[4].text.strip()
        losses = cells[5].text.strip()
        goal_diff = cells[6].text.strip()
        goals = cells[7].text.strip()
        points = cells[8].text.strip()

        writer.writerow((number, team, games, wins, draws, losses, goal_diff, goals, points))
        cnt+=1
        time.sleep(random.randint(1, 4))

logging.info('Закончили работу')