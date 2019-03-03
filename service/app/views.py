import aiohttp
import aiohttp_jinja2
import datetime
from .models import Entry
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bson import json_util
import json

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
        app_id = form.get('test').split('id=')[1]
        if re.match(
                r'((https|http):\/\/)(play\.google\.com\/store\/apps\/details\?id=)?(.*)?(&hl=ru|&hl=en)?$', req_url)\
                and error is None:
            #делаем запрос проверяем нет ли в базе по app_id
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(req_url)
            driver.find_elements_by_css_selector('a.hrTbp ')[2].click()
            data = {
                'id': app_id,
                'time': datetime.datetime.utcnow(),
            }
            app_name = driver.find_element_by_class_name("AHFaub").text
            permissions = {'app_name': app_name}
            block_permissions = driver.find_elements_by_class_name("yk0PFc")
            for e in block_permissions:
                key_block = e.find_element_by_class_name("BR7Zgd").text
                val_block = [entry.text for entry in e.find_elements_by_tag_name('li')]
                permissions.update({key_block: val_block})
            up_data = json.dumps(permissions, ensure_ascii=False)
            data.update({'app_data': json_util.loads(up_data)})
            entry = Entry(self.mongo)
            await entry.save(data=data)
            driver.quit()
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

