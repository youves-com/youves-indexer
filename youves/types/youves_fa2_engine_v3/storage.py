# generated by datamodel-codegen:
#   filename:  storage.json

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra


class Key(BaseModel):
    class Config:
        extra = Extra.forbid

    owner: str
    token_id: str


class Administrator(BaseModel):
    class Config:
        extra = Extra.forbid

    key: Key
    value: Dict[str, Any]


class CollateralRatio(BaseModel):
    class Config:
        extra = Extra.forbid

    numerator: str
    denominator: str


class IntroducerRatio(BaseModel):
    class Config:
        extra = Extra.forbid

    numerator: str
    denominator: str


class LiquidationPayoutRatio(BaseModel):
    class Config:
        extra = Extra.forbid

    numerator: str
    denominator: str


class MintingFeeRatio(BaseModel):
    class Config:
        extra = Extra.forbid

    numerator: str
    denominator: str


class SettlementPayoutRatio(BaseModel):
    class Config:
        extra = Extra.forbid

    numerator: str
    denominator: str


class SettlementRatio(BaseModel):
    class Config:
        extra = Extra.forbid

    numerator: str
    denominator: str


class SettlementRewardFeeRatio(BaseModel):
    class Config:
        extra = Extra.forbid

    numerator: str
    denominator: str


class VaultContexts(BaseModel):
    class Config:
        extra = Extra.forbid

    balance: str
    introducer: Optional[str]
    minted: str


class YouvesFa2EngineV3Storage(BaseModel):
    class Config:
        extra = Extra.forbid

    accrual_update_timestamp: str
    administrators: List[Administrator]
    collateral_ratio: CollateralRatio
    collateral_token_contract: str
    collateral_token_id: str
    compound_interest_rate: str
    governance_token_contract: str
    interest_rate_setter_contract: str
    introducer_ratio: IntroducerRatio
    liquidation_payout_ratio: LiquidationPayoutRatio
    minting_fee_ratio: MintingFeeRatio
    options_contract: str
    reference_interest_rate: str
    reward_pool_contract: str
    savings_pool_contract: str
    settlement_payout_ratio: SettlementPayoutRatio
    settlement_ratio: SettlementRatio
    settlement_reward_fee_ratio: SettlementRewardFeeRatio
    spread_rate: str
    target_price_oracle: str
    token_contract: str
    token_id: str
    total_supply: str
    vault_contexts: Dict[str, VaultContexts]
