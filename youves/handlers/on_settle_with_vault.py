from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_settle_with_vault(
    _ctx: HandlerContext,
    internal_settle_with_vault,
) -> None:
    vault = await models.Vault.get(
        owner=internal_settle_with_vault.parameter.vault_owner,
        engine_contract_address=internal_settle_with_vault.data.sender_address,
    )

    last_balance = vault.balance

    storage_vault = internal_settle_with_vault.storage.vault_contexts[
        internal_settle_with_vault.parameter.vault_owner
    ]

    vault.minted = Decimal(storage_vault.minted)
    vault.balance = Decimal(storage_vault.balance)

    await vault.save()
    await models.Activity.create(
        vault=vault,
        operation_hash=internal_settle_with_vault.data.hash,
        created=internal_settle_with_vault.data.timestamp,
        event=models.Event.SETTLE_WITH_VAULT,
        token_amount=Decimal(internal_settle_with_vault.parameter.token_amount),
        collateral_token_amount=last_balance - vault.balance,
        engine_contract_address=internal_settle_with_vault.data.sender_address,
    )
