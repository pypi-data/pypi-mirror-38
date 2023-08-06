# GlobalPy
The package **pyglobal** allows you to execute your python scripts globally

## Available on pypi
`pip install globalpy`

## How to use?

```
globalpy --help
    usage: globalize [-h] [--setup] [--target TARGET [TARGET ...]]
                 [--pyversion PYVERSION] [--alias ALIAS [ALIAS ...]]

    optional arguments:
        -h, --help            show this help message and exit
        --setup, -s           run only once after installing module
        --target TARGET [TARGET ...], -t TARGET [TARGET ...]
                              target file that should become a global command
                              (multiple targets possible)
        --pyversion PYVERSION, -p PYVERSION
                              choose the python version to execute in
        --alias ALIAS [ALIAS ...], -a ALIAS [ALIAS ...]
                        alias for the program
```

## Demo

`globalpy -t test.py - a myalias`


![alt img <>](demo/alias.png)

When no alias is specified, the filename will be used as an alias:  

`globalpy -t test.py`


![alt img <>](demo/default.png)

## License

License can be found [here](https://github.com/frankzl/globalpy/blob/master/LICENSE)


