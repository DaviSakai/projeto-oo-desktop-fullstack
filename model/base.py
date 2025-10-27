from datetime import datetime
from pydantic import BaseModel

class WithId(BaseModel):
    id: int | None = None

class TimeStamped(BaseModel):
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()
