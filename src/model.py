import os
from sqlalchemy import create_engine, String, Float, Integer, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

DB_URL = os.getenv("DB_URL", "sqlite:///./bird_species.db")

# Adjust SQLite-specific settings if necessary
connect_args = {}
if DB_URL.startswith("sqlite"):
    connect_args.update({"check_same_thread": False})

# Create the engine and session maker
engine = create_engine(
    DB_URL, connect_args=connect_args, pool_recycle=3600
)
create_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for the ORM models
class Base(DeclarativeBase):
    pass

# Define the `audio_analysis` table
class AudioAnalysis(Base):
    __tablename__ = "audio_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    iot_id: Mapped[str] = mapped_column(String, nullable=False)
    analysis_date: Mapped[Date] = mapped_column(Date, nullable=False)

    # Relationship to link to species_counts
    species_counts = relationship("SpeciesCounts", back_populates="audio_analysis")

# Define the `species_counts` table
class SpeciesCounts(Base):
    __tablename__ = "species_counts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    audio_id: Mapped[int] = mapped_column(Integer, ForeignKey("audio_analysis.id"), nullable=False)
    species_name: Mapped[str] = mapped_column(String, nullable=False)
    analysis_date: Mapped[Date] = mapped_column(Date, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationship back to audio_analysis
    audio_analysis = relationship("AudioAnalysis", back_populates="species_counts")

# Create the tables in the database
Base.metadata.create_all(bind=engine)