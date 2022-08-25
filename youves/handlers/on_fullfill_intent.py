from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_fullfill_intent(
    _ctx: HandlerContext,
    fulfill_intent,
) -> None:
    if hasattr(fulfill_intent.parameter, "address"):
        intent = await models.Intent.get(
            owner=fulfill_intent.parameter.address,
            engine_contract_address=fulfill_intent.storage.engine_address,
        )
    else:
        intent = await models.Intent.get(
            owner=fulfill_intent.parameter.__root__,
            engine_contract_address=fulfill_intent.storage.engine_address,
        )

    if intent.owner in fulfill_intent.storage.intents:
        intent.token_amount = Decimal(
            fulfill_intent.storage.intents[intent.owner].token_amount
        )
        await intent.save()
    else:
        await intent.delete()
