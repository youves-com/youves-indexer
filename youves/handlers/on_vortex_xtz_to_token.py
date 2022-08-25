from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models
from youves.utils import symbols


async def on_vortex_xtz_to_token(_ctx: HandlerContext, xtz_to_token) -> None:
    symbol = symbols.dex_to_symbol_map.get(xtz_to_token.data.target_address, "")
    await models.Trade.create(
        type=models.TradeType.BUY,
        owner_address=xtz_to_token.parameter.to,
        dex_contract_address=xtz_to_token.data.target_address,
        symbol=symbol,
        lp_token_total_supply=Decimal(xtz_to_token.storage.lqtTotal),
        created=xtz_to_token.data.timestamp,
        token_1_pool=Decimal(xtz_to_token.storage.xtzPool),
        token_2_pool=Decimal(xtz_to_token.storage.tokenPool),
        token_2_address=xtz_to_token.storage.tokenAddress,
    )
