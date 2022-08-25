# generated by datamodel-codegen:
#   filename:  storage.json

from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, Extra


class Intents(BaseModel):
    class Config:
        extra = Extra.forbid

    start_timestamp: str
    token_amount: str


class YouvesFa2IntentsStorage(BaseModel):
    class Config:
        extra = Extra.forbid

    collateral_token_address: str
    collateral_token_id: str
    engine_address: str
    intents: Dict[str, Intents]
    sender: str
    target_price: str
    target_price_oracle: str
    token_address: str
    token_id: str