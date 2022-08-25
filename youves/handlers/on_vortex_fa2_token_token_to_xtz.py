from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models
from youves.utils import symbols


async def on_vortex_fa2_token_token_to_xtz(_ctx: HandlerContext, token_to_xtz) -> None:
    symbol = symbols.dex_to_symbol_map.get(token_to_xtz.data.target_address, "")
    await models.Trade.create(
        type=models.TradeType.SELL,
        owner_address=token_to_xtz.parameter.to,
        dex_contract_address=token_to_xtz.data.target_address,
        symbol=symbol,
        lp_token_total_supply=Decimal(token_to_xtz.storage.lqtTotal),
        created=token_to_xtz.data.timestamp,
        token_1_pool=Decimal(token_to_xtz.storage.xtzPool),
        token_2_pool=Decimal(token_to_xtz.storage.tokenPool),
        token_2_address=token_to_xtz.storage.tokenAddress,
    )
