import aiohttp
import aiohttp_jinja2
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

        if error is None and form.get('test'):
            await self.mongo.message.insert(
                {
                    'text': form.get('test'),
                    # 'timestamp': datetime.datetime.utcnow()
                }
            )
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

