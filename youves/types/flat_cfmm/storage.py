# generated by datamodel-codegen:
#   filename:  storage.json

from __future__ import annotations

from pydantic import BaseModel, Extra


class FeeRatio(BaseModel):
    class Config:
        extra = Extra.forbid

    denominator: str
    numerator: str


class FlatCfmmStorage(BaseModel):
    class Config:
        extra = Extra.forbid

    admin: str
    cashAddress: str
    cashMultiplier: str
    cashPool: str
    feeRatio: FeeRatio
    lqtAddress: str
    lqtTotal: str
    pendingPoolUpdates: str
    proposedAdmin: str
    rewardRecipient: str
    tokenAddress: str
    tokenId: str
    tokenMultiplier: str
    tokenPool: str
