from decimal import Decimal
from enum import Enum

from tortoise import Model, fields

# from dipdup.models import Model
# from tortoise import fields
from tortoise.signals import pre_save


class Intent(Model):
    owner = fields.CharField(58)
    token_amount = fields.DecimalField(max_digits=40, decimal_places=0, default=0)
    start_timestamp = fields.DatetimeField(blank=True, null=True)
    engine_contract_address = fields.CharField(58)


class Vault(Model):
    address = fields.CharField(58)
    balance = fields.DecimalField(max_digits=40, decimal_places=0, default=0)
    is_being_liquidated = fields.BooleanField(default=False)
    allow_settlement = fields.BooleanField(default=True)
    minted = fields.DecimalField(max_digits=40, decimal_places=0, default=0)
    ratio = fields.FloatField(default=0)
    owner = fields.CharField(58, unique=False)  # "toplevel"
    engine_contract_address = fields.CharField(58)

    class Meta:
        unique_together = ("owner", "engine_contract_address", "address")


@pre_save(Vault)
async def vault_pre_save(sender, instance: Vault, using_db, update_fields) -> None:
    if instance.minted > 0:
        instance.ratio = float(instance.balance / instance.minted)
    else:
        instance.ratio = float("inf")


class SavingsPool(Model):
    address = fields.CharField(58, pk=True)
    disc_factor = fields.DecimalField(max_digits=40, decimal_places=0, default=0)
    dist_factor = fields.DecimalField(max_digits=40, decimal_places=0, default=0)
    total_stake = fields.DecimalField(
        max_digits=40,
        decimal_places=0,
        default=0,
    )
    token_balance = fields.DecimalField(
        max_digits=40,
        decimal_places=0,
        default=0,
    )
    collateral_token_balance = fields.DecimalField(
        max_digits=40, decimal_places=0, default=0
    )


class SavingsStake(Model):
    pool_address = fields.CharField(58)
    owner = fields.CharField(58, index=True)
    stake = fields.DecimalField(max_digits=40, decimal_places=0, default=0)
    dist_factor = fields.DecimalField(max_digits=40, decimal_places=0, default=0)


class SavingsEvent(str, Enum):
    DEPOSIT_IN_SAVINGS = "DEPOSIT_IN_SAVINGS"
    WITHDRAW_FROM_SAVINGS = "WITHDRAW_FROM_SAVINGS"
    BAILOUT_WITH_SAVINGS = "BAILOUT_WITH_SAVINGS"
    PAY_IN_SAVINGS = "PAY_IN_SAVINGS"


class SavingsActivity(Model):
    operation_hash = fields.CharField(51)
    owner = fields.CharField(58, index=True, null=True)
    event = fields.CharEnumField(SavingsEvent)
    created = fields.DatetimeField(auto_now_add=True, use_tz=True, index=True)
    token_amount = fields.DecimalField(max_digits=40, decimal_places=0, default=0)
    collateral_token_amount = fields.DecimalField(
        max_digits=40, decimal_places=0, default=0
    )


class Event(str, Enum):
    CREATE_VAULT = "CREATE_VAULT"
    DEPOSIT_IN_VAULT = "DEPOSIT_IN_VAULT"
    WITHDRAW_FROM_VAULT = "WITHDRAW_FROM_VAULT"
    SETTLE_WITH_VAULT = "SETTLE_WITH_VAULT"
    MINT = "MINT"
    BURN = "BURN"
    BAILOUT = "BAILOUT"
    LIQUIDATE = "LIQUIDATE"


class Activity(Model):
    operation_hash = fields.CharField(51)
    vault = fields.ForeignKeyField("models.Vault", related_name="activities")
    event = fields.CharEnumField(Event)
    created = fields.DatetimeField(auto_now_add=True, use_tz=True, index=True)
    token_amount = fields.DecimalField(max_digits=40, decimal_places=0, default=0)
    collateral_token_amount = fields.DecimalField(
        max_digits=40, decimal_places=0, default=0
    )
    engine_contract_address = fields.CharField(58)


class TradeType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    INVEST = "INVEST"
    DIVEST = "DIVEST"


class Trade(Model):
    owner_address = fields.CharField(58, index=True)
    token_1_address = fields.CharField(58, null=True)
    token_2_address = fields.CharField(58, null=True)
    dex_contract_address = fields.CharField(58, index=True)
    symbol = fields.CharField(20, index=True, null=True)
    lp_token_total_supply = fields.DecimalField(
        max_digits=40, decimal_places=0, default=0
    )

    type = fields.CharEnumField(TradeType)

    token_1_amount = fields.DecimalField(max_digits=40, decimal_places=0, default=0)
    token_2_amount = fields.DecimalField(max_digits=40, decimal_places=0, default=0)

    token_1_pool = fields.DecimalField(max_digits=40, decimal_places=0, default=0)
    token_2_pool = fields.DecimalField(max_digits=40, decimal_places=0, default=0)

    price = fields.FloatField(default=0)
    created = fields.DatetimeField(auto_now_add=True, index=True)


@pre_save(Trade)
async def trade_pre_save(sender, instance: Trade, using_db, update_fields) -> None:
    last_trade = (
        await Trade.filter(dex_contract_address=instance.dex_contract_address)
        .order_by("-created")
        .first()
    )

    if last_trade:
        last_token_1_pool = last_trade.token_1_pool
        last_token_2_pool = last_trade.token_2_pool
    else:
        last_token_1_pool = 0
        last_token_2_pool = 0

    instance.token_1_amount = abs(last_token_1_pool - instance.token_1_pool)
    instance.token_2_amount = abs(last_token_2_pool - instance.token_2_pool)

    if instance.token_1_pool > Decimal(0):
        instance.price = instance.token_2_pool / instance.token_1_pool
    else:
        instance.price = Decimal(0.0)


class OraclePrice(Model):
    oracle_address = fields.CharField(58, index=True)
    value = fields.DecimalField(max_digits=40, decimal_places=0, default=0)
    created = fields.DatetimeField(auto_now_add=True, index=True)
    symbol = fields.CharField(15, index=True)


class Chat(Model):
    chat_id = fields.BigIntField(default=0)
    vaults = fields.ManyToManyField("models.Vault", related_name="chats")
    created = fields.DatetimeField(auto_now_add=True, index=True)
    log_level = fields.IntField(default=0)


class Transfer(Model):
    operation_hash = fields.CharField(51)
    sender = fields.CharField(58, index=True)
    receiver = fields.CharField(58, index=True)
    contract = fields.CharField(58, index=True)
    token_amount = fields.DecimalField(max_digits=40, decimal_places=0, default=0)
    token_id = fields.BigIntField(default=0, null=True)
    created = fields.DatetimeField(auto_now_add=True, use_tz=True, index=True)
