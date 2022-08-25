from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models
from youves.utils import symbols


async def on_flat_cfmm_token_to_cash(_ctx: HandlerContext, token_to_cash) -> None:
    symbol = symbols.dex_to_symbol_map.get(token_to_cash.data.target_address, "")
    await models.Trade.create(
        type=models.TradeType.SELL,
        owner_address=token_to_cash.data.sender_address,
        dex_contract_address=token_to_cash.data.target_address,
        symbol=symbol,
        lp_token_total_supply=Decimal(token_to_cash.storage.lqtTotal),
        created=token_to_cash.data.timestamp,
        token_1_pool=Decimal(token_to_cash.storage.tokenPool),
        token_2_pool=Decimal(token_to_cash.storage.cashPool),
        token_1_address=token_to_cash.storage.tokenAddress,
        token_2_address=token_to_cash.storage.cashAddress,
    )
