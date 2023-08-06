# pypika-gis

SpatialTypes functions for extend [PyPika](https://github.com/kayak/pypika) with GIS.

## Example

```python
from pypika import Query
from pypika_gis import spatialtypes as st

query = Query.from_('field').select('id', st.AsGeoJSON('geom'))
print(str(query))
# SELECT "id",ST_AsGeoJSON('geom') FROM "field"

query = Query.from_('crop').select('id').where(st.Intersects('geom', st.SRID(st.MakePoint(10, 10))))
```

## Available functions

Check this list.

## Dependencies

- [PyPika](https://github.com/kayak/pypika)

## Setup

```bash
pip install pypika-gis
```

## Development

Full tests and coverage

```bash
pip install -r requirements-dev.txt
python -m pytest --cov
```

## Credits

pypika-gis is based on [PyPika](https://github.com/kayak/pypika). Check their page for further query buider instructions and examples.
