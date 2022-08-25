from dipdup.context import HandlerContext

from youves import models


async def on_create_vault(
    ctx: HandlerContext,
    create_vault,
) -> None:
    if (
        create_vault.data.sender_address not in create_vault.storage.vault_contexts
    ):  # this is unintuitive but because the vault context is already there its not in the storage change of the operation
        vault = await models.Vault.get(
            owner=create_vault.data.sender_address,
            engine_contract_address=create_vault.data.target_address,
        )
    else:
        if hasattr(
            create_vault.storage.vault_contexts[create_vault.data.sender_address],
            "address",
        ):
            vault_address = create_vault.storage.vault_contexts[
                create_vault.data.sender_address
            ].address
        else:
            vault_address = create_vault.data.sender_address

        vault, created = await models.Vault.get_or_create(
            owner=create_vault.data.sender_address,
            address=vault_address,
            engine_contract_address=create_vault.data.target_address,
        )
        await models.Activity.create(
            vault=vault,
            operation_hash=create_vault.data.hash,
            created=create_vault.data.timestamp,
            event=models.Event.CREATE_VAULT,
            collateral_token_amount=create_vault.data.amount or 0,
            engine_contract_address=create_vault.data.target_address,
        )

    if vault.balance is None:
        vault.balance = 0

    if create_vault.data.amount is not None:
        vault.balance += create_vault.data.amount

    await vault.save()
