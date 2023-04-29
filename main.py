import requests
from bs4 import BeautifulSoup
import openpyxl


def set_cell(value):
    global c
    c += 1
    sheet.cell(r, c).value = value

workbook = openpyxl.Workbook()
sheet = workbook.active
r, c = 1, 0
set_cell('Название')
set_cell('Ссылка')
set_cell('Цена')
set_cell('Цена для юр.лиц')
set_cell('Скидка(если есть)')
set_cell('Наличие')
for i in range(1, 17):
    url_main = f'https://mydrone.ru/kupit/kvadrokopter/page-{i}'
    response = requests.get(url_main)
    soup = BeautifulSoup(response.content, 'html.parser')
    dron_page = soup.find_all('div', attrs={'class': 'ut2-gl__image'})
    url_page = []
    for dron in dron_page:
        url_page.append(dron.find('a')['href'])

    for url in url_page:
        r+=1
        c = 0
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        name = soup.find('h1',{'class':'ut2-pb__title'})
        price_main = soup.find('span', {'class': 'ty-price-num'})
        price_urlic = soup.find('span', {'class': 'ty-price-num my-legalentity-price-num'})
        price_promo = soup.find('span', {'class': 'ty-price-num my-promocode-price-num'})
        nalichie = soup.find('span', {'class': 'ty-qty-in-stock ty-control-group__item'})
        send_from = soup.find('span', {'class': 'ty-control-group__item'})
        set_cell(name.text)
        set_cell(url)
        set_cell(price_main.text)
        if price_urlic != None: set_cell(price_urlic.text)
        else: set_cell('None')
        if price_promo != None: set_cell(price_promo.text)
        else: set_cell('None')
        set_cell(nalichie.text.strip())
        # type_desc = soup.find_all('th',{'style':'box-sizing: border-box; padding: 6px 0px; text-align: left; width: 222px; color: #44a8f2; font-size: 12px; line-height: 1.4em; font-weight: 400; vertical-align: top;'})
        # desc = soup.find_all('td',{'style':'box-sizing: border-box; padding: 6px 0px 6px 10px; width: 333px; font-size: 12px; line-height: 1.4em; vertical-align: top;'})
#         Тех описание не у всех есть
workbook.save('file.xlsx')
workbook.close()

