from sqlalchemy import create_engine, Column, String, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/land_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class PlotDocument(Base):
    __tablename__ = "plot_documents"

    id = Column(UUID(as_uuid=True), primary_key=True)
    plot_id = Column(UUID(as_uuid=True), ForeignKey("plots.id"), nullable=False)
    document_type = Column(String(50), nullable=False)
    document_name = Column(String(255), nullable=False)
    file_url = Column(String, nullable=False)
    file_size = Column(Numeric)
    mime_type = Column(String(100))
    created_at = Column(TIMESTAMP(timezone=True))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
