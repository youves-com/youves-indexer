from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models
from youves.utils import symbols


async def on_plenty_add_liquidity(_ctx: HandlerContext, add_liquidity) -> None:
    symbol = symbols.dex_to_symbol_map.get(add_liquidity.data.target_address, "")
    await models.Trade.create(
        type=models.TradeType.INVEST,
        owner_address=add_liquidity.data.sender_address,
        dex_contract_address=add_liquidity.data.target_address,
        symbol=symbol,
        lp_token_total_supply=Decimal(add_liquidity.storage.totalSupply),
        created=add_liquidity.data.timestamp,
        token_1_pool=Decimal(add_liquidity.storage.token1_pool),
        token_2_pool=Decimal(add_liquidity.storage.token2_pool),
        token_1_address=add_liquidity.storage.token1Address,
        token_2_address=add_liquidity.storage.token2Address,
    )
