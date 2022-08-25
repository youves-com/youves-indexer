from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_set_generic_prices(_: HandlerContext, fulfill) -> None:
    await set_generic_price(fulfill, "DEFI/USD", "DEFI")
    await set_generic_price(fulfill, "XTZ/USD", "XTZ")
    await set_generic_price(fulfill, "BTC/USD", "BTC")


async def set_generic_price(fulfill, symbol, token):
    if token in fulfill.storage.prices:
        await models.OraclePrice.create(
            oracle_address=fulfill.data.target_address,
            value=Decimal(fulfill.storage.prices[token]),
            created=fulfill.data.timestamp,
            symbol=symbol,
        )
