from app.database import SessionLocal
from app.models import Location
from sqlalchemy import select

with SessionLocal() as session:

    location = Location(name="Detroit", latitude=42.3601, longitude=-71.0589)

    # session.add(location)
    # session.commit()

    #query = select(Location).where(Location.name == "Boston", Location.latitude > 40).order_by(Location.latitude.asc()).limit(3) # sets the scheam for query
    query = select(Location).where(Location.name == "Detroit")
    result = session.execute(query) #executes the query and retrieves the data
    # output = result.scalars().all() #extracts values from rows and retrieves them as a list
    output = result.scalars().first()
    if output is not None:
        # output.latitude = 42.3602
        session.delete(output)
        #session.add(output)
        session.commit()
    print(output)