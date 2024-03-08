from fastapi import APIRouter, Depends, Query
from caerp_db.models import Test
from caerp_schemas import TestSchema


from sqlalchemy.orm import Session
from caerp_db.database import get_db

from typing import List



router = APIRouter(
    prefix="/testendpoint",
    tags=["testendpoint"]
)

@router.get("/example")
async def example(db: Session = Depends(get_db)):
    # Use the database session (db) to perform database operations
    # For example, you can execute queries or perform CRUD operations here
    # Example:
    # result = db.query(...)
    return {"message": "Endpoint using the database session"}


@router.get("/test_values/{db_name}")
async def get_test_values(db_name: str, db: Session = Depends(get_db)):
    print(db_name)
    test_values = db.query(Test).all()
    
    # Convert the SQLAlchemy objects to dictionaries for JSON serialization
    test_values_dicts = [{"id": test.id, "name": test.name} for test in test_values]
    
    # Return the values as a JSON response
    return {"test_values": test_values_dicts}



# @router.get("/get_data/{db_name}")
# async def get_data(db_name: str, session: Session = Depends(get_db)):
#     try:
#         # Define a select query using the Test model
#         query = session.query(Test).all()

#         # Fetch the data
#         data = [{"id": item.id, "name": item.name} for item in query]

#         return {"data": data}
#     except Exception as e:
#         return {"error": str(e)}
    
    


