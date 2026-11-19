from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:Starwars88@localhost:5432/geospatial_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

