from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models
from youves.utils import symbols


async def on_quipu_token_to_xtz(
    _ctx: HandlerContext,
    token_to_tez_payment,
) -> None:
    symbol = symbols.dex_to_symbol_map.get(token_to_tez_payment.data.target_address, "")
    await models.Trade.create(
        type=models.TradeType.SELL,
        owner_address=token_to_tez_payment.parameter.receiver,
        dex_contract_address=token_to_tez_payment.data.target_address,
        symbol=symbol,
        lp_token_total_supply=Decimal(
            token_to_tez_payment.storage.storage.total_supply
        ),
        created=token_to_tez_payment.data.timestamp,
        token_1_pool=Decimal(token_to_tez_payment.storage.storage.tez_pool),
        token_2_pool=Decimal(token_to_tez_payment.storage.storage.token_pool),
    )
