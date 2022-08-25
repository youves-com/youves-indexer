from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_execute_intent(
    _ctx: HandlerContext,
    execute_intent,
) -> None:
    intent = await models.Intent.get(
        owner=execute_intent.data.sender_address,
        engine_contract_address=execute_intent.storage.engine_address,
    )
    intent.token_amount = intent.token_amount - Decimal(
        execute_intent.parameter.token_amount
    )
    if intent.token_amount <= 0:
        await intent.delete()
    else:
        await intent.save()
