from task1.emulate import VarImitator
from task1.db_infl import DataBase
import random
import time


if __name__ == "__main__":
    variables = VarImitator()
    data = DataBase()
    for a in "abcdefghijk":
        variables.addv(a, random.randint(0, 35))
    while True:
        vars_list = variables.get_variables()
        data.write_data(vars_list)
        print(time.time(), vars_list)
        variables.emulate()
        time.sleep(1)