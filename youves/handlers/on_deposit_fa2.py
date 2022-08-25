from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_deposit_fa2(
    _ctx: HandlerContext,
    deposit,
) -> None:
    new_balance = Decimal(deposit.parameter.__root__)
    vault = await models.Vault.get(
        address=deposit.data.sender_address,
        owner=deposit.data.sender_address,
        engine_contract_address=deposit.data.target_address,
    )
    vault.balance = vault.balance + new_balance
    await vault.save()
    await models.Activity.create(
        vault=vault,
        operation_hash=deposit.data.hash,
        created=deposit.data.timestamp,
        event=models.Event.DEPOSIT_IN_VAULT,
        collateral_token_amount=new_balance,
        engine_contract_address=deposit.data.target_address,
    )
