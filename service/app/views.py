import aiohttp
import aiohttp_jinja2
import datetime
from .models import Entry
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

DETAILS = ["Подробнее…", "View details"]


class SiteHandler:
    def __init__(self, mongo):
        self._mongo = mongo

    @property
    def mongo(self):
        return self._mongo

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        return {}

    @aiohttp_jinja2.template('index.html')
    async def get_data(self, request):
        form = await request.post()
        error = await validate_form(form)
        req_url = form.get('test')

        if re.match(
                r'((https|http):\/\/)(play\.google\.com\/store\/apps\/details\?id=)?(.*)?(&hl=ru|&hl=en)?$', req_url)\
                and error is None:
            #делаем запрос проверяем нет ли в базе
            # options = Options()
            # options.add_argument("--headless")
            # driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe',
            #                           chrome_options=options)  # Optional argument, if not specified will search path.
            # driver.get(url)
            # soup = BeautifulSoup(driver.page_source)
            driver = webdriver.Chrome(ChromeDriverManager().install())
            # driver = webdriver.Chrome()
            options = Options()
            options.add_argument("--headless")
            driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)
            driver.get(req_url)
            page = driver.page_source


            # result = requests.get(req_url)
            # page = result.text
            soup = BeautifulSoup(page, 'html.parser')

            for div in soup.find_all("a", class_="hrTbp"):
                if div.text in DETAILS:
                    # делаем клик открывается новы html
                    result_data = {}
                    for div_permissions in soup.find_all("div", class_="yk0PFc"):
                        raise Exception('нашёл! yk0PFc')
                        title_div = div_permissions.find('div', attrs={'class': 'tDgPAd'})
                        key_block = title_div.find('span', class_='text').text
                        values_block = []
                        for li in div_permissions.find_all('li', class_='NLTG4'):
                            values_block.append(li.text)
                        entry_permission = {key_block: values_block}
                        result_data.update(entry_permission)


            # парсим и забираем данные

            data = {
                'id': form.get('test'),
                'time': datetime.datetime.utcnow(),
                #         {'id': data['id'],
                #          # 'hl': data['hl'],
                #          'time': data['time'],
                #          # 'identity': data,
                #          # 'contacts': data,
                #          # 'location': data,
                #          # 'phone': data,
                #          # 'pmf': data['Photos/Media/Files'],
                #          # 'storage': data,
                #          # 'camera': data,
                #          # 'microphone': data,
                #          # 'wifi': data['Wi-Fi connection information'],
                #          # 'device_information': data['Device ID & call information'],
                #          # 'phone2': data['Phone2'],
                #          # 'other': data['Other'],
                #          }
            }
            # запись в базу
            entry = Entry(self.mongo)
            await entry.save(data=data)
            #забирать данные из базы, писать в переменную и отправлять в шаблон с таблицей
            return redirect(request, 'index')
        else:
            return form


def redirect(request, name, **kw):
    router = request.app.router
    location = router[name].url_for(**kw)
    return aiohttp.web.HTTPFound(location=location)


async def validate_form(form):
    error = None
    if not form['test']:
        error = 'You have to enter a text'
    return error

