from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_bailout_vault(
    _ctx: HandlerContext,
    bailout,
) -> None:
    vault = await models.Vault.get(
        owner=bailout.storage.sender,
        engine_contract_address=bailout.data.sender_address,
    )

    last_balance = vault.balance

    storage_vault = bailout.storage.vault_contexts[bailout.storage.sender]

    vault.minted = Decimal(storage_vault.minted)
    vault.balance = Decimal(storage_vault.balance)

    await vault.save()

    await models.Activity.create(
        vault=vault,
        operation_hash=bailout.data.hash,
        created=bailout.data.timestamp,
        event=models.Event.BAILOUT,
        token_amount=Decimal(bailout.parameter.__root__),
        collateral_token_amount=last_balance - vault.balance,
        engine_contract_address=bailout.data.target_address,
    )
