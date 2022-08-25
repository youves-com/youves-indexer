from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_savings_deposit(
    _ctx: HandlerContext,
    internal_deposit,
) -> None:
    # Update the savings pool
    savings_pool, _ = await models.SavingsPool.get_or_create(
        address=internal_deposit.data.target_address
    )
    savings_pool.token_balance = Decimal(internal_deposit.storage.last_balance)
    savings_pool.disc_factor = Decimal(internal_deposit.storage.disc_factor)
    savings_pool.dist_factor = Decimal(internal_deposit.storage.dist_factor)
    savings_pool.total_stake = Decimal(internal_deposit.storage.total_stake)
    await savings_pool.save()

    # Update the savings stake
    savings_stake, _ = await models.SavingsStake.get_or_create(
        pool_address=internal_deposit.data.target_address,
        owner=internal_deposit.storage.sender,
    )
    if internal_deposit.storage.sender in internal_deposit.storage.dist_factors.keys():
        savings_stake.dist_factor = Decimal(
            internal_deposit.storage.dist_factors[internal_deposit.storage.sender]
        )
    if internal_deposit.storage.sender in internal_deposit.storage.stakes.keys():
        savings_stake.stake = Decimal(
            internal_deposit.storage.stakes[internal_deposit.storage.sender]
        )
    await savings_stake.save()

    # Update savings activity
    delta = Decimal(internal_deposit.storage.dist_factor)
    if internal_deposit.storage.sender in internal_deposit.storage.dist_factors.keys():
        delta = delta - Decimal(
            internal_deposit.storage.dist_factors[internal_deposit.storage.sender]
        )

    if internal_deposit.storage.sender in internal_deposit.storage.stakes.keys():
        delta = delta * Decimal(
            internal_deposit.storage.stakes[internal_deposit.storage.sender]
        )
    else:
        delta = Decimal(0)

    await models.SavingsActivity.create(
        operation_hash=internal_deposit.data.hash,
        event=models.SavingsEvent.DEPOSIT_IN_SAVINGS,
        owner=internal_deposit.storage.sender,
        created=internal_deposit.data.timestamp,
        token_amount=Decimal(internal_deposit.parameter.__root__),
        collateral_token_amount=delta // Decimal(10**12),
    )
