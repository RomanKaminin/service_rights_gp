import aiohttp
import aiohttp_jinja2
import datetime
from .models import Entry
import requests
import re
from bs4 import BeautifulSoup

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
            result = requests.get(req_url)
            page = result.text
            soup = BeautifulSoup(page, 'html.parser')
            person = {}

            for div in soup.find_all("a", class_="hrTbp"):
                if div.text in DETAILS:
                    raise Exception('нашёл!')

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

