from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_advertise_intent(
    _ctx: HandlerContext,
    advertise_intent,
) -> None:
    intent, _ = await models.Intent.get_or_create(
        owner=advertise_intent.data.sender_address,
        engine_contract_address=advertise_intent.storage.engine_address,
    )
    intent.start_timestamp = advertise_intent.data.timestamp
    intent.token_amount = Decimal(advertise_intent.parameter.__root__)
    await intent.save()
