import vega_datasets

def stocks():
    return vega_datasets.data.stocks().pivot('date', 'symbol', 'price')