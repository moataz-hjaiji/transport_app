from datetime import datetime
from pydantic import BaseModel

class TokenData(BaseModel):
    username: str
    scopes: list[str] = []  
    exp: datetime | None = None  