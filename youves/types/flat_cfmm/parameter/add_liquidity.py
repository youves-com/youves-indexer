# generated by datamodel-codegen:
#   filename:  addLiquidity.json

from __future__ import annotations

from pydantic import BaseModel, Extra


class AddLiquidityParameter(BaseModel):
    class Config:
        extra = Extra.forbid

    owner: str
    minLqtMinted: str
    maxTokensDeposited: str
    cashDeposited: str
    deadline: str
