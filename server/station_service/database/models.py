from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Station(Base):
    __tablename__ = "stations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, index=True, nullable=False)
    longtitude: Mapped[float] = mapped_column(Float, index=True, nullable=False)
    connection_type: Mapped[str] = mapped_column(String, index=True, nullable=False)
    power_kw: Mapped[int] = mapped_column(Integer, nullable=False)