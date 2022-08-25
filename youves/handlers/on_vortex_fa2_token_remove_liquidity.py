from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models
from youves.utils import symbols


async def on_vortex_fa2_token_remove_liquidity(
    _ctx: HandlerContext, remove_liquidity
) -> None:
    symbol = symbols.dex_to_symbol_map.get(remove_liquidity.data.target_address, "")
    await models.Trade.create(
        type=models.TradeType.DIVEST,
        owner_address=remove_liquidity.data.sender_address,
        dex_contract_address=remove_liquidity.data.target_address,
        symbol=symbol,
        lp_token_total_supply=Decimal(remove_liquidity.storage.lqtTotal),
        created=remove_liquidity.data.timestamp,
        token_1_pool=Decimal(remove_liquidity.storage.xtzPool),
        token_2_pool=Decimal(remove_liquidity.storage.tokenPool),
        token_2_address=remove_liquidity.storage.tokenAddress,
    )
