from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    zone = Column(String(100))

    objects = relationship("Object", back_populates="event")


class Object(Base):
    __tablename__ = "object"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("event.id"))

    uuid = Column(String(100))
    type = Column(String(50))
    x = Column(Float)
    y = Column(Float)
    speed_ms = Column(Float)

    event = relationship("Event", back_populates="objects")
