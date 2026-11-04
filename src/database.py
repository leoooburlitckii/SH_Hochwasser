from settings import settings
from sqlalchemy import create_engine, String, Float, Integer, BigInteger, Boolean, select, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import insert  #ist so spezifisch weil jede Datenbank anders mit Duplikaten umgeht

engine = create_engine(settings.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

class Station(Base):
    __tablename__ = "stations"

    uuid: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    mean_low_water: Mapped[float | None] = mapped_column(Float, nullable=True)   # Mittleres Niedrigwasser (MNW)
    mean_high_water: Mapped[float | None] = mapped_column(Float, nullable=True)  # Mittleres Hochwasser (MHW)

    col: Mapped[int] = mapped_column(Integer, nullable=False)
    row: Mapped[int] = mapped_column(Integer, nullable=False)

    is_hotspot: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    measurements: Mapped[list["Measurement"]] = relationship(back_populates="station")  # Anführungszeichen hier sind forward reference

class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    station_uuid: Mapped[str] = mapped_column(ForeignKey("stations.uuid"), primary_key=False)
    water_level: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    station: Mapped["Station"] = relationship(back_populates="measurements")

    __table_args__ = (
        UniqueConstraint("station_uuid", "timestamp", name="uq_station_timestamp"),  # uq = Unique Constraint, Komma muss vorkommen damit es als Tuple erkannt wird
    )

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    station_name: Mapped[str] = mapped_column(String, nullable=False)
    threshold: Mapped[str] = mapped_column(String, nullable=False)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_station(
    uuid: str,
    name: str,
    mean_low_water: float | None,
    mean_high_water: float | None,
    col: int,
    row: int,
    is_hotspot: bool
):
    with SessionLocal() as session:
        station = Station(
            uuid = uuid,
            name = name,
            mean_low_water = mean_low_water,
            mean_high_water = mean_high_water,
            col = col,
            row = row,
            is_hotspot = is_hotspot
        )
        session.merge(station)
        session.commit()
    print(f"Gespeichert {name} mit uuid:{uuid}, mnw {mean_low_water}, mhw {mean_high_water}, col {col}, row {row}, hotspot {is_hotspot}")

def save_measurement(
    station_uuid: str,
    station_name: str,
    water_level: int,
    timestamp: datetime,
):
    with SessionLocal() as session:
        stmt = insert(Measurement).values(
            station_uuid=station_uuid,
            water_level = water_level,
            timestamp = timestamp
        )

        stmt = stmt.on_conflict_do_nothing(
            constraint = "uq_station_timestamp"
        )

        session.execute(stmt)
        session.commit()

    print(f"Gespeichert {station_name} mit {station_uuid}-> {water_level}cm {timestamp}")

def save_measurements_batch(station_uuid: str, measurements: list) -> int:
    rows = []
    for m in measurements:
        rows.append({
            "station_uuid": station_uuid,
            "water_level": int(m["value"]),
            "timestamp": m["timestamp"]
        })

    # PostgreSQL driver allows max 65535 parameters per query.
    # Each row uses 3 parameters, so we insert in chunks of 5000 rows.
    chunk_size = 5000

    with SessionLocal() as session:
        for start in range(0, len(rows), chunk_size):
            chunk = rows[start:start + chunk_size]
            stmt = insert(Measurement).values(chunk)
            stmt = stmt.on_conflict_do_nothing(
                constraint = "uq_station_timestamp"
            )
            session.execute(stmt)
        session.commit()

    return len(rows)

def get_latest_measurement(station_uuid: str):

    with SessionLocal() as session:
        stmt = select(Measurement).where(Measurement.station_uuid == station_uuid).order_by(Measurement.timestamp.desc())
        result = session.scalar(stmt)

        if result:
            return{
                "name": result.station.name,
                "value": result.water_level,
                "timestamp": result.timestamp,
                "mean_low_water": result.station.mean_low_water if result.station.mean_low_water is not None else "--",
                "mean_high_water": result.station.mean_high_water if result.station.mean_high_water is not None else "--",
            }

        return {
        "name": "Unbekannt",
        "value": "--",
        "timestamp": "--",
        "mean_low_water": "--",
        "mean_high_water": "--",
    }

def get_all_stations() -> list["Station"]:
    with SessionLocal() as session:
        stmt = select(Station)
        return session.scalars(stmt).all()

def get_hotspots() -> list["Station"]:
    with SessionLocal() as session:
        stmt = select(Station).where(Station.is_hotspot == True)
        return session.scalars(stmt).all()
