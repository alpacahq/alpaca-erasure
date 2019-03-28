import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
from io import StringIO

NY = 'America/New_York'
api = tradeapi.REST()

def load_sample():
    mapper = lambda x:{'Stock': 'symbol', 'Score': 'score'}.get(x)
    return pd.read_csv( 'sample.csv').rename( columns=mapper ).set_index('symbol')


def _get_prices(symbols, end_dt, max_workers=5):
    '''Get the map of DataFrame price data from Alpaca's data API.'''

    start_dt = end_dt - pd.Timedelta('50 days')
    start = start_dt.isoformat()
    end = end_dt.isoformat()

    def get_barset(symbols):
        return api.get_barset(
            symbols,
            'day',
            limit = 50,
            start=start,
            end=end
        )

    # The maximum number of symbols we can request at once is 200.
    barset = None
    idx = 0
    while idx <= len(symbols) - 1:
        if barset is None:
            barset = get_barset(symbols[idx:idx+200])
        else:
            barset.update(get_barset(symbols[idx:idx+200]))
        idx += 200

    return barset.df


def prices(symbols):
    '''Get the map of prices in DataFrame with the symbol name key.'''
    now = pd.Timestamp.now(tz=NY)
    end_dt = now
    if now.time() >= pd.Timestamp('09:30', tz=NY).time():
        end_dt = now - \
            pd.Timedelta(now.strftime('%H:%M:%S')) - pd.Timedelta('1 minute')
    return _get_prices(symbols, end_dt)


def calc_scores(price_df, dayindex=-1):
    '''Calculate scores based on the indicator and
    return the sorted result.
    '''
    diffs = {}
    param = 10
    for symbol in price_df.columns.levels[0]:
        df = price_df[symbol]
        if len(df.close.values) <= param:
            continue
        ema = df.close.ewm(span=param).mean()[dayindex]
        last = df.close.values[dayindex]
        diff = (last - ema) / ema
        diffs[symbol] = diff

    df = pd.DataFrame(diffs.items(), columns=('symbol', 'score')).set_index('symbol')
    df = df[pd.notnull(df.score)]
    df.score = df.score / np.linalg.norm(df.score) * -0.5 + 0.5
    return df

def main():
    symbols = load_sample().index
    price_df = prices(symbols)
    df = calc_scores(price_df)

    buf = StringIO()
    print(df.to_csv(buf))
    print(buf.getvalue())


if __name__ == '__main__':
    main()