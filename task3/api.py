import asyncio
from task1.db_infl import DataBase
from task1.emulate import VarImitator
from task3.web_server import WebServer

app = WebServer()
data_base = DataBase()
var_imitator = VarImitator()
imitate = False
times = {}


ERROR_RESPONSE = {"r": "EROOR"}
NORMAL_RESPONSE = {"r": "DONE"}


async def emulator():
    global imitate
    tts = 1
    last_time = 0
    while imitate:
        dc = var_imitator.get_variables()
        rd = {}
        if dc:
            for a in dc:
                if a in times:
                    times[a][0] -= last_time
                    if times[a][0] <= 0:
                        times[a][0] = times[a][1]
                        var_imitator.emulate()
                        rd[a] = dc[a]
                    if tts > times[a][0]:
                        tts = times[a][0]
                else:
                    rd[a] = dc[a]
            data_base.write_data(rd)
        if tts < 0.000001:
            tts = 0.001
        await asyncio.sleep(tts)
        last_time = tts


async def start_imitate():
    global imitate
    if imitate:
        return ERROR_RESPONSE
    imitate = True
    loop = asyncio.get_event_loop()
    loop.create_task(emulator())
    return NORMAL_RESPONSE


app.add_get('/begin', start_imitate)


async def stop_imitate():
    global imitate
    if not imitate:
        return ERROR_RESPONSE
    imitate = False
    return NORMAL_RESPONSE

app.add_get('/end', stop_imitate)


async def variable(name: str, bv: float = 1, flag: str = 'add', tts: float = 1.0):
    if flag == 'add':
        var_imitator.addv(name, bv)
        times[name] = [tts, tts]
        return NORMAL_RESPONSE
    elif flag == 'rem':
        rt = var_imitator.delv(name)
        if name in times:
            times.pop(name)
        if rt:
            return NORMAL_RESPONSE
        return ERROR_RESPONSE
    return ERROR_RESPONSE


app.add_get('/var_func', variable)


async def av():
    ms = var_imitator.get_variables()
    return {"variables_count": len(ms), "vars": ms}

app.add_get('/av', av)


if __name__ == "__main__":
    app.start()
