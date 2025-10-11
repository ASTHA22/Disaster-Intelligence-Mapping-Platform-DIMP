"""
Database configuration with PostgreSQL + PostGIS
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
import os
from datetime import datetime

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://dimp_user:dimp_password@localhost:5432/dimp")

# Create engine
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class DisasterZone(Base):
    __tablename__ = "disaster_zones"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    severity = Column(String)
    damage_score = Column(Float)
    affected_area_km2 = Column(Float)
    location = Column(Geometry('POINT', srid=4326))
    lat = Column(Float)
    lon = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column(JSON)

class FloodArea(Base):
    __tablename__ = "flood_areas"
    
    id = Column(String, primary_key=True, index=True)
    area_name = Column(String)
    water_level_meters = Column(Float)
    affected_area_km2 = Column(Float)
    location = Column(Geometry('POINT', srid=4326))
    lat = Column(Float)
    lon = Column(Float)
    severity = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)

class Infrastructure(Base):
    __tablename__ = "infrastructure"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    status = Column(String)
    location = Column(Geometry('POINT', srid=4326))
    lat = Column(Float)
    lon = Column(Float)
    damage_level = Column(String)
    last_updated = Column(DateTime, default=datetime.utcnow)

class PopulationDisplacement(Base):
    __tablename__ = "population_displacement"
    
    id = Column(String, primary_key=True, index=True)
    area_name = Column(String)
    displaced_count = Column(Integer)
    location = Column(Geometry('POINT', srid=4326))
    lat = Column(Float)
    lon = Column(Float)
    shelter_capacity = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    severity = Column(String)
    description = Column(String)
    location = Column(Geometry('POINT', srid=4326))
    lat = Column(Float)
    lon = Column(Float)
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SocialMediaPost(Base):
    __tablename__ = "social_media_posts"
    
    id = Column(String, primary_key=True, index=True)
    text = Column(String)
    urgency = Column(String)
    priority_score = Column(Float)
    location_name = Column(String)
    location = Column(Geometry('POINT', srid=4326), nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    verified = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    analysis_json = Column(JSON)

class FeedbackLog(Base):
    """Continuous learning feedback"""
    __tablename__ = "feedback_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entity_type = Column(String)  # 'zone', 'alert', 'social_post'
    entity_id = Column(String)
    feedback_type = Column(String)  # 'accuracy', 'false_positive', 'severity_correction'
    original_value = Column(String)
    corrected_value = Column(String)
    user_id = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column(JSON)

# Database initialization
def init_db():
    """Initialize database with PostGIS extension"""
    from sqlalchemy import text
    
    # Create PostGIS extension
    with engine.connect() as conn:
        try:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
            conn.commit()
        except Exception as e:
            print(f"PostGIS extension already exists or error: {e}")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized with PostGIS!")

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
