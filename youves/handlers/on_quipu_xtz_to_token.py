from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models
from youves.utils import symbols


async def on_quipu_xtz_to_token(
    _ctx: HandlerContext,
    tez_to_token_payment,
) -> None:
    symbol = symbols.dex_to_symbol_map.get(tez_to_token_payment.data.target_address, "")
    await models.Trade.create(
        type=models.TradeType.BUY,
        owner_address=tez_to_token_payment.parameter.receiver,
        dex_contract_address=tez_to_token_payment.data.target_address,
        symbol=symbol,
        lp_token_total_supply=Decimal(
            tez_to_token_payment.storage.storage.total_supply
        ),
        created=tez_to_token_payment.data.timestamp,
        token_1_pool=Decimal(tez_to_token_payment.storage.storage.tez_pool),
        token_2_pool=Decimal(tez_to_token_payment.storage.storage.token_pool),
    )
