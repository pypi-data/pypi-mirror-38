import eelgraph.colors as colors
import json


class Chart(object):
    obj = {}

    def recalc(self):
        pass

    def tojson(self):
        self.recalc()
        return json.dumps(self.obj)


class Doughnut(Chart):
    def __init__(self, data, colorSet=colors.best):
        self.data = data
        self.colors = {
            label: colors.randomColor(colorSet, True)
            for label, _ in self.data.items()
        }

    def recalc(self):
        bgColors = [colors.stroke(self.colors[k])
                    for k, v in self.data.items()]
        self.obj = {
            'type': 'doughnut',
            'data': {
                'datasets': [{
                    'data': [v for k, v in self.data.items()],
                    'backgroundColor': bgColors
                }],
                'labels': [k for k, v in self.data.items()]
            }
        }


class Line(Chart):
    def __init__(self, data=[], *args, lines=1, labels=None, radius=2.5,
                 fill=None, smooth=None, color=None):
        self.data = data
        if labels is None:
            self.labels = [""
                           for _ in range(self.lines)]
        else:
            self.labels = labels
        self.radius = radius
        self.lines = lines
        if color is None:
            self.colors = [colors.randomColor(colorSet=colors.best)
                           for _ in range(self.lines)]
        else:
            self.colors = color
        if fill is None:
            self.fill = [False for _ in range(self.lines)]
        else:
            self.fill = fill
        if smooth is None:
            self.smooth = [0.0 for _ in range(self.lines)]
        else:
            self.smooth = smooth

    def calcsets(self):
        sets = []
        for n in range(self.lines):
            sets.append({
                'label': self.labels[n],
                'data': [{'x': p[0], 'y': p[1][n]} for p in self.data],
                'backgroundColor': colors.fill(self.colors[n]),
                'borderColor': colors.stroke(self.colors[n]),
                'pointRadius': self.radius,
                'fill': self.fill[n],
                'lineTension': self.smooth[n]
            })
        return sets

    def recalc(self):
        self.obj = {
            'type': 'line',
            'data': {
                'datasets': self.calcsets(),
                'labels': ["%.02f" % p[0] for p in self.data]
            }
        }
