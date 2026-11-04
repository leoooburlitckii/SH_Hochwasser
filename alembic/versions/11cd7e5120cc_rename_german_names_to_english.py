"""rename german names to english

Revision ID: 11cd7e5120cc
Revises: 406495eca07d
Create Date: 2026-11-04 23:12:18.585618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11cd7e5120cc'
down_revision: Union[str, Sequence[str], None] = '406495eca07d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Benennt deutsche Tabellen-, Spalten- und Constraint-Namen auf Englisch um (Daten bleiben erhalten)."""
    # Tabellen
    op.rename_table("stationen", "stations")
    op.rename_table("messungen", "measurements")

    # Spalten
    op.alter_column("stations", "mnw", new_column_name="mean_low_water")
    op.alter_column("stations", "mhw", new_column_name="mean_high_water")
    op.alter_column("measurements", "wasserstand", new_column_name="water_level")
    op.alter_column("measurements", "zeitstempel", new_column_name="timestamp")
    op.alter_column("users", "schwellenwert", new_column_name="threshold")

    # Constraints, Indizes und Sequenzen (PostgreSQL benennt sie nicht automatisch mit der Tabelle um)
    op.execute("ALTER TABLE measurements RENAME CONSTRAINT uq_station_zeit TO uq_station_timestamp")
    op.execute("ALTER TABLE stations RENAME CONSTRAINT stationen_pkey TO stations_pkey")
    op.execute("ALTER TABLE measurements RENAME CONSTRAINT messungen_pkey TO measurements_pkey")
    op.execute("ALTER TABLE measurements RENAME CONSTRAINT messungen_station_uuid_fkey TO measurements_station_uuid_fkey")
    op.execute("ALTER SEQUENCE messungen_id_seq RENAME TO measurements_id_seq")


def downgrade() -> None:
    """Stellt die alten deutschen Namen wieder her."""
    op.execute("ALTER SEQUENCE measurements_id_seq RENAME TO messungen_id_seq")
    op.execute("ALTER TABLE measurements RENAME CONSTRAINT measurements_station_uuid_fkey TO messungen_station_uuid_fkey")
    op.execute("ALTER TABLE measurements RENAME CONSTRAINT measurements_pkey TO messungen_pkey")
    op.execute("ALTER TABLE stations RENAME CONSTRAINT stations_pkey TO stationen_pkey")
    op.execute("ALTER TABLE measurements RENAME CONSTRAINT uq_station_timestamp TO uq_station_zeit")

    op.alter_column("users", "threshold", new_column_name="schwellenwert")
    op.alter_column("measurements", "timestamp", new_column_name="zeitstempel")
    op.alter_column("measurements", "water_level", new_column_name="wasserstand")
    op.alter_column("stations", "mean_high_water", new_column_name="mhw")
    op.alter_column("stations", "mean_low_water", new_column_name="mnw")

    op.rename_table("measurements", "messungen")
    op.rename_table("stations", "stationen")
