# generated by datamodel-codegen:
#   filename:  fulfill.json

from __future__ import annotations

from pydantic import BaseModel, Extra


class FulfillParameter(BaseModel):
    class Config:
        extra = Extra.forbid

    script: str
    payload: str
