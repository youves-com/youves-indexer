from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_savings_bailout(
    _: HandlerContext,
    internal_bailout,
) -> None:
    # Update the savings pool
    savings_pool, _ = await models.SavingsPool.get_or_create(
        address=internal_bailout.data.target_address
    )
    savings_pool.token_balance = Decimal(internal_bailout.storage.last_balance)
    savings_pool.disc_factor = Decimal(internal_bailout.storage.disc_factor)
    savings_pool.dist_factor = Decimal(internal_bailout.storage.dist_factor)
    savings_pool.total_stake = Decimal(internal_bailout.storage.total_stake)
    await savings_pool.save()

    # Update the savings activity.
    await models.SavingsActivity.create(
        operation_hash=internal_bailout.data.hash,
        event=models.SavingsEvent.BAILOUT_WITH_SAVINGS,
        created=internal_bailout.data.timestamp,
        token_amount=Decimal(internal_bailout.parameter.__root__),
        collateral_token_amount=0,
    )
