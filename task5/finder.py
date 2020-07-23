from task1.db_infl import DataBase


if __name__ == '__main__':
    a = input("Print vars like a b c or fill empty>> ")
    if a == "":
        params = None
    else:
        params = a.split(" ")
    a = input("Print begin time in s>> ")
    if a == "":
        a = 0
        c = None
    else:
        a = int(a) * 1000000000
        c = input("Print duration in s>> ")
        if c == "":
            c = None
        else:
            c = int(c) * 1000000000 + a

    req, timer = DataBase().get_data(a, params, c, epoch='s')
    print(req)
    print("duration: ", timer)
