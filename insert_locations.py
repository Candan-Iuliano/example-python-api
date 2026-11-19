import json
from app.database import SessionLocal
from app.models import Location
from sqlalchemy import select
from app.logging_config import get_logger

logger = get_logger()


def validate_location(locations: list[dict]) -> list[dict]: 
    output = []
    for location in locations:
        try:
            if "name" not in location:
                raise KeyError("Name is missing")
            if not isinstance(location["name"], str) or not location["name"].strip():
                raise ValueError("Name must be a nonempty string")
            if "latitude" not in location:
                raise KeyError("Latitude is missing")
            if "longitude" not in location:
                raise KeyError("Longitude is missing")
            if not isinstance(location["latitude"], (int, float)) or isinstance(location["latitude"], bool):
                raise TypeError("Latitude must be a number")
            if not isinstance(location["longitude"], (int, float)) or isinstance(location["longitude"], bool):
                raise TypeError("Longitude must be a number")
            if not -90 <= location["latitude"] <= 90:
                raise ValueError("Latitude values are outside -90 - 90 bounds")
            if not -180 <= location["longitude"] <= 180:
                raise ValueError("Longitude values are outside -180 - 180 bounds")
            output.append(location)
        except (KeyError, TypeError, ValueError) as e:
            logger.warning("Invalid location skipped",extra={"event": "location_validation_failed", "reason": str(e)} )
            continue
    return output

def filter_new_locations(locations: list[dict], session)-> list[dict]:
    output = []
    query = select(Location.name)
    result = session.execute(query) #executes the query and retrieves the data
    check = set(result.scalars().all())
    for location in locations:
        if location["name"] not in check:
            output.append(location)
            check.add(location["name"])
    return output

def ingest_location(file_path: str):
    session = SessionLocal()
    logger.info("Location ingestion started")
    try:
        with open(file_path, "r") as file:
            locations = json.load(file)
            valid_locals = validate_location(locations)
            unique_locals = filter_new_locations(valid_locals, session)
            for location in unique_locals:
                dblocation = Location(**location)
                session.add(dblocation)
                logger.info("added location", extra={"event": "location_addded", "location_name": location["name"]} )
            session.commit()
            logger.info("ingestion completed, added %s locations", len(unique_locals))
    finally:
        session.close()

ingest_location("./data/locations.json")
#"./data/locations.json"