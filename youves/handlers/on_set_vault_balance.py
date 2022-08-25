from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_set_vault_balance(
    _ctx: HandlerContext,
    set_vault_balance,
) -> None:
    vault = await models.Vault.get(
        address=set_vault_balance.data.sender_address,
        engine_contract_address=set_vault_balance.data.target_address,
    )
    last_balance = vault.balance
    vault.balance = Decimal(set_vault_balance.parameter.__root__)
    await vault.save()

    if not await models.Activity.filter(
        operation_hash=set_vault_balance.data.hash
    ).exists():
        if Decimal(vault.balance) > Decimal(set_vault_balance.parameter.__root__):
            await models.Activity.create(
                vault=vault,
                operation_hash=set_vault_balance.data.hash,
                created=set_vault_balance.data.timestamp,
                event=models.Event.WITHDRAW_FROM_VAULT,
                collateral_token_amount=Decimal(vault.balance)
                - Decimal(set_vault_balance.parameter.__root__),
                engine_contract_address=set_vault_balance.data.target_address,
            )
        else:
            await models.Activity.create(
                vault=vault,
                operation_hash=set_vault_balance.data.hash,
                created=set_vault_balance.data.timestamp,
                event=models.Event.DEPOSIT_IN_VAULT,
                collateral_token_amount=Decimal(set_vault_balance.parameter.__root__)
                - Decimal(last_balance),
                engine_contract_address=set_vault_balance.data.target_address,
            )
