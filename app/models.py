from sqlalchemy import Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class Location(Base):
    __tablename__ = "locations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    description: Mapped[str |None] = mapped_column(String, nullable=True)
    #dunder method: executres when using a print method on the object, unpacks it and runs the code on it. dev mode version
    def __repr__(self):
        return f"Location(name={self.name}, latitude={self.latitude}, longitude={self.longitude})"

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    origin_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    origin: Mapped[Location] = relationship(
        Location,
        foreign_keys=[origin_id]
    )
    dest_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    destination: Mapped[Location] = relationship(
        Location,
        foreign_keys=[dest_id]
    )
    # description: Mapped[str |None] = mapped_column(String, nullable=True)
    analysis_type: Mapped[str] = mapped_column(String)
    result: Mapped[dict] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc)
)
  