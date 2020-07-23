import time
from influxdb import InfluxDBClient


DB = "localhost"
DBNAME = "pract"
DBMES = "mesr"


class DataBase:
    def __init__(self):
        self._db_cli = InfluxDBClient(DB, database=DBNAME)

    def write_data(self, points: {}):
        if len(points) > 0:
            mes = {
                "measurement": DBMES,
                "fields": points
            }
            self._db_cli.write_points([mes])

    def get_data(self, begin_t=0, variables=None, end_t=None, epoch='ns'):
        qst = ''
        if variables is not None:
            params = ''
            for a in range(len(variables)):
                if a != 0:
                    params += ','
                params += variables[a]
        else:
            params = "*"
        if end_t is not None:
            qst = ' AND \"time\" < ' + str(end_t)
        query = "SELECT " + params + " FROM " + DBMES + " WHERE \"time\" > " + str(begin_t) + qst \
                + ' GROUP BY "time()"'
        time_begin = time.time()
        pts = self._db_cli.query(query, epoch=epoch)
        time_end = time.time() - time_begin

        return list(pts.get_points()), time_end
