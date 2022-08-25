from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models
from youves.utils import symbols


async def on_flat_cfmm_cash_to_token(_ctx: HandlerContext, cash_to_token) -> None:
    symbol = symbols.dex_to_symbol_map.get(cash_to_token.data.target_address, "")
    await models.Trade.create(
        type=models.TradeType.BUY,
        owner_address=cash_to_token.data.sender_address,
        dex_contract_address=cash_to_token.data.target_address,
        symbol=symbol,
        lp_token_total_supply=Decimal(cash_to_token.storage.lqtTotal),
        created=cash_to_token.data.timestamp,
        token_1_pool=Decimal(cash_to_token.storage.tokenPool),
        token_2_pool=Decimal(cash_to_token.storage.cashPool),
        token_1_address=cash_to_token.storage.tokenAddress,
        token_2_address=cash_to_token.storage.cashAddress,
    )
