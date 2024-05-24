from pydantic import BaseModel, ConfigDict


class CredentialBase(BaseModel):
    model_config = ConfigDict(strict=True)
    service: str
    username: str


class CredentialCreate(CredentialBase):
    user_id: int | None = None
    password: str


class CredentialDelete(CredentialBase):
    user_id: int | None = None


class Credential(CredentialBase):
    id: int
