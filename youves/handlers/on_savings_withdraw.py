from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_savings_withdraw(
    _: HandlerContext,
    internal_withdraw,
) -> None:
    # Update the savings pool
    savings_pool, _ = await models.SavingsPool.get_or_create(
        address=internal_withdraw.data.target_address
    )
    savings_pool.token_balance = Decimal(internal_withdraw.storage.last_balance)
    savings_pool.disc_factor = Decimal(internal_withdraw.storage.disc_factor)
    savings_pool.dist_factor = Decimal(internal_withdraw.storage.dist_factor)
    savings_pool.total_stake = Decimal(internal_withdraw.storage.total_stake)
    await savings_pool.save()

    # Update the savings stake
    savings_stake, _ = await models.SavingsStake.get_or_create(
        pool_address=internal_withdraw.data.target_address,
        owner=internal_withdraw.storage.sender,
    )
    if (
        internal_withdraw.storage.sender
        in internal_withdraw.storage.dist_factors.keys()
    ):
        savings_stake.dist_factor = Decimal(
            internal_withdraw.storage.dist_factors[internal_withdraw.storage.sender]
        )
    if internal_withdraw.storage.sender in internal_withdraw.storage.stakes.keys():
        savings_stake.stake = Decimal(
            internal_withdraw.storage.stakes[internal_withdraw.storage.sender]
        )
    await savings_stake.save()

    # Update savings activity
    delta = Decimal(internal_withdraw.storage.dist_factor)
    token_delta = 0
    if (
        internal_withdraw.storage.sender
        in internal_withdraw.storage.dist_factors.keys()
    ):
        delta = delta - Decimal(
            internal_withdraw.storage.dist_factors[internal_withdraw.storage.sender]
        )

    if internal_withdraw.storage.sender in internal_withdraw.storage.stakes.keys():
        delta = delta * Decimal(
            internal_withdraw.storage.stakes[internal_withdraw.storage.sender]
        )
        token_delta = internal_withdraw.storage.stakes[internal_withdraw.storage.sender]
    else:
        delta = Decimal(0)

    await models.SavingsActivity.create(
        operation_hash=internal_withdraw.data.hash,
        event=models.SavingsEvent.WITHDRAW_FROM_SAVINGS,
        owner=internal_withdraw.storage.sender,
        created=internal_withdraw.data.timestamp,
        token_amount=token_delta
        * Decimal(internal_withdraw.storage.disc_factor)
        // Decimal(10**12),
        collateral_token_amount=delta // Decimal(10**12),
    )
