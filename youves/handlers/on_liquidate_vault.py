from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_liquidate_vault(
    _ctx: HandlerContext,
    liquidate,
) -> None:
    vault = await models.Vault.get(
        owner=liquidate.parameter.vault_owner,
        engine_contract_address=liquidate.data.target_address,
    )
    last_balance = vault.balance
    storage_vault = liquidate.storage.vault_contexts[liquidate.parameter.vault_owner]

    vault.minted = Decimal(storage_vault.minted)
    vault.balance = Decimal(storage_vault.balance)

    await vault.save()

    await models.Activity.create(
        vault=vault,
        operation_hash=liquidate.data.hash,
        created=liquidate.data.timestamp,
        event=models.Event.LIQUIDATE,
        token_amount=Decimal(liquidate.parameter.token_amount),
        collateral_token_amount=last_balance - vault.balance,
        engine_contract_address=liquidate.data.target_address,
    )
