import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re
from pprint import pprint


def find_true_info(text):
    pattern = r"django|flask"
    result = re.findall(pattern, text, flags=re.I)
    return result

def find_usd(salary):
    pattern = r"usd"
    result = re.findall(pattern, salary, flags=re.I)
    return result

def city(text):
    pattern = r"([А-ё-]+),| .*"
    result = re.sub(pattern, r"\1", text)
    return result

def get_headers():
    return Headers(browser="chrome", os="win").generate()



HOST = r"https://spb.hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=python&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=1&items_on_page=50"
headh_main_html = requests.get(HOST, headers=get_headers()).text
soup = BeautifulSoup(headh_main_html, features="lxml")
tag_div_list = soup.find_all('div', class_="serp-item")
info = []
info.clear()
# if len(find_true_info(description_body)) > 0:
print(len(tag_div_list))
for num, tag in enumerate(tag_div_list):
    link = tag.find('a', class_="serp-item__title")['href']
    city_name = tag.select_one('.bloko-text[data-qa=vacancy-serp__vacancy-address]').text
    job_name = tag.find('a', class_="bloko-link bloko-link_kind-tertiary").text
    
    description_html = requests.get(link, headers=get_headers()).text
    soup1 = BeautifulSoup(description_html, features="lxml")
    description_body = soup1.find(class_="vacancy-section").text
    tag_salary = soup1.find(class_="bloko-header-section-2 bloko-header-section-2_lite").text   

    if len(find_usd(tag_salary)) > 0:
        info.append({
                "Link": link,
                "Salary": tag_salary.replace(u"\xa0", ""),
                "Name": job_name.replace(u"\xa0", " "),
                "City": city(city_name)
            })

    # break
pprint(info)