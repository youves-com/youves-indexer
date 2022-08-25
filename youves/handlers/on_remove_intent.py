from dipdup.context import HandlerContext

from youves import models


async def on_remove_intent(
    ctx: HandlerContext,
    remove_intent,
) -> None:
    await models.Intent.filter(
        owner=remove_intent.data.sender_address,
        engine_contract_address=remove_intent.storage.engine_address,
    ).delete()
