import random


class MyVar:
    def __init__(self, value, not_from_mqtt = True):
        self.emulate = not_from_mqtt
        self.value = float(value)


class VarImitator:
    def __init__(self):
        self._var = {}

    def addv(self, name, val, not_from_mqtt=True):
        self._var[name] = MyVar(val, not_from_mqtt)

    def delv(self, name):
        if name not in self._var:
            return False
        self._var.pop(name)
        return True

    def emulate(self):
        for a in self._var:
            if self._var[a].emulate:
                self._var[a].value += -1 + 2 * random.randint(0, 1)

    def get_variables(self):
        rm = {}
        for a in self._var:
            rm[a] = float(self._var[a].value)
        return rm
