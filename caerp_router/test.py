

from fastapi import APIRouter, Depends, HTTPException
from caerp_db.models import CountryDB, Designation
from sqlalchemy.orm import Session
from caerp_auth import oauth2
from caerp_db.database import get_db
from caerp_schemas import CAPTCHARequest, CompanyMasterBase, CountryCreate
from typing import List

from caerp_db.models import CountryDB, Designation,Voucher,Master,Detail1,Detail2
import random



router = APIRouter(
   
    tags=["TEST API"]
)



@router.get("/country", response_model=List[CountryCreate])
def get_all_countries(token: str = Depends(oauth2.oauth2_scheme),
                      db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    countries = db.query(CountryDB).all()
    
    return countries





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


def generate_captcha():
    # Generate two random numbers between 1 and 100
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    
    # Generate a random operation (+ or -)
    operation = random.choice(['+', '-'])
    
    # Perform the operation
    if operation == '+':
        result = num1 + num2
    else:
        result = num1 - num2
    
    # Display the expression to the user
    captcha = f"What is {num1} {operation} {num2}?"
    return captcha, result

# Generate CAPTCHA once
captcha, expected_result = generate_captcha()
# print("CAPTCHA:", captcha)
# print("Expected Result:", expected_result)

@router.post("/verify_captcha/")
async def verify_captcha(captcha_request: CAPTCHARequest):
    # Validate user's input against expected result
    user_answer = captcha_request.answer
    if user_answer == expected_result:
        return {"success": True, "message": "CAPTCHA is correct!"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect CAPTCHA answer!")