import eel
import os


name = "eelgraph"


def plot(chart, *args, options={}, title="electrograph", block=True):
    # Import web files
    webpath = os.path.join(os.path.dirname(__file__), 'ui')
    eel.init(webpath)
    # Send initial chart data to eel
    eel.init_chart(title, chart.tojson(), options)
    # Start eel server
    eel.start('chart.html', size=(640, 480), block=block)


def sleep(sec):
    eel.sleep(sec)


def update(chart):
    eel.update_chart(chart.tojson())
