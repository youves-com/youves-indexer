from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_fa12_transfer(
    ctx: HandlerContext,
    transfer,
) -> None:
    token_amount = Decimal(transfer.parameter.token_amount)
    await models.Transfer.create(
        operation_hash=transfer.data.hash,
        sender=transfer.parameter.from_,
        receiver=transfer.parameter.to,
        contract=transfer.data.target_address,
        token_amount=token_amount,
        token_id=None,
        created=transfer.data.timestamp,
    )
