# generated by datamodel-codegen:
#   filename:  tokenToToken.json

from __future__ import annotations

from pydantic import BaseModel, Extra


class TokenToTokenParameter(BaseModel):
    class Config:
        extra = Extra.forbid

    outputDexterContract: str
    minTokensBought: str
    to: str
    tokensSold: str
    deadline: str