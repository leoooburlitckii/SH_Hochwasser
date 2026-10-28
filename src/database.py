from settings import settings
from sqlalchemy import create_engine, String, Float, Integer, BigInteger, Boolean, select, ForeignKey, UniqueConstraint, DateTime 
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert #ist so spezifisch weil jede Datenbank anders mit Duplikaten umgeht

engine = create_engine(settings.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

class Station(Base):
    __tablename__ = "stationen"

    uuid: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    mnw: Mapped[float | None] = mapped_column(Float, nullable=True)
    mhw: Mapped[float | None] = mapped_column(Float, nullable=True)

    col: Mapped[int] = mapped_column(Integer, nullable=False)
    row: Mapped[int] = mapped_column(Integer, nullable=False)

    is_hotspot: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    messungen: Mapped[list["Messung"]] = relationship(back_populates="station") # Anführungszeichnen hier sind forward reference

class Messung(Base):
    __tablename__= "messungen"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    station_uuid: Mapped[str] = mapped_column(ForeignKey("stationen.uuid"))
    wasserstand: Mapped[int] = mapped_column(Integer, nullable=False)
    zeitstempel: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,)
    
    station: Mapped["Station"] = relationship(back_populates="messungen")

    __table_args__ = (
        UniqueConstraint("station_uuid", "zeitstempel", name="uq_station_zeit"), #uq = Unique Contraint , komma muss vorkommen damit als Tuple erkennt
    )

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    station_name: Mapped[str] = mapped_column(String, nullable=False)
    schwellenwert: Mapped[str] = mapped_column(String, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_station(
    uuid: str,
    name: str,
    mnw: float| None,
    mhw: float| None,
    col: int,
    row: int,
    is_hotspot: bool
):
    with SessionLocal() as session:
        station = Station(
            uuid = uuid,
            name = name,
            mnw = mnw,
            mhw = mhw,
            col = col,
            row = row,
            is_hotspot = is_hotspot
        )
        session.merge(station)
        session.commit()
    print(f"Gespeichert {name} mit uuid:{uuid}, mnw {mnw}, mhw {mhw}, col {col}, row {row}, hotspot {is_hotspot}")
    
def save_measurment(
    station_uuid: str,
    station_name: str,
    wasserstand: int,
    zeitstempel: datetime,
):
    with SessionLocal() as session:
        stmt = insert(Messung).values(
            station_uuid=station_uuid,
            wasserstand = wasserstand,
            zeitstempel = zeitstempel
        )

        stmt = stmt.on_conflict_do_nothing(
            constraint = "uq_station_zeit"
        )
        
        session.execute(stmt)
        session.commit()

    print(f"Gespeichert {station_name} mit {station_uuid}-> {wasserstand}cm {zeitstempel}")

def get_latest_measurment(station_uuid: str):
    
    with SessionLocal() as session:
        stmt = select(Messung).where(Messung.station_uuid == station_uuid).order_by(Messung.zeitstempel.desc())
        result = session.scalar(stmt)

        if result:
            return{
                "name": result.station.name,
                "wert": result.wasserstand,
                "zeit": result.zeitstempel,
                "mnw": result.station.mnw if result.station.mnw is not None else "--",
                "mhw": result.station.mhw if result.station.mhw is not None else "--",
            }

        return {
        "name": "Unbekannt",
        "wert": "--",
        "zeit": "--",
        "mnw": "--",
        "mhw": "--",
    }

def get_all_stations() -> list["Station"]:
    with SessionLocal() as session:
        stmt = select(Station)
        return session.scalars(stmt).all()

def get_hotspots() -> list["Station"]:
    with SessionLocal() as session:
        stmt = select(Station).where(Station.is_hotspot == True)
        return session.scalars(stmt).all()

def get_measurments_for_graphs(station_uuid: str, start: datetime, to: datetime) -> tuple[list[datetime], list[int]]:
    with SessionLocal() as session:
        stmt = (
            select(Messung).
            where(Messung.station_uuid== station_uuid).
            where(Messung.zeitstempel >= start).
            where(Messung.zeitstempel <=to).
            order_by(Messung.zeitstempel.asc())
        )
        
        messungen = session.scalars(stmt).all()

        if not messungen:
            fallback_stmt = (
                select(Messung).
                where(Messung.station_uuid== station_uuid).
                where(Messung.zeitstempel <start).
                order_by(Messung.zeitstempel.desc()).
                limit(1)
            )

            fallback = session.scalar(fallback_stmt)

            if fallback:
                messungen = [fallback]
            else:
                return ([], [] )


    x_axis = []
    y_axis = []
    
    for messung in messungen:
        x_axis.append(messung.zeitstempel)
        y_axis.append(messung.wasserstand)

    return (x_axis, y_axis)


