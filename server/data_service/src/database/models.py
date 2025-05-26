from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    battery_capacity: Mapped[str] = mapped_column(String, nullable=False)
    consumpting: Mapped[str] = mapped_column(String, nullable=False)
    type_charger: Mapped[str] = mapped_column(String, nullable=False)