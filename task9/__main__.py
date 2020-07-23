import asyncio
from nats.aio.client import Client as NATS
from aioconsole import ainput
import argparse

pr = argparse.ArgumentParser()
pr.add_argument('-r', action="store", dest='room', required=True)
pr.add_argument('-n', action="store", dest='name', required=True)
arg = pr.parse_args()


async def run(loop):
    nc = NATS()

    await nc.connect("127.0.0.1:4222", loop=loop)

    async def message_handler(msg):
        data = msg.data.decode()
        print("Received a message: " + data)

    # Simple publisher and async subscriber via coroutine.
    sid = await nc.subscribe(arg.room, cb=message_handler)
    while True:
        line = await ainput(">>> ")
        if line == "/exit":
            break
        if len(line) > 0:
            await nc.publish(arg.room, (arg.name+": "+line).encode())

    await nc.unsubscribe(sid)

    # Terminate connection to NATS.
    await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()
