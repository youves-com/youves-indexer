from decimal import Decimal

from dipdup.context import HandlerContext

from youves import models


async def on_mint_vault(
    _ctx: HandlerContext,
    mint,
) -> None:
    try:
        vault = await models.Vault.get(
            owner=mint.data.sender_address,
            engine_contract_address=mint.data.target_address,
        )
        amount = (Decimal(mint.parameter.__root__) * Decimal(10**12)) // Decimal(
            mint.storage.compound_interest_rate
        )
        vault.minted = vault.minted + amount
        await vault.save()

        await models.Activity.create(
            vault=vault,
            operation_hash=mint.data.hash,
            created=mint.data.timestamp,
            event=models.Event.MINT,
            token_amount=Decimal(mint.parameter.__root__),
            engine_contract_address=mint.data.target_address,
        )
    except Exception:
        pass
