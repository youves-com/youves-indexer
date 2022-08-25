from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_assets_token_burn(
    _ctx: HandlerContext,
    burn,
) -> None:
    token_amount = Decimal(burn.parameter.token_amount)
    await models.Transfer.create(
        operation_hash=burn.data.hash,
        sender=burn.parameter.owner,
        receiver="tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU",
        contract=burn.data.target_address,
        token_amount=token_amount,
        token_id=int(burn.parameter.token_id),
        created=burn.data.timestamp,
    )
