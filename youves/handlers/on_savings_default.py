from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_savings_default(
    _: HandlerContext,
    default,
) -> None:
    # Update the savings pool
    savings_pool, _ = await models.SavingsPool.update_or_create(
        address=default.data.target_address
    )
    savings_pool.token_balance = Decimal(default.storage.last_balance)
    savings_pool.disc_factor = Decimal(default.storage.disc_factor)
    savings_pool.dist_factor = Decimal(default.storage.dist_factor)
    savings_pool.total_stake = Decimal(default.storage.total_stake)
    await savings_pool.save()

    # Update the savings activity
    models.SavingsActivity.filter(operation_hash=default.data.hash).update(
        collateral_token_amount=Decimal(default.data.amount),
        event=models.SavingsEvent.PAY_IN_SAVINGS,
    )
