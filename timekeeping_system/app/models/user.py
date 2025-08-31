from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[str]
    username: str
    email: str
    hashed_password: str
