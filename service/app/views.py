import aiohttp
import aiohttp_jinja2
import datetime
from .models import Entry
from aiohttp_jinja2 import template


# routes = aiohttp.web.RouteTableDef()

# @template('index.html')
# async def index(request):
#     return {}
#     # return aiohttp.web.Response(text="ok")


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
        # обработка запроса
        # парсить адрес
        # делать запрос
        # забирать данные
        if error is None and form.get('test'):
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

