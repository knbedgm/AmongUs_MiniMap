import asyncio
import threading

import socketio
from aiohttp import web
from aiohttp_index import IndexMiddleware

sio = socketio.AsyncServer(logger=False, engineio_logger=False, ping_interval=0.25, ping_timeout=10)  # stupid ping interval cause client only receives data after it pings due to thread weirdness
app = web.Application(middlewares=[IndexMiddleware()])
sio.attach(app)

app.router.add_static('/', './webroot')



runner = web.AppRunner(app)


def run_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    loop.run_until_complete(site.start())
    loop.run_forever()


t = threading.Thread(target=run_server)
t.daemon = True


def run():
    t.start()

if __name__ == "__main__":
    print("Press Enter to Quit")
    run()
    input()


__all__ = ['sio', 'run']
