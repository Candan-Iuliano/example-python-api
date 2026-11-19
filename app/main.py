from fastapi import FastAPI, HTTPException
from app.database import SessionLocal
from app.models import Location, AnalysisResult
from sqlalchemy import select
from app.schemas import LocationResponse, AnalysisResultResponse
from sqlalchemy.orm import joinedload

app = FastAPI()

@app.get("/health")
def health_check():
    return {"message":"running"}

@app.get("/locations", response_model=list[LocationResponse])
def get_locations():
    session = SessionLocal()
    try:  
        query = select(Location)
        results = session.execute(query).scalars().all()

        return results
    finally:
        session.close()

@app.get("/locations/{id}", response_model=LocationResponse)
def get_locations(id:int):
    session = SessionLocal()
    try:  
        query = select(Location).where(Location.id == id)
        results = session.execute(query).scalars().first()
        if results is None:
            raise HTTPException(status_code=404,detail="id not found")
        return results
    finally:
        session.close()

@app.get("/analysis", response_model=list[AnalysisResultResponse])
def get_locations():
    session = SessionLocal()
    try:  
        query = select(AnalysisResult).options(
            joinedload(AnalysisResult.origin),
            joinedload(AnalysisResult.destination)
        )
        results = session.execute(query).scalars().all()
        return results
    finally:
        session.close()


@app.get("/analysis/{id}", response_model=AnalysisResultResponse)
def get_locations(id:int):
    session = SessionLocal()
    try:  
        query = select(AnalysisResult).options(
            joinedload(AnalysisResult.origin),
            joinedload(AnalysisResult.destination)
        ).where(AnalysisResult.id == id)
        results = session.execute(query).scalars().first()
        if results is None:
            raise HTTPException(status_code=404,detail="id not found")
        return results
    finally:
        session.close()