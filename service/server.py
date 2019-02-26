from aiohttp import web
import asyncio
from app.setup import init as app_init


def main():
    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(app_init(loop))
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    main()

