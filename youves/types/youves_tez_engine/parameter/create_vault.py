# generated by datamodel-codegen:
#   filename:  create_vault.json

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra


class CreateVaultParameter(BaseModel):
    class Config:
        extra = Extra.forbid

    baker: Optional[str]
    contract_address_callback: str
