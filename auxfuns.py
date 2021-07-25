trader_is = lambda trader: (trader.is_alive(), trader.is_positioned)

def trader_status(traders):
    return [falive: {trader_is(trader)[0]}, positioned: {trader_is(trader)[1]} for trader in traders]
