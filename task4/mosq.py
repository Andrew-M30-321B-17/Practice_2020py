import asyncio
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1
import task3.api as ap
from task7.oauth import login, get_current_user, Depends, User

mqtt_address = 'mqtt://localhost'
mqtt: MQTTClient = None


def deploy():
    global mqtt
    if mqtt is None:
        mqtt = MQTTClient()
        yield from mqtt.connect(mqtt_address)


def loop_coroutine(topic, callback):
    global mqtt
    yield from deploy()
    yield from mqtt.subscribe([(topic, QOS_1)])
    runnig = True
    while runnig:
        message = yield from mqtt.deliver_message()
        packet = message.publish_packet
        runnig = callback(float(packet.payload.data.decode("utf-8")))
    yield from mqtt.disconnect()


def start_coroutine(topic, callback):
    asyncio.get_event_loop().create_task(loop_coroutine(topic, callback))


async def start_mqtt(topic: str, name: str, us: User = Depends(get_current_user)):
    def callback(a: float):
        ap.var_imitator.addv(name, a, False)
        return True
    start_coroutine(topic+'/'+name, callback)
    return ap.NORMAL_RESPONSE

ap.app.add_get('/smqtt', start_mqtt)
ap.app.add_post('/login', login)

if __name__ == '__main__':
    ap.app.start()
