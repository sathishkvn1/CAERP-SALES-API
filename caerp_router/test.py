

from fastapi import APIRouter, Depends, HTTPException
from caerp_db.models import CountryDB, Designation
from sqlalchemy.orm import Session
from caerp_auth import oauth2
from caerp_db.database import get_db
from caerp_schemas import CompanyMasterBase, CountryCreate
from typing import List

from caerp_db.models import CountryDB, Designation,Voucher,Master,Detail1,Detail2




router = APIRouter(
    prefix="/test",
    tags=["TEST API"]
)



@router.get("/country", response_model=List[CountryCreate])
def get_all_countries(token: str = Depends(oauth2.oauth2_scheme),
                      db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    countries = db.query(CountryDB).all()
    
    return countries

# @router.get("/data/")
# async def get_data(deleted_state: dele = DeletedSatus.not_deleted,db: Session = Depends(get_db)):
#     data = get_designations_by_deleted_state(db, deleted_state)
#     return {"data": data}


# def get_designations_by_deleted_state(db: Session, deleted_state: YesNoEnum):
#     if deleted_state == YesNoEnum.deleted:
#         return db.query(Designation).filter(Designation.is_deleted == 'yes').all()
#     elif deleted_state == YesNoEnum.not_deleted:
#         return db.query(Designation).filter(Designation.is_deleted == 'no').all()
#     elif deleted_state == YesNoEnum.All:
#         return db.query(Designation).all()
#     else:
#         # Handle invalid state or raise an error
#         raise ValueError("Invalid deleted_state")



def get_next_voucher_id(db: Session):
    voucher = db.query(Voucher).order_by(Voucher.id.desc()).first()
    if voucher:
        next_voucher_id = voucher.voucher_id + 1
    else:
        next_voucher_id = 1
    new_voucher = Voucher(voucher_id=next_voucher_id)
    db.add(new_voucher)
    db.commit()
    return next_voucher_id


@router.post('/insert_voucher_to_all')
def insert_voucher_to_all(db: Session = Depends(get_db)):
    try:
        # Get the next voucher ID
        next_voucher_id = get_next_voucher_id(db)

        # Create entries for Master, Detail1, and Detail2 tables with the next voucher_id
        master_entry = Master(voucher_id=next_voucher_id)
        db.add(master_entry)
        
        detail1_entry = Detail1(voucher_id=next_voucher_id)
        db.add(detail1_entry)
        
        detail2_entry = Detail2(voucher_id=next_voucher_id)
        db.add(detail2_entry)
        
        # Commit the transaction
        db.commit()
        
        return {'message': 'Data inserted successfully to all tables'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

