from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database setup (SQLite for simplicity)
SQLALCHEMY_DATABASE_URL = "sqlite:///./pothole.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define database model
class PotholeDB(Base):
    __tablename__ = "potholes"
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    severity = Column(Integer, default=1)  # 1=Low, 2=Medium, 3=High
    reported_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Pydantic model for request data
class PotholeReport(BaseModel):
    latitude: float
    longitude: float
    severity: int = 1

# API Endpoints
@app.post("/report")
async def report_pothole(report: PotholeReport):
    db = SessionLocal()
    db_pothole = PotholeDB(
        latitude=report.latitude,
        longitude=report.longitude,
        severity=report.severity
    )
    db.add(db_pothole)
    db.commit()
    db.refresh(db_pothole)
    return {"status": "success", "id": db_pothole.id}

@app.get("/potholes")
async def get_potholes():
    db = SessionLocal()
    potholes = db.query(PotholeDB).all()
    return potholes