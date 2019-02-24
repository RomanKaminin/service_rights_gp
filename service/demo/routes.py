from .views import frontend


def setup_routes(app, handler, project_root):
    router = app.router
    h = handler
    # router.add_post('/', h.index, name='index')
    router.add_route('GET', '/', h.index),
    router.add_static('/static/', path=str(project_root / 'static'),
                      name='static')

# def setup_routes(app):
#     app.router.add_route('GET', '/', frontend.index)

