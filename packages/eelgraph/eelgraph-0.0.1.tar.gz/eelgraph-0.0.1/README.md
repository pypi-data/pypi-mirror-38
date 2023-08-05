# eelgraph
### creates live chart.js charts from python

## Example Usage:
```py
import eelgraph
from eelgraph.charts import Doughnut

chart = Doughnut({
    "People who use 4 spaces": 5000,
    "People who use 2 spaces": 50
})

eelgraph.plot(chart, title="Secrets of the Universe")
```

## Installation
```
python3 setup.py install
```
