from typing import Optional

from pydantic import BaseModel


class Meta(BaseModel):
    total: int
    limit: Optional[int]
    offset: Optional[int]
    sort: Optional[str]
    order: Optional[str]
