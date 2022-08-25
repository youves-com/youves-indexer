from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_assets_token_mint(
    _ctx: HandlerContext,
    mint,
) -> None:
    token_amount = Decimal(mint.parameter.token_amount)
    await models.Transfer.create(
        operation_hash=mint.data.hash,
        sender="tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU",
        receiver=mint.parameter.owner,
        contract=mint.data.target_address,
        token_amount=token_amount,
        token_id=int(mint.parameter.token_id),
        created=mint.data.timestamp,
    )
