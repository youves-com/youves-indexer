from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_burn_vault(
    _ctx: HandlerContext,
    burn,
) -> None:
    vault = await models.Vault.get(
        owner=burn.data.sender_address, engine_contract_address=burn.data.target_address
    )

    burned_amount = (Decimal(burn.parameter.__root__) * Decimal(10**12)) // Decimal(
        burn.storage.compound_interest_rate
    )
    vault.minted = vault.minted - burned_amount
    await vault.save()

    await models.Activity.create(
        vault=vault,
        operation_hash=burn.data.hash,
        created=burn.data.timestamp,
        event=models.Event.BURN,
        token_amount=Decimal(burn.parameter.__root__),
        engine_contract_address=burn.data.target_address,
    )
