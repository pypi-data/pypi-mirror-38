# Spaten for Python

This library enables you to work with Spaten files with Python.

Compatible with Python 3.5, 3.6, 3.7 and PyPy3.

## Installation

`pip install spaten`

## Usage

Reading Files:

```python
from spaten import File

for feature in File('your_file.spaten', readonly=True):
    # Do something with feature
    print(feature)
```

Writing Files:

```python
from shapely.geometry import Point
from spaten import Feature, File

with File('out.spaten') as sf:
    sf.append(Feature(Point(6.9, 50.9), {"class": "shop", "height": 12}))
```

You can also use a stream for reading and writing in one go:

```python
from spaten import File

with File('in_and_out.spaten') as sf:
    for feature in sf:
        if some_condition(feature):
            sf.append(apply_transformation(feature))
```
