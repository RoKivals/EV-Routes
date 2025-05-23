from sqlalchemy import String, Integer, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    favorite_routes: Mapped[list[int]] = mapped_column(JSON, default=list)
    favorite_stations: Mapped[list[int]] = mapped_column(JSON, default=list)