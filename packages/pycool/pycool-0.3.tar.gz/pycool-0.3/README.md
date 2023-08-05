# pycool, simple script library

## install

```sh
$ pip install pycool
```

## usage

**pretty.py**:
```python
from pycool import *

args = parse('prettyprint a json file',[
        ('jfile',{'help':'path to json file'}),
        ('-i','--indent',{'action':'store_true'})
        ])

s = jget(args.jfile)
i = args.indent

print(jdumps(s, indent=i))
```

*in shell*:
```sh
$ python pretty.py -h
$ python pretty.py -i path/to/json
```

## note

- works with python 2 and 3
- resolves utf-8 encoding problem with python 2
