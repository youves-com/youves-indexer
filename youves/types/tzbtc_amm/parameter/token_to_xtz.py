# generated by datamodel-codegen:
#   filename:  tokenToXtz.json

from __future__ import annotations

from pydantic import BaseModel, Extra


class TokenToXtzParameter(BaseModel):
    class Config:
        extra = Extra.forbid

    to: str
    tokensSold: str
    minXtzBought: str
    deadline: str
