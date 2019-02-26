import os
import yaml
import pathlib
import aiohttp_jinja2
import motor.motor_asyncio as aiomotor
import jinja2
from aiohttp import web
from .routes import setup_routes
from .views import SiteHandler


PROJ_ROOT = pathlib.Path(__file__).parent.parent


async def init_mongo(conf, loop):
    host = os.environ.get('DOCKER_MACHINE_IP', '127.0.0.1')
    conf['host'] = host
    mongo_uri = "mongodb://{}:{}".format(conf['host'], conf['port'])
    conn = aiomotor.AsyncIOMotorClient(
        mongo_uri,
        io_loop=loop)
    db_name = conf['database']
    return conn[db_name]


async def setup_mongo(app, conf, loop):
    mongo = await init_mongo(conf['mongo'], loop)

    async def close_mongo(app):
        mongo.client.close()

    app.on_cleanup.append(close_mongo)
    return mongo


def load_config(fname):
    with open(fname, 'rt') as f:
        data = yaml.load(f)
    return data


async def init(loop):
    conf = load_config(PROJ_ROOT / 'config' / 'config.yml')
    app = web.Application(loop=loop)
    mongo = await setup_mongo(app, conf, loop)
    aiohttp_jinja2.setup(app,
                         loader=jinja2.PackageLoader('app', 'templates')
                         )
    handler = SiteHandler(mongo)
    setup_routes(app, handler, PROJ_ROOT)
    host, port = conf['host'], conf['port']
    return app, host, port


# async def create_app():
#     app = web.Application()
#     aiohttp_jinja2.setup(app,
#                          loader=jinja2.PackageLoader('app', 'templates')
#                          )
#     setup_routes(app)
#     return app

# def create_app(loop=None):
#     app = web.Application(loop=loop)
#     DBNAME = 'testdb'
#     mongo = AsyncIOMotorClient(io_loop=loop)
#     db = mongo[DBNAME]
#     app['db'] = db
#
#     async def cleanup(app):
#         mongo.close()
#
#     app.on_cleanup.append(cleanup)
#     aiohttp_jinja2.setup(app,
#                          loader=jinja2.PackageLoader('app', 'templates')
#                          )
#     setup_routes(app)
#     return app

# def create_app(loop=None):
#     app = web.Application()
#
#     client = MongoClient('localhost', 27017)
#     db = client.test_database
#     post = {"author": "Roman",
#             "text": "My first blog post!",
#             "tags": ["mongodb", "python", "pymongo"],
#             "date": datetime.datetime.utcnow()
#             }
#     posts = db.posts
#     post_id = posts.insert(post)
#     print(posts.find_one({"author": "Roman"}))
#     app['db'] = posts
#     aiohttp_jinja2.setup(app,
#                          loader=jinja2.PackageLoader('app', 'templates')
#                          )
#     setup_routes(app)
#     return app


# async def do_insert(db, document):
#     # document = {'key': 'value'}
#     result = await db.test_collection.insert(document)
#     print('result %s' % repr(result.inserted_id))


