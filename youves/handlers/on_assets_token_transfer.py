from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_assets_token_transfer(
    _: HandlerContext,
    transfers,
) -> None:
    for transfer in transfers.parameter.__root__:
        for tx in transfer.txs:
            token_amount = Decimal(tx.amount)
            await models.Transfer.create(
                operation_hash=transfers.data.hash,
                sender=transfer.from_,
                receiver=tx.to_,
                contract=transfers.data.target_address,
                token_amount=token_amount,
                token_id=int(tx.token_id),
                created=transfers.data.timestamp,
            )
