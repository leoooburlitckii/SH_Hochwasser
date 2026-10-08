from settings import settings
from sqlalchemy import create_engine, String, Float, Integer, BigInteger, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

engine = create_engine(settings.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Messung(Base):
    __tablename__= "messungen"

    station_uuid: Mapped[str] = mapped_column(String, primary_key=True)
    station_name: Mapped[str] = mapped_column(String, nullable=False)
    wasserstand: Mapped[int] = mapped_column(Integer, nullable=False)
    zeitstempel: Mapped[str] = mapped_column(String, nullable=False)
    mnw: Mapped[float | None] = mapped_column(Float, nullable=True)
    mhw: Mapped[float | None] = mapped_column(Float, nullable=True)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    station_name: Mapped[str] = mapped_column(String, nullable=False)
    schwellenwert: Mapped[str] = mapped_column(String, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("PostgreSQL: Таблицы успешно созданы.")

def save_measurment(
    station_uuid: str,
    station_name: str,
    wasserstand: int,
    zeitstempel: str,
    mnw: float | None = None,
    mhw: float | None = None,
):
    with SessionLocal() as session:
        messung = Messung(
            station_uuid=station_uuid,
            station_name=station_name,
            wasserstand=wasserstand,
            zeitstempel=zeitstempel,
            mnw=mnw,
            mhw=mhw,
        )
        
        session.merge(messung)
        session.commit()

    print(f"Gespeichert {station_name} mit {station_uuid}-> {wasserstand}cm {zeitstempel}, {mnw} cm und {mhw} cm")


def get_latest_measurment(station_uuid: str):
    
    with SessionLocal() as session:
        stmt = select(Messung).where(Messung.station_uuid == station_uuid)
        result = session.scalar(stmt)

        if result:
            return{
                "name": result.station_name,
                "wert": result.wasserstand,
                "zeit": result.zeitstempel,
                "mnw": result.mnw if result.mnw is not None else "--",
                "mhw": result.mhw if result.mhw is not None else "--",
            }

        return {
        "name": "Unbekannt",
        "wert": "--",
        "zeit": "--",
        "mnw": "--",
        "mhw": "--",
    }