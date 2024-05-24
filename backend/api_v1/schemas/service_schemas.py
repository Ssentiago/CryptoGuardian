from pydantic import BaseModel, Field


class PasswordSettings(BaseModel):
    length: int = Field(ge=8)
    include_lower: bool | None = None
    include_upper: bool | None = None
    include_digits: bool | None = None
    include_symbols: bool | None = None

    def model_post_init(self, *args):
        if any(
            [
                self.include_lower,
                self.include_upper,
                self.include_digits,
                self.include_symbols,
            ]
        ):
            return True
        raise ValueError


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
