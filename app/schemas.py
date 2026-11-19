from pydantic import BaseModel,ConfigDict
from datetime import datetime

class LocationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    latitude:float
    longitude: float
    description: str | None = None


class AnalysisResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    origin: LocationResponse
    destination: LocationResponse
    analysis_type: str
    result: dict
    created_at: datetime

  