from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from caerp_db.models import CustomerCompanyProfile, CustomerPracticingAs,CustomerAreaOfPracticing,CustomerProfessionalQualification, CustomerInstallmentDetails, CustomerInstallmentMaster, CustomerNews, CustomerPasswordReset, CustomerRegister, CustomerSalesQuery, OtpGeneration, SmsTemplates
from caerp_schemas import CustomerCompanyProfileSchema,CompleteCustomerQualificationSchema, CustomerInstallmentDetailsBase, CustomerInstallmentMasterBase, CustomerNewsBase, CustomerRegisterBase, CustomerRegisterBaseForUpdate, CustomerSalesQueryBase
from caerp_db.hash import Hash
from caerp_db.database import get_db
from typing import List,Optional, Union,Dict
from UserDefinedConstants.user_defined_constants import DeletedStatus,ActiveStatus,ParameterConstant,RecordActionType
# from caerp_schemas import 
from datetime import date,datetime
from sqlalchemy import func,text
from sqlalchemy.exc import SQLAlchemyError
import send_message,send_email
import random
from caerp_schemas import  Email
from datetime import date,datetime,timedelta
from caerp_auth import oauth2

import  os

from settings import WEB_BASE_URL
UPLOAD_DIR_COMPANYLOGO = "uploads/company_logo"





#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
# def create_customer(db: Session, customer_data: CustomerRegisterBase):
#     customer_data_dict = customer_data.dict()
#     customer_data_dict["created_on"] = datetime.utcnow()
#     customer_data_dict["password"] = Hash.bcrypt(customer_data_dict["password"])
#     new_customer = CustomerRegister(**customer_data_dict)
    
#     db.add(new_customer)
#     db.commit()
#     db.refresh(new_customer)
#     customer_id= new_customer.id
#     #--- otp for mobile verification --------
#     # mobile_otp_data= db_send_email.generate_otp(5)  # Generate OTP data
#     # mobile_otp_value = mobile_otp_data["random_value"]
#     mobile_otp_value = random.randint(pow(10,5), pow(10,5+1)-1)  
#     new_otp = create_otp(db, mobile_otp_value,customer_id)
#     mobile_otp_id = new_otp.id    
#     message= f"{mobile_otp_value}is your SECRET One Time Password (OTP) for your mobile registration. Please use this password to complete your transaction. From:BRQ GLOB TECH"
#     temp_id= 1607100000000128308
    
#     try:
#         send_message.send_sms_otp(new_customer.mobile_number,message,temp_id,db)
#     #  db_send_sms.send_sms(new_customer.mobile_number,message,temp_id)
#     except Exception as e:
#         # Handle sms sending failure
#         print(f"Failed to send message: {str(e)}")
#     #-------------------------------------------
#     #------otp for email verification ---------------
#     # otp_data= db_send_email.generate_otp(5)  # Generate OTP data
#     # otp_value = otp_data["random_value"]  
#     otp_value = random.randint(pow(10,5), pow(10,5+1)-1)
#     new_email_otp = create_otp(db, otp_value,customer_id)
#     email_otp_id = new_email_otp.id
#     email = Email(
#         messageTo = new_customer.email_id,
#         subject=  "Email verification",
#         messageBody = f"{otp_value} , is one time password for compleating your registration",
#         messageType= "NO_REPLY"
#     )
    
#     try:
#         send_email.send_email(email, db)
#     except Exception as e:
#         # Handle email sending failure
#         # For example, log the error and inform the user that email verification failed
#         print(f"Failed to send email: {str(e)}")


def create_customer(db: Session, customer_data: CustomerRegisterBase):
    customer_data_dict = customer_data.dict()
    customer_data_dict["created_on"] = datetime.utcnow()
    customer_data_dict["password"] = Hash.bcrypt(customer_data_dict["password"])
    new_customer = CustomerRegister(**customer_data_dict)
    
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    customer_id= new_customer.id
    #--- otp for mobile verification --------
    # mobile_otp_data= db_send_email.generate_otp(5)  # Generate OTP data
    # mobile_otp_value = mobile_otp_data["random_value"]
    mobile_otp_value = random.randint(pow(10,5), pow(10,5+1)-1)  
    new_otp = create_otp(db, mobile_otp_value,customer_id)
    mobile_otp_id = new_otp.id    
    # message= f"{mobile_otp_value}is your SECRET One Time Password (OTP) for your mobile registration. Please use this password to complete your transaction. From:BRQ GLOB TECH"
    # temp_id= 1607100000000128308
    sms_type= 'OTP'
    print('SMS Type : ', sms_type)
    template_data = get_templates_by_type(db,sms_type)
    print('template ID : ',template_data)
    temp_id= template_data.template_id
    template_message = template_data.message_template
    replace_values = [ mobile_otp_value, 'mobile registration']
    placeholder = "{#var#}"
    for value in replace_values:
        template_message = template_message.replace(placeholder, str(value),1)
            
    try:
        send_message.send_sms_otp(new_customer.mobile_number,template_message,temp_id,db)
    #  db_send_sms.send_sms(new_customer.mobile_number,message,temp_id)
    except Exception as e:
        # Handle sms sending failure
        print(f"Failed to send message: {str(e)}")
    #-------------------------------------------
    #------otp for email verification ---------------
    # otp_data= db_send_email.generate_otp(5)  # Generate OTP data
    # otp_value = otp_data["random_value"]  
    otp_value = random.randint(pow(10,5), pow(10,5+1)-1)
    new_email_otp = create_otp(db, otp_value,customer_id)
    email_otp_id = new_email_otp.id
    email = Email(
        messageTo = new_customer.email_id,
        subject=  "Email verification",
        messageBody = f"{otp_value} , is one time password for compleating your registration",
        messageType= "NO_REPLY"
    )
    
    try:
        send_email.send_email(email, db)
    except Exception as e:
        # Handle email sending failure
        # For example, log the error and inform the user that email verification failed
        print(f"Failed to send email: {str(e)}")

    #---------------------------------------------

    data={
                    "mobile_otp_id": mobile_otp_id,
                    'email_otp_id': email_otp_id  ,
                    'user_id'     : customer_id
                }
    access_token = oauth2.create_access_token(data=data)
   
    return {'access_token': access_token,
                'token_type': 'bearer'
                }
   
    #------------------------------------------------------------------------------------------

    data={
                    "mobile_otp_id": mobile_otp_id,
                    'email_otp_id': email_otp_id  ,
                    'user_id'     : customer_id
                }
    access_token = oauth2.create_access_token(data=data)
   
    return {'access_token': access_token,
                'token_type': 'bearer'
                }
   




#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
def get_otp_by_id(db: Session,otp_id:str):
    return db.query(OtpGeneration).filter(OtpGeneration.id == otp_id).first()


def create_otp(db: Session, otp_value: str, user_id: int):
    current_time = datetime.utcnow()

    # Calculate OTP expiry time (30 minutes from current time)
    expiry_time = current_time + timedelta(minutes=30)

    # Create a new instance of OtpGeneration
    new_otp = OtpGeneration(
        otp=otp_value,
        created_on=current_time,
        created_by=user_id,
        otp_expire_on=expiry_time,
    )
    print("new otp", new_otp)
    # Add the new OTP to the database session
    db.add(new_otp)
    # Commit the changes to the database
    db.commit()
    # Refresh the new OTP object to reflect any changes made during the commit
    db.refresh(new_otp)

    # Return the newly created OTP object
    return new_otp


def get_templates_by_type(db: Session, type: str):
    return db.query(SmsTemplates).filter(SmsTemplates.sms_type == type).first()


#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------

def update_customer(db: Session, user_id: int, customer_data: CustomerRegisterBaseForUpdate):
    customer = db.query(CustomerRegister).filter(CustomerRegister.id == user_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    customer_data_dict = customer_data.dict(exclude_unset=True)

    for key, value in customer_data_dict.items():
        setattr(customer, key, value)
    


    db.commit()
    db.refresh(customer)
    return customer
        






def get_all_customers(db: Session):
    return db.query(CustomerRegister).all()




# def get_all_customers(db: Session, filter_condition: Optional[dict] = None):
#     query = db.query(CustomerRegister)
#     if filter_condition:
#         query = query.filter_by(**filter_condition)
#     return query.all()


def get_deleted_customers(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(CustomerRegister).filter(CustomerRegister.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(CustomerRegister).filter(CustomerRegister.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(CustomerRegister).all()
    else:
        # Handle invalid state or raise an error
        raise ValueError("Invalid deleted_status")




def get_active_customers(db: Session, active_status: ActiveStatus):
    if active_status == ActiveStatus.ACTIVE:
        return db.query(CustomerRegister).filter(CustomerRegister.is_active == 'yes').all()
    elif active_status == ActiveStatus.NOT_ACTIVE:
        return db.query(CustomerRegister).filter(CustomerRegister.is_active == 'no').all()
    elif active_status == ActiveStatus.ALL:
        return db.query(CustomerRegister).all()
    else:
        raise ValueError("Invalid active_status")
    
    
    




def get_customer_by_state_id(db: Session,parameter: str,id: int):
        
        return db.query(CustomerRegister).filter(getattr(CustomerRegister, parameter)== id).all()

def get_customer_by_expiring_date(db: Session,expiring_on: date):
        
        return db.query(CustomerRegister).filter(func.DATE(CustomerRegister.expiring_on) == expiring_on).all()

def get_customer_between_dates(db: Session, start_date: date, end_date: date):
    return db.query(CustomerRegister).filter(CustomerRegister.created_on.between(start_date, end_date)).all()



    
    
def add_customer(db: Session, request: CustomerRegisterBase):
    customer_data = request.dict()
    
    
    new_customer= CustomerRegister(**customer_data)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

def save_customer(db: Session, customer_data: CustomerRegisterBase):
    # Hash the password before saving
    hashed_password = Hash.bcrypt(customer_data.password)
    customer_data_dict = customer_data.dict(exclude={"password"})  # Exclude password from dictionary
    customer_data_dict["password"] = hashed_password
    customer_data_dict["created_on"] = datetime.utcnow()
    new_customer = CustomerRegister(**customer_data_dict)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer






# def save_customer(db: Session, customer_data: CustomerRegisterSchema, customer_id: int):

#     if customer_id == 0:
#         # Add operation
#         customer_data_dict = customer_data.dict()
#         customer_data_dict["created_on"] = datetime.utcnow()
#         new_customer = CustomerRegister(**customer_data_dict)
#         db.add(new_customer)
#         db.commit()
#         db.refresh(new_customer)
#         return new_customer
#     else:
#         # Update operation
#         customer = db.query(CustomerRegister).filter(CustomerRegister.id == customer_id).first()
#         if customer is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
#         customer_data_dict = customer_data.dict(exclude_unset=True)
#         for key, value in customer_data_dict.items():
#             setattr(customer, key, value)
        
#         db.commit()
#         db.refresh(customer)
#         return customer



def delete_customer(db: Session, customer_id: int,deleted_by: int):
    existing_customer = db.query(CustomerRegister).filter(CustomerRegister.id == customer_id).first()

    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    existing_customer.is_deleted = 'yes'
    existing_customer.deleted_by = deleted_by
    existing_customer.deleted_on = datetime.utcnow()
   
    db.commit()

    return {
        "message": "Customer marked as deleted successfully",

    }


def inactive_customer(db: Session, customer_id: int):
    existing_customer = db.query(CustomerRegister).filter(CustomerRegister.id == customer_id).first()

    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    existing_customer.is_active = 'no'
   
    db.commit()

    return {
        "message": "Customer marked as inactive successfully",

    }
    
def reset_password(db: Session, customer_id: int, password: str):
    hashed_password =Hash.bcrypt(password)
    existing_customer = db.query(CustomerRegister).filter(CustomerRegister.id == customer_id).first()

    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    existing_customer.password = hashed_password
   
    try:
        db.commit()  # Commit changes to the database
    except Exception as e:
        db.rollback()  # Rollback changes if an error occurs
        raise HTTPException(status_code=500, detail=f"Failed to reset password: {str(e)}")


    return {
        "message": "Password reset successful",

    }



def update_customer_type(db: Session, customer_id: int, type: int):
    
    existing_customer = db.query(CustomerRegister).filter(CustomerRegister.id == customer_id).first()

    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    existing_customer.customer_type_id = type
   
    try:
        db.commit()  # Commit changes to the database
    except Exception as e:
        db.rollback()  # Rollback changes if an error occurs
        raise HTTPException(status_code=500, detail=f"Failed to reset password: {str(e)}")


    return {
        "message": "Password reset successful",

    }
    
    






def get_customer_by_customer_id(db: Session, id: int):
    return db.query(CustomerCompanyProfile).filter(CustomerCompanyProfile.customer_id== id).first()



def get_company_logo(db: Session, company_id: int):
    # Construct the file path for the company logo
    logo_path = os.path.join(UPLOAD_DIR_COMPANYLOGO, f"{company_id}.jpg")
    
    # Check if the file exists
    if not os.path.exists(logo_path):
        return None
    
    # Read the content of the file
    with open(logo_path, "rb") as f:
        logo_content = f.read()
    
    return logo_content



# def save_customer_news(db: Session, data: CustomerNewsBase, id: int, user_id: int):
#     try:
#         if id == 0:
#             # Add operation
#             news_data_dict = data.dict()
#             news_data_dict["created_by"] = user_id
#             new_news = CustomerNews(**news_data_dict)
#             db.add(new_news)
#             db.commit()
#             db.refresh(new_news)
#             return new_news
#         else:
#             # Update operation
#             existing_news = db.query(CustomerNews).filter(CustomerNews.id == id).first()
#             if existing_news is None:
#                 raise HTTPException(status_code=404, detail="News not found")
            
#             update_data = data.dict(exclude_unset=True)
#             for key, value in update_data.items():
#                 setattr(existing_news, key, value)
#             existing_news.modified_by = user_id
#             existing_news.modified_on = datetime.utcnow()

#             db.commit()
#             db.refresh(existing_news)

#             return existing_news
#     except Exception as e:
#         error_message = f"Failed to save customer news: {e}"
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)

def save_customer_news(db: Session, data: CustomerNewsBase, id: int, user_id: int):
    try:
        if id == 0:
            # Add operation
            news_data_dict = data.dict()
            news_data_dict["created_by"] = user_id
            new_news = CustomerNews(**news_data_dict)
            db.add(new_news)
            db.commit()
            db.refresh(new_news)
            return new_news
        else:
            # Update operation
            existing_news = db.query(CustomerNews).filter(CustomerNews.id == id).first()
            if existing_news is None:
                raise HTTPException(status_code=404, detail="News not found")
            
            update_data = data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(existing_news, key, value)
            existing_news.modified_by = user_id
            existing_news.modified_on = datetime.utcnow()

            db.commit()
            db.refresh(existing_news)

            return existing_news
    except SQLAlchemyError as e:
        error_message = f"Failed to save customer news: {e}"
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)



def delete_customer_news_details(db: Session, id: int, deleted_by: int):
    result = db.query(CustomerNews).filter(CustomerNews.id == id).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Director not found")

    result.is_deleted = 'yes'
    result.deleted_by = deleted_by
    result.deleted_on = datetime.utcnow()

    db.commit()

    return {
        "message": "Deleted successfully",
    }



def get_customer_news_by_id(db: Session, id: int):
    return db.query(CustomerNews).filter(CustomerNews.id == id).first()


def save_customer_sales_query(db: Session, query_data: CustomerSalesQueryBase):
    query_data_dict = query_data.dict()
    new_query = CustomerSalesQuery(**query_data_dict) 
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return new_query



def get_customer_sales_queries_by_id(db: Session, id: int):
    return db.query(CustomerSalesQuery).filter(CustomerSalesQuery.id == id).first()


def get_all_customer_sales_queries(db: Session):
    return db.query(CustomerSalesQuery).all()


def save_customer_installment_master(db: Session, data: CustomerInstallmentMasterBase, id: int):

    try:
        if id == 0:
            # Add operation
            customer_installment_data_dict = data.dict()
           
            new_data = CustomerInstallmentMaster(**customer_installment_data_dict)
            db.add(new_data)
            db.commit()
            db.refresh(new_data)
            return new_data
        else:
            # Update operation
            existing_data = db.query(CustomerInstallmentMaster).filter(CustomerInstallmentMaster.id == id).first()
            if existing_data is None:
                raise HTTPException(status_code=404, detail="Not found")
            
            installment_data_dict = data.dict(exclude_unset=True)
            for key, value in installment_data_dict.items():
                setattr(existing_data, key, value)
           

            db.commit()
            db.refresh(existing_data)

            return existing_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

def get_customer_by_id(db: Session,id: int):
        
        return db.query(CustomerRegister).filter(CustomerRegister.id== id).first() 
    

def get_all_customer_installment_master_details(db: Session):
    return db.query(CustomerInstallmentMaster).all()



def get_customer_installment_master_details_by_id(db: Session,id: int):
    return db.query(CustomerInstallmentMaster).filter(CustomerInstallmentMaster.id == id).first()


def create_customer_installment_details(db: Session, data: CustomerInstallmentDetailsBase):
    data_dict = data.dict()

    new_installment = CustomerInstallmentDetails(**data_dict) 
    db.add(new_installment)
    db.commit()
    db.refresh(new_installment)
    return new_installment


def get_customer_installment_details(db: Session,id: int):
    return db.query(CustomerInstallmentDetails).filter(CustomerInstallmentDetails.id == id).first()


def get_customer_installment_master_details_by_customer_installment_master_id(db: Session,id: int):
    return db.query(CustomerInstallmentDetails).filter(CustomerInstallmentDetails.customer_installment_master_id == id).first()

def get_user_by_mobile(db: Session, mobile: str):
    return db.query(CustomerRegister).filter(CustomerRegister.mobile_number == mobile).first()

def get_user_by_email(db: Session, email: str):
    return db.query(CustomerRegister).filter(CustomerRegister.email_id == email).first()

def get_customer_user_by_id(db: Session, user_id: int):
    return db.query(CustomerRegister).filter(CustomerRegister.id == user_id).first()

def get_customer_company_profile(db: Session, user_id: int):
    return db.query(CustomerCompanyProfile).filter(CustomerCompanyProfile.customer_id == user_id).all()


#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------

def save_customer_password_reset_request(db: Session, customer_id:int, email: str,customer_name: str):
   
    current_time = datetime.utcnow() 
    expiry_time = current_time + timedelta(minutes=5)
    data={
                    'expiry_time': expiry_time.strftime("%Y-%m-%d %H:%M:%S") , # Format time as string,                   
                    'user_id'     : customer_id
                }
    access_token = oauth2.create_access_token(data=data)
    new_data=CustomerPasswordReset(
        customer_id=customer_id,
        request_token=access_token,
        request_timestamp=current_time
        
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    # return new_data
    response_data = {
        "id": new_data.id,
        "customer_id": new_data.customer_id,
        "request_token": new_data.request_token,
        # "request_timestamp": new_data.request_timestamp.strftime("%Y-%m-%d %H:%M:%S")  # Convert datetime to string
    } 
    print(access_token)
    template_content = read_template('email-verification.html')
    dynamic_content = {"verificationUrl": f'{WEB_BASE_URL}/reset_password/?token={access_token}',
                        "Name": f'{customer_name}'} 
    email_body = render_template(template_content, dynamic_content)
    email = Email(
        messageTo=email,
        subject='Reset Password Link',
        messageBody=email_body,
        messageType="NO_REPLY"
    )
    
    try:
        send_email.send_email(email, db)
        return {"Value":"Success","Message":"Password reset link has been sent to your mail"}
    except Exception as e:
        # Handle email sending failure
        # For example, log the error and inform the user that email verification failed
        return {"Value": "Error", "Message": f"Failed to send password reset link. Error: {str(e)}. Please try again later."}





# Read email template from file
def read_template(template_name):
    template_dir = "templates"
    template_filename = os.path.join(template_dir, template_name)
    with open(template_filename, "r") as template_file:
        template_content = template_file.read()
    return template_content

# Replace placeholders with dynamic content
def render_template(template_content, dynamic_content):
    # Replace placeholders in the template with dynamic content
    for key, value in dynamic_content.items():
        template_content = template_content.replace("{{" + key + "}}", str(value))
    return template_content




def customer_password_reset(db: Session, customer_id: int, password: str,  time_expire: datetime):
    print("Searching for password reset link in the database with expiry time:", time_expire)
    
    time_expire_datetime = datetime.strptime(time_expire, '%Y-%m-%d %H:%M:%S')

# Add timedelta to the datetime object
    time_expire_updated = time_expire_datetime - timedelta(minutes=5)
    existing_link = db.query(CustomerPasswordReset).filter(CustomerPasswordReset.request_timestamp == time_expire_updated).first()
    
    if existing_link is None:
        print("Password reset link not found or expired.")
        raise HTTPException(status_code=404, detail="Link Has Expired")

    print("Password reset link found.")

    hashed_password = Hash.bcrypt(password)
    existing_customer = db.query(CustomerRegister).filter(CustomerRegister.id == customer_id).first()

    if existing_customer is None:
        print("Customer not found in the database.")
        raise HTTPException(status_code=404, detail="Customer not found")

    print("Customer found. Resetting password...")

    existing_customer.password = hashed_password

    try:
        db.commit()  # Commit changes to the database
        print("Password reset successful.")
    except Exception as e:
        db.rollback()  # Rollback changes if an error occurs
        print("Failed to reset password:", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to reset password: {str(e)}")

    return {
        "message": "Password reset successful",
    }


def get_customer_by_email(db: Session,email: str):
        
        return db.query(CustomerRegister).filter(CustomerRegister.email_id== email).first() 


def get_customer_practicing_info(db: Session, customer_id: int,parameter = ParameterConstant):
    if parameter == 'QUALIFICATION':
        qualification_data = db.query(CustomerProfessionalQualification).filter(
        CustomerProfessionalQualification.customer_id==customer_id,
        CustomerProfessionalQualification.is_deleted=='no'
        ).all()
        # return qualification
        result = {
            "customer_id": customer_id,
            "qualifications": [
                {
                    "id"     : qualification.id,
                    "profession_type_id": qualification.profession_type_id,
                    "membership_number" : qualification.membership_number,
                    "enrollment_date"   : qualification.enrollment_date,
                    "is_deleted"        : qualification.is_deleted
                } for qualification in qualification_data
            ]
        }
        return result
    if parameter == 'PRACTICING_AS':
        practicing_as = db.query(CustomerPracticingAs).filter(
        CustomerPracticingAs.customer_id==customer_id,
        CustomerPracticingAs.is_deleted=='no').all()
        # return practicing_as
        result = {
            "customer_id": customer_id,
            "practicing_as": [
                {
                    "id": practicing.id,
                    "practicing_type_id": practicing.practicing_type_id,
                    "other": practicing.other,
                    "is_deleted": practicing.is_deleted
                } for practicing in practicing_as
            ]
        }
        return result
    if parameter == 'AREA_OF_PRACTICING_AS':
        area_of_practicing = db.query(CustomerAreaOfPracticing).filter(
        CustomerAreaOfPracticing.customer_id==customer_id,
        CustomerAreaOfPracticing.is_deleted=='no')

        result = {
            "customer_id": customer_id,
            "areas_of_practicing": [
                {
                    "id": aop.id,
                    "area_of_practicing_id": aop.area_of_practicing_id,
                    "other": aop.other,
                    "is_deleted": aop.is_deleted
                } for aop in area_of_practicing
            ]
        }
        return result




def save_customer_practicing_info(
    db: Session,
    qualification_data: CompleteCustomerQualificationSchema,
    # id: Optional[int] = None
):
    qualification_data_dict = qualification_data.dict(exclude_unset=True)
    
    # Remove nested fields from main data dictionary
    customer_id = qualification_data_dict['customer_id']
    qualifications  = qualification_data_dict.pop('qualifications',[])
    practicing_as_data = qualification_data_dict.pop('practicing_as', [])
    area_of_practicing_data = qualification_data_dict.pop('area_of_practicing', [])
    # print("qualification data----", qualifications)
    
    # Insert main qualification data
    if qualifications:
        update_query = text(
            "UPDATE customer_professional_qualification SET is_deleted='yes' "                        
            "WHERE customer_id = :customer_id"
        )
        db.execute(update_query, {'customer_id': customer_id})
        new_qualification = None
        for qual_data in qualifications:
            existing_data = db.query(CustomerProfessionalQualification).filter(
                CustomerProfessionalQualification.customer_id == customer_id,
                CustomerProfessionalQualification.profession_type_id == qual_data['profession_type_id']
            ).first()
            # print(existing_data.statement.compile(compile_kwargs={"literal_binds": True}))
            print("existing data --------------------",existing_data)
            if existing_data:
                qualification_data_dict["modified_on"] = datetime.utcnow()
                qualification_data_dict["is_deleted"] = 'no'
                qualification_data_dict["customer_id"]= customer_id
                print("DATA ------------------: ", qualification_data_dict["customer_id"])
                for key, value in qualification_data_dict.items():
                    setattr(existing_data, key, value)
            else:
                new_qualification = CustomerProfessionalQualification(
                    customer_id=customer_id,
                    **qual_data
                )
                new_qualification.created_on = datetime.utcnow()
                db.add(new_qualification)
        
        db.commit()
        if new_qualification:
            db.refresh(new_qualification)
            # return new_qualification
        
        # return {"message": "Success", "success": True}
    
    # Insert practicing_as data
    if practicing_as_data:
        update_query = text(
            "UPDATE customer_practicing_as SET is_deleted='yes' "                        
            "WHERE customer_id = :customer_id"
        )
        db.execute(update_query, {'customer_id': customer_id})
        
        for practicing_as in practicing_as_data:
            existing_data = db.query(CustomerPracticingAs).filter(
                CustomerPracticingAs.customer_id == customer_id,
                CustomerPracticingAs.practicing_type_id == practicing_as['practicing_type_id']
            ).first()
            if existing_data:
                practicing_as["modified_on"] = datetime.utcnow()
                practicing_as["is_deleted"] = 'no'
                for key, value in practicing_as.items():
                    setattr(existing_data, key, value)
            else:
                practicing_as_record = CustomerPracticingAs(
                    customer_id=customer_id,
                    **practicing_as
                )
                practicing_as_record.created_on = datetime.utcnow()
                db.add(practicing_as_record)
        
        db.commit()
        # return {"message": "Success", "success": True}

    # Insert area_of_practicing data
    if area_of_practicing_data:
        update_query = text(
            "UPDATE customer_area_of_practicing SET is_deleted='yes' "                        
            "WHERE customer_id = :customer_id"
        )
        db.execute(update_query, {'customer_id': customer_id})
        
        for area_of_practicing in area_of_practicing_data:
            existing_data = db.query(CustomerAreaOfPracticing).filter(
                CustomerAreaOfPracticing.customer_id == customer_id,
                CustomerAreaOfPracticing.area_of_practicing_id == area_of_practicing['area_of_practicing_id']
            ).first()
            if existing_data:
                area_of_practicing["modified_on"] = datetime.utcnow()
                area_of_practicing["is_deleted"] = 'no'
                for key, value in area_of_practicing.items():
                    setattr(existing_data, key, value)
            else:
                area_of_practicing_record = CustomerAreaOfPracticing(
                    customer_id=customer_id,
                    **area_of_practicing
                )
                area_of_practicing_record.created_on = datetime.utcnow()
                db.add(area_of_practicing_record)
        
        db.commit()
    return {"message": "Success", "success": True}
