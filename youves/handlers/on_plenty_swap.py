from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models
from youves.utils import symbols


async def on_plenty_swap(_ctx: HandlerContext, swap) -> None:
    symbol = symbols.dex_to_symbol_map.get(swap.data.target_address, "")
    await models.Trade.create(
        type=(
            models.TradeType.BUY
            if swap.parameter.requiredTokenId == swap.storage.token1Id
            else models.TradeType.SELL
        ),
        owner_address=swap.parameter.recipient,
        dex_contract_address=swap.data.target_address,
        symbol=symbol,
        lp_token_total_supply=Decimal(swap.storage.totalSupply),
        created=swap.data.timestamp,
        token_1_pool=Decimal(swap.storage.token1_pool),
        token_2_pool=Decimal(swap.storage.token2_pool),
        token_1_address=swap.storage.token1Address,
        token_2_address=swap.storage.token2Address,
    )
