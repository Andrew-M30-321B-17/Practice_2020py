from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import sys
import random

from task1.db_infl import DataBase


class MainWindow():
    def __init__(self):
        self._db = DataBase()
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title="influx")
        self.win.resize(600, 600)
        self.win.setBackground('w')
        self._last_measure = 0
        self._data_holder = {}
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        self.canvas = self.win.addPlot()
        self.canvas.addLegend()
        timer = QtCore.QTimer()
        timer.timeout.connect(self._update_plot)
        timer.start(50)
        self.start()

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def trace(self, name, data_x, data_y):
        if name in self._data_holder:
            self._data_holder[name]["time"].append(data_x)
            self._data_holder[name]["y"].append(data_y)
            self._data_holder[name]["plot"].setData(self._data_holder[name]["time"], self._data_holder[name]["y"])
        else:
            self._data_holder[name] = {"plot": self.canvas.plot([data_x], [data_y], name=name,
                                                          pen=(random.randint(0, 200), random.randint(0, 200),
                                                               random.randint(0, 200))),
                                 "time": [],
                                 "y": []
                                 }

    def _update_plot(self):
        res, _ = self._db.get_data(self._last_measure)
        time_l = self._last_measure
        for measure in res:
            time_l = int(measure.pop("time"))
            for variable in measure:
                if measure[variable] is None:
                    continue
                self.trace(variable, time_l, float(measure[variable]))
        self._last_measure = time_l


if __name__ == '__main__':
    MainWindow()