from dataclasses import dataclass
from typing import  Optional

@dataclass
class MessageData:
    id: int
    title: Optional[str]
    size : int
