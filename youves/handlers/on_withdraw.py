from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_withdraw(
    _ctx: HandlerContext,
    withdraw,
) -> None:
    vault = await models.Vault.get(
        owner=withdraw.storage.sender,
        engine_contract_address=withdraw.data.target_address,
    )

    last_balance = vault.balance

    storage_vault = withdraw.storage.vault_contexts[withdraw.storage.sender]
    vault.balance = Decimal(storage_vault.balance)
    await vault.save()

    await models.Activity.create(
        vault=vault,
        operation_hash=withdraw.data.hash,
        created=withdraw.data.timestamp,
        event=models.Event.WITHDRAW_FROM_VAULT,
        collateral_token_amount=last_balance - vault.balance,
        engine_contract_address=withdraw.data.target_address,
    )
