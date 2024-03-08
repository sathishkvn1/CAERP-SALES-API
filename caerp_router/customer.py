from fastapi import APIRouter ,Depends,Request,HTTPException,status,UploadFile,File,Response
from caerp_db.models import CustomerCompanyProfile, CustomerLog, CustomerNews, CustomerRegister
from caerp_schemas import ClientUserChangePasswordSchema, CompanyProfileSchemaForGet, CustomerCompanyProfileSchema, CustomerCompanyProfileSchemaResponse, CustomerInstallmentDetailsBase, CustomerInstallmentDetailsForGet, CustomerInstallmentMasterBase, CustomerLogSchema, CustomerLoginRequest, CustomerNewsBase, CustomerNewsBaseForGet, CustomerNewsResponse, CustomerRegisterBase, CustomerRegisterBaseForUpdate, CustomerRegisterListSchema, CustomerRegisterSchema, CustomerSalesQueryBase, CustomerSalesQueryForGet, EmailVerificationStatus, MobileVerificationStatus
from caerp_db.database import get_db
from caerp_db import db_customer
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from caerp_db import models
from caerp_db.hash import Hash
from caerp_auth import oauth2
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from typing import List,Optional, Union,Dict
from UserDefinedConstants.user_defined_constants import DeletedStatus,ActiveStatus,ParameterConstant
from datetime import date
from caerp_auth.authentication import authenticate_user
from sqlalchemy import func 

UPLOAD_DIR_COMPANYLOGO = "uploads/company_logo"
UPLOAD_DIR_CUSTOMER_NEWS = "uploads/customer_news"
router = APIRouter(
  
    tags=['CUSTOMER']
)

#---------------------------------------------------------------------------------------------------------------

@router.post('/add/customer', response_model=CustomerRegisterBase)
def create_customer(customer_data: CustomerRegisterBase, db: Session = Depends(get_db)):
    new_customer = db_customer.create_customer(db, customer_data)
    return new_customer

#---------------------------------------------------------------------------------------------------------------

@router.post('/update/customer/', response_model=CustomerRegisterBaseForUpdate)
def update_customer(
       
        customer_data: CustomerRegisterBaseForUpdate,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)):
    
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
   
    updated_customer = db_customer.update_customer(db, user_id, customer_data)

    return updated_customer

#---------------------------------------------------------------------------------------------------------------
@router.post('/change_password/{id}', response_model=CustomerRegisterBase)
def change_password(
        id: int,
        password_data: ClientUserChangePasswordSchema,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    user = db.query(CustomerRegister).filter(CustomerRegister.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Verify old password
    if not Hash.verify(user.password, password_data.old_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")

    # Hash the new password
    hashed_new_password = Hash.bcrypt(password_data.new_password)

    # Update the user's password
    user.password = hashed_new_password
    db.commit()
    db.refresh(user)

    return user
#---------------------------------------------------------------------------------------------------------------

@router.get("/get_all_customers/", response_model=CustomerRegisterListSchema)
async def get_all_customers(db: Session = Depends(get_db)):
    customer_details = db_customer.get_all_customers(db)
    return {"customers": customer_details}

#---------------------------------------------------------------------------------------------------------------


@router.get("/get_deleted_customers/" , response_model=List[CustomerRegisterSchema])
async def get_deleted_customers(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):
    return get_deleted_customers(db, deleted_status)



def get_deleted_customers(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(CustomerRegister).filter(CustomerRegister.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(CustomerRegister).filter(CustomerRegister.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(CustomerRegister).all()
    else:
       
        raise ValueError("Invalid deleted_status")
		    
#---------------------------------------------------------------------------------------------------------------





@router.get("/get_active_customers/", response_model=CustomerRegisterListSchema)
async def get_active_customers(
    active_status: ActiveStatus = ActiveStatus.ACTIVE,
    db: Session = Depends(get_db)
):
    customer_details = db_customer.get_active_customers(db, active_status)
    return {"customers": customer_details}


#---------------------------------------------------------------------------------------------------------------

@router.get("/get_customer_by_type/{id}", response_model=List[CustomerRegisterBase])
def get_customer_by_type(parameter: ParameterConstant,id: int, db: Session = Depends(get_db)):
    customer_details = db_customer.get_customer_by_state_id(db, parameter,id)
    if not customer_details:
        raise HTTPException(status_code=404, detail="No customers found for this id")
    return customer_details


#---------------------------------------------------------------------------------------------------------------
@router.get("/get_customer_by_expiring_date/{expiring_on}", response_model=List[CustomerRegisterBase])
def get_customer_by_expiring_date(expiring_on: date, db: Session = Depends(get_db)):
    customer_details = db_customer.get_customer_by_expiring_date(db, expiring_on)
    if not customer_details:
        raise HTTPException(status_code=404, detail="No customers found for this date")
    return customer_details
#---------------------------------------------------------------------------------------------------------------
@router.get("/get_customers_between_dates/", response_model=List[CustomerRegisterBase])
def get_customers_between_dates(start_date: date, end_date: date, db: Session = Depends(get_db)):
    customer_details = db_customer.get_customer_between_dates(db, start_date, end_date)
    if not customer_details:
        raise HTTPException(status_code=404, detail="No customers found between these dates")
    return customer_details
#---------------------------------------------------------------------------------------------------------------

@router.delete("/delete/customer/{customer_id}")
def delete_customer(
                     request: Request,
                     customer_id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)
                    ):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    return db_customer.delete_customer(db, customer_id,deleted_by=user_id)


#---------------------------------------------------------------------------------------------------------------

@router.post("/inactive/customer/{customer_id}")
def inactive_customer(
                     request: Request,
                     customer_id: int,
                     db: Session = Depends(get_db),
                    ):
    
    return db_customer.inactive_customer(db, customer_id)

#---------------------------------------------------------------------------------------------------------------
@router.post("/password/{customer_id}")
def reset_password(
                     request: Request,
                     customer_id: int,
                     password: str,
                     db: Session = Depends(get_db),
                     
                    ):
    
    return db_customer.reset_password(db, customer_id, password)

#---------------------------------------------------------------------------------------------------------------
@router.post("/update_type/{customer_id}")
def update_customer_type(
                     request: Request,
                     customer_id: int,
                     type: int,
                     db: Session = Depends(get_db),
                     
                    ):
    
    return db_customer.update_customer_type(db, customer_id, type)


#---------------------------------------------------------------------------------------------------------------



@router.post("/save_customer_company_profile/", response_model=CustomerCompanyProfileSchema)
def save_customer_company_profile(
    customer_profile_data: CustomerCompanyProfileSchema = Depends(),
    image_file: UploadFile = File(None),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    # Check authorization and validate token
    auth_info = authenticate_user(token)
    user_id = auth_info.get("user_id")
    
    try:
        
        user_count = db.query(func.count()).filter(CustomerCompanyProfile.customer_id == user_id).scalar()
        
        if user_count > 0:
            # If there are existing profiles, it's an update operation
            existing_customer = db.query(CustomerCompanyProfile).filter(CustomerCompanyProfile.customer_id == user_id).first()
            if existing_customer:
                # Update existing profile
                for key, value in customer_profile_data.dict(exclude_unset=True).items():
                    setattr(existing_customer, key, value)
                db.commit()
                db.refresh(existing_customer)
                saved_profile = existing_customer  # Assuming existing_customer is saved_profile
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer profile not found")
        else:
            # If there are no existing profiles, it's an insert operation
            new_customer = CustomerCompanyProfile(**customer_profile_data.dict())
            new_customer.customer_id = user_id  # Assign user_id from token
            db.add(new_customer)
            db.commit()
            db.refresh(new_customer)
            saved_profile = new_customer
        
        # If image provided, save it
        if image_file:
            file_content = image_file.file.read()
            file_path = f"{UPLOAD_DIR_COMPANYLOGO}/{saved_profile.id}.jpg"
            with open(file_path, "wb") as f:
                f.write(file_content)
        
        return saved_profile
        
    except Exception as e:
        error_detail = {
            "loc": ["server"],
            "msg": "Internal server error",
            "type": "internal_server_error"
        }
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

#---------------------------------------------------------------------------------------------------------------    
@router.get("/get_customer_by_customer_id/{id}", response_model=CustomerCompanyProfileSchemaResponse)
def get_customer_by_customer_id(id: int,
                        db: Session = Depends(get_db)):
    
    customer_detail = db_customer.get_customer_by_customer_id(db, id)
    if customer_detail is None:
        raise HTTPException(status_code=404, detail=f"Not found with ID {id}")
    return {"customer": [customer_detail]}

#---------------------------------------------------------------------------------------------------------------    

@router.get("/company_logo/{id}")
def get_company_logo(id: int, db: Session = Depends(get_db)):
    company_logo_content = db_customer.get_company_logo(db, id)
    if company_logo_content is None:
        raise HTTPException(status_code=404, detail="Company logo not found")
    
    # Return the logo image in the HTTP response
    return Response(content=company_logo_content, media_type="image/jpeg")

#---------------------------------------------------------------------------------------------------------------    



@router.post('/save_customer_news/{id}', response_model=CustomerNewsBase)
def save_customer_news(
    id: int = 0,
    data: CustomerNewsBase = Depends(),
    image_file: UploadFile = File(None),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    
    try:
        news = db_customer.save_customer_news(db, data, id, user_id)
        news_id = news.id

        if image_file:
            file_content = image_file.file.read()
            file_path = f"{UPLOAD_DIR_CUSTOMER_NEWS}/{news_id}.jpg"
            with open(file_path, "wb") as f:
                f.write(file_content)
        
        return news
    except HTTPException as e:
        raise e
    except SQLAlchemyError as e:
        error_message = f"Failed to save customer news: {e}"
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)

    
#---------------------------------------------------------------------------------------------------------------    


@router.delete("/delete/customer_news_details/{id}")
def delete_customer_news_details(
                     
                     id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    
    
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    return db_customer.delete_customer_news_details(db, id, deleted_by=user_id)


#---------------------------------------------------------------------------------------------------------------    .
@router.get("/get_all_customer_news_details/" , response_model=List[CustomerNewsBaseForGet])
async def get_all_customer_news_details(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):
    return get_all_customer_news_details(db, deleted_status)



def get_all_customer_news_details(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(CustomerNews).filter(CustomerNews.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(CustomerNews).filter(CustomerNews.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(CustomerNews).all()
    else:
       
        raise ValueError("Invalid deleted_status")
		    
#---------------------------------------------------------------------------------------------------------------    .      
@router.get("/get_customer_news_by_id/{id}", response_model=CustomerNewsResponse)
def get_customer_news_by_id(id: int,
                        db: Session = Depends(get_db)):
    
    detail = db_customer.get_customer_news_by_id(db, id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Not found with ID {id}")
    return {"news": [detail]}

#---------------------------------------------------------------------------------------------------------------    .      

@router.post("/save_customer_sales_queries", response_model=CustomerSalesQueryBase)
def save_customer_sales_query(
        query_data: CustomerSalesQueryBase,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    try:
        new_query = db_customer.save_customer_sales_query(db, query_data)
        return new_query
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    #---------------------------------------------------------------------------------------------------------------    .      
@router.get("/get_customer_sales_queries_by_id/{id}", response_model=CustomerSalesQueryForGet)
def get_customer_sales_queries_by_id(id: int,
                        db: Session = Depends(get_db)):
    
    role_detail = db_customer.get_customer_sales_queries_by_id(db, id)
    if role_detail is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"roles": [role_detail]}

#---------------------------------------------------------------------------------------------------------------    .      

@router.get("/get_all_customer_sales_queries", response_model=List[CustomerSalesQueryForGet])
def get_all_customer_sales_queries(db: Session = Depends(get_db)):
    
    queries = db_customer.get_all_customer_sales_queries(db)
    return queries

#---------------------------------------------------------------------------------------------------------------    .      

@router.post('/save_customer_installment_master/{id}', response_model=CustomerInstallmentMasterBase)
def save_customer_installment_master(
    id: int = 0,  # Default to 0 for add operation
    data: CustomerInstallmentMasterBase=Depends(),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):

    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    auth_info = authenticate_user(token) 
   
    
    try:
        new_data = db_customer.save_customer_installment_master(db, data, id)
        return new_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    


@router.get("/get_all_customer_installment_master_details", response_model=List[CustomerInstallmentMasterBase])
def get_all_customer_installment_master_details(db: Session = Depends(get_db)):
    
    countries = db_customer.get_all_customer_installment_master_details(db)
    return countries

@router.get("/get_customer_installment_master_details_by_id/{id}", response_model=CustomerInstallmentMasterBase)
def get_customer_installment_master_details_by_id(id: int,
                    db: Session = Depends(get_db)
                   ):
    state = db_customer.get_customer_installment_master_details_by_id(db, id)
    print("sate is",state)
    if not state:
        raise HTTPException(status_code=404, detail=f"No state found with ID {id}")
    return state


@router.post('/add/customer_installment_details', response_model=CustomerInstallmentDetailsBase)
def create_customer_installment_details(
    data: CustomerInstallmentDetailsBase=Depends(),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
   
    try:
        new_installment = db_customer.create_customer_installment_details(db, data)

        return new_installment
    except Exception as e:
        error_detail = {
            "loc": ["server"],
            "msg": f"Failed to create customer installment details: {str(e)}",
            "type": "internal_server_error"
        }
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=[error_detail])

@router.get("/get_customer_installment_details/{id}", response_model=CustomerInstallmentDetailsForGet)
def get_customer_installment_master_details_by_id(id: int, db: Session = Depends(get_db)):
    """  
    Retrieves customer installment details based on the provided ID.

    Parameters:
    - id (int): The unique identifier of the customer installment details to retrieve.

    Returns:
    - JSON: Returns the customer installment details corresponding to the provided ID if found.


    Raises:
    - HTTPException(404): Customer installment details not found if the provided ID does not exist in the database.
    """
    installment_details = db_customer.get_customer_installment_details(db, id)
   
    if not installment_details:
        raise HTTPException(status_code=404, detail=f"No state found with ID {id}")
    return installment_details



@router.get("/get_customer_installment_details/{customer_installment_master_id}", response_model=CustomerInstallmentDetailsForGet)
def get_customer_installment_master_details_by_customer_installment_master_id(customer_installment_master_id: int, db: Session = Depends(get_db)):
    """  
    Retrieves customer installment details based on the provided customer_installment_master_id.

    Parameters:
    - customer_installment_master_id (int): The unique identifier of the customer installment master to retrieve details for.

    Returns:
    - JSON: Returns the customer installment details corresponding to the provided customer_installment_master_id if found.
     
    Raises:
    - HTTPException(404): Customer installment details not found if the provided customer_installment_master_id does not exist in the database.
    """
    installment_details = db_customer.get_customer_installment_master_details_by_customer_installment_master_id(db, customer_installment_master_id)
   
    if not installment_details:
        raise HTTPException(status_code=404, detail=f"No state found with ID {customer_installment_master_id}")
    return installment_details 





    
@router.get("/is-mobile-verified/{mobile}", response_model=MobileVerificationStatus)
def is_mobile_verified(mobile: str, db: Session = Depends(get_db)):
    # Check if the mobile number exists in the database
    user = db_customer.get_user_by_mobile(db, mobile)
    if user:
        return {"mobile": mobile, "message": "Mobile number already exists.", "is_verified": True}
    else:
        return {"mobile": mobile, "message": "Mobile number does not exist.", "is_verified": False}



@router.get("/is-email-verified/{email}", response_model=EmailVerificationStatus)
def is_email_verified(email: str, db: Session = Depends(get_db)):
    # Check if the email exists in the database
    user = db_customer.get_user_by_email(db, email)
    if user:
        return {"email_id": email, "message": "Email already exists.", "is_verified": True}
    else:
        return {"email_id": email, "message": "Email does not exist.", "is_verified": False}
  
  
    
@router.get("/logged_in_client_user", response_model=CustomerRegisterListSchema)
def get_logged_in_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    """
    Retrieve details of the currently logged-in user.

    This endpoint requires a valid authentication token to be provided in the headers.

    Args:
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).
        token (str): Authentication token obtained during login.

    Returns:
        CustomerRegisterListSchema: Details of the logged-in user.

    Raises:
        HTTPException: If the token is missing or invalid, or if the user details are not found.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing"
        )

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]

    logged_in_user = db_customer.get_customer_user_by_id(db, user_id)

    if not logged_in_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User details not found"
        )

    # Convert the single CustomerRegister object into a list
    customer_list = [logged_in_user]
    return {"customers": customer_list}

@router.get("/get_customer_company_profile", response_model=List[CompanyProfileSchemaForGet])
def get_customer_company_profile(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    """
    Retrieve details of the company profile for the logged-in user.

    This endpoint requires a valid authentication token to be provided in the headers.

    Args:
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).
        token (str): Authentication token obtained during login.

    Returns:
        List[CompanyProfileSchema]: Details of the company profile.

    Raises:
        HTTPException: If the token is missing or invalid, or if the company profile details are not found.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing"
        )

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]

    company_profile = db_customer.get_customer_company_profile(db, user_id)

    # if not company_profile:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Company profile details not found"
    #     )

    return company_profile



@router.get("/get_customer_logs_by_user_id/", response_model=List[CustomerLogSchema])
def get_customer_logs_by_user_id(db: Session = Depends(get_db), token: str = Depends(oauth2.oauth2_scheme)):
    """
    Retrieve all customer log details for the currently logged-in user.

    Args:
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).
        token (str): Authentication token obtained during login.

    Returns:
        List[CustomerLogSchema]: List of customer log details for the currently logged-in user.

    Raises:
        HTTPException: If the token is missing or invalid, or if there are no customer logs for the user.
    """

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing"
        )
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]

    customer_logs = db.query(CustomerLog).filter(CustomerLog.user_id == user_id).all()
    if not customer_logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer logs not found for this user")

    customer_logs_schema = [CustomerLogSchema.from_orm(customer_log) for customer_log in customer_logs]

    return customer_logs_schema



@router.get("/get_all_customer_logs/", response_model=List[CustomerLogSchema])
def get_all_customer_logs(db: Session = Depends(get_db), token: str = Depends(oauth2.oauth2_scheme)):
    """
    Retrieve all customer log details from the database.

    Args:
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).
        token (str): Authentication token obtained during login.

    Returns:
        List[CustomerLogSchema]: List of customer log details.

    Raises:
        HTTPException: If the token is missing or invalid.
    """

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing"
        )

  
    # Query all admin logs
    customer_logs = db.query(CustomerLog).all()

    return customer_logs






