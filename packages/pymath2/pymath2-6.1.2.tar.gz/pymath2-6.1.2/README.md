# pymath

Perform calculations and graphing either on the command line or in the Python repl.  
Defines several common math functions not in the python standard library (found in the [pymath](https://github.com/cjbassi/pymath/tree/master/pymath) folder), and also imports the following:

- [math](https://docs.python.org/3/library/math.html)
- [statistics as stats](https://docs.python.org/3/library/statistics.html)
- [itertools as it](https://docs.python.org/3/library/itertools.html)
- [fractions as frac](https://docs.python.org/3/library/fractions.html)
- [decimal as dec](https://docs.python.org/3/library/decimal.html)
- [matplotlib.pyplot as plt](https://matplotlib.org/index.html)
- [numpy as np](https://www.numpy.org/)

## Installation

```shell
pip install [--user] pymath2
```

**Note**: `~/.local/bin` should be in your `$PATH` for `--user` installs.

## Usage

Run an expression from the command line:

```shell
> pymath 'factorial(5)+1'
121
```

Or perform multiple calculations in the Python repl:

```shell
> pymath
>>> xgcd(5, 2)
(1, 1, -2)
>>> primes(5)
[2, 3, 5, 7, 11]
>>>
```

List all available functions:

```shell
pymath -l
```
