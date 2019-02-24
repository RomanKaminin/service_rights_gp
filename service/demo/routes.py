
def setup_routes(app, handler, project_root):
    router = app.router
    router.add_get('/', handler.index, name='index')
    router.add_post('/data', handler.get_data, name='get_data')
    router.add_static(
        '/static/', path=str(project_root / 'static'), name='static')





