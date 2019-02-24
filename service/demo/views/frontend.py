import datetime
import aiohttp
import aiohttp_jinja2
from aiohttp_jinja2 import template


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

    # @template('index.html')
    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        # form = await request.post()
        # error = await validate_form(form)
        #обработка запроса


        # if error is None and form.get('text'):
        #     await self.mongo.message.insert_one(
        #         {
        #          'text': form['text'],
        #          'timestamp': datetime.datetime.utcnow()})
        #     return redirect(request, '/')
        # else:
        return {}

def redirect(request, name, **kw):
    router = request.app.router
    location = router[name].url_for(**kw)
    return aiohttp.web.HTTPFound(location=location)


async def validate_form(form):
    error = None
    if not form['text']:
        error = 'You have to enter a text'
    return error

