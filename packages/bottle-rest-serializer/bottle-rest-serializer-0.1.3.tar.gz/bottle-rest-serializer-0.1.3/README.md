bottle-rest-serializer
======================

Simple serializers for REST APIs built using [BottlePy](https://bottlepy.org/)
------------------------------------------------------------------------------

Default Python serializers don't work when your dicts/objects contains `datetime` or `Decimal` instances. This plugin is meant to fix this "issue".

- `datetime` instances will be converted to [ISO8601 strings](https://pt.wikipedia.org/wiki/ISO_8601).
- `Decimal` instances will be converted to `float`.

Installation
------------

`bottle-rest-serializer` is available from PyPI as `bottle-rest-serializer`:

```
pip install bottle-rest-serializer
```

**JSON Serializer:**
```python
from datetime import datetime
from decimal import Decimal

from bottle import Bottle, run
from truckpad.bottle.rest_serializer import FlexibleJSONPlugin

app = Bottle()
app.install(FlexibleJSONPlugin())

@app.get('/')
def index():
    return {
        'now': datetime.now(),
        'float_number': Decimal(123.4567),
        'int_number': Decimal(4567)
    }

if __name__ == '__main__':
    run(app)
```


**XML Serializer:**

*To be developed in the future :P*
