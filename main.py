import platform
import aiohttp
import asyncio
import argparse
from datetime import date, timedelta

CURRENT_DAY = date.today() # konstanta z obecną datą na moment zapytania
URL = 'https://api.privatbank.ua/p24api/exchange_rates?date=' # konstanta dla URL adresu PryvatBanku

def pars() -> dict: # funkcja do definicji argumentu  konsoli
    parser = argparse.ArgumentParser() # tworzymy obiekt klasy parsera
    parser.add_argument('-d', '--days', default='1', help='Number of days to ') # definiujemy argument dla liczby dni wstecz kursów walut
    args = vars(parser.parse_args()) # funkcja vars zwraca __dict__ atrybut dla obiektu (w tym przypadku obiektem jest 'parser'-obiekt typu ArgumentParser,
                                     # w którym funkcja parse_args() analizuje argumenty i przypisuje zgodnie z funkcją add_argument())'''
    return args # zwracamy wartości zadane w konsoli do późniejszych obliczeń daty, wartości zwrcane w postaci dict (w naszym przypadku {days: ilość dni zadana w konsoli}')

def days_list():
    days = [] # zmienna typu list dla tworzenia listy dat wstecz od obecnej w zależności od argumentu puktu wejścia (ilości)
    number_ask_days = int(pars().get('days')) # 
    for day in range(number_ask_days): # pętla do 
        if number_ask_days <= 10 :
            asked_day = CURRENT_DAY - timedelta(days=day)
            days.append(asked_day.strftime('%d.%m.%Y'))
        else:
            print('Too long period, please enter number of days less or equal 10')
            break
    return days

def url_list(days):
    urls = []
    for day in days:
        urls.append(f'{URL}{day}')
    return urls

async def convert(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    await format_json(result)
                    return result
                else:
                    print(f"Error status: {response.status} for {url}")
        except aiohttp.ClientConnectorError as er:
            print(f"Connection error: {url}", str(er))


async def format_json(data):
    date = data.get('date')
    res = {
        date : {
        'EUR': {
            'sale': 0.00,
            'purchase': 0.00
        },
        'USD': {
            'sale': 0.00,
            'purchase': 0.00
        }
        }
    }
    for i in data.get('exchangeRate'):
        if i.get('currency') in ('USD', 'EUR'):
            res.get(date).get(i.get('currency'))['sale']=i.get('saleRate')
            res.get(date).get(i.get('currency'))['purchase']=i.get('purchaseRate')
    print(res)
    return res


async def main():
    days = days_list()
    urls = url_list(days)
    tasks = [convert(url) for url in urls]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
