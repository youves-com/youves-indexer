from dipdup.context import HandlerContext

from youves import models

ADDRESS_TO_SYMBOL = {
    "KT1HjoLU8KAgQYszocVigHW8TxUb8ZsdGTog": "USD/XTZ",
    "KT1UuqJiGQgfNrTK5tuR1wdYi5jJ3hnxSA55": "DEFI/USD",
}


async def on_set_price(
    _ctx: HandlerContext,
    set_price,
) -> None:
    await models.OraclePrice.create(
        oracle_address=set_price.data.target_address,
        value=set_price.storage.price,
        created=set_price.data.timestamp,
        symbol=ADDRESS_TO_SYMBOL[set_price.data.target_address],
    )
