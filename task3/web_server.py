import asyncio
from fastapi import FastAPI
from uvicorn import Server, Config


class WebServer:
    def __init__(self):
        self._web = FastAPI(docs_url=None, redoc_url=None)

    def add_get(self, path, f):
        self._web.get(path)(f)

    def add_post(self,path ,f):
        self._web.post(path)(f)

    def start(self):
        loop = asyncio.get_event_loop()
        config = Config(app=self._web, host="0.0.0.0", port=8083)
        server = Server(config)
        loop.run_until_complete(server.serve())
