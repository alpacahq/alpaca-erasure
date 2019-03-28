# Alpaca - Erasure

This script is an example code that calcualtes stock scores every day using
latest price data. With the output of this script, you can build daily
rebalancing long-short algorithm.

The score is calculated using exponential weighted moving average with span=10,
and take the difference from last day closing price. The value range is between 0 and 1
with 0 being most overvalued and 1 being most undervalued. For more information,
please take a look at the reference below.

# How to

Install `alpaca-trade-api`

```sh
$ pip install alpaca-trade-api
```

and run erasure.py

```sh
$ python erasure.py
```

It outputs something like below.

```
...
PFIE,0.5015664246239445
PFIS,0.4997877550102791
PFNX,0.4768029748467622
PFPT,0.500816891906715
PFS,0.5010411315523059
PFSI,0.5053465393041152
PFSW,0.5149531269639088
PG,0.49686832450835694
PGC,0.5057306188423834
PGNX,0.4998828329411989
PGR,0.498740133468462
PGRE,0.5007967622834778
PGTI,0.5019629289791301
...
```

## Reference
The part of scoring logic was extracted from
[Alpaca tutorial algorithm](https://github.com/alpacahq/samplealgo01)