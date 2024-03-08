from fastapi import APIRouter, HTTPException, status,Header
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from caerp_schemas import CustomerLoginRequest, LoginRequest
from sqlalchemy.orm import Session
from caerp_db.database import get_db
from caerp_db import models
from caerp_db.hash import Hash
from caerp_auth import oauth2
# from .oauth2 import create_access_token, get_current_user,oauth2_scheme,SECRET_KEY, ALGORITHM
from .oauth2 import create_access_token,SECRET_KEY, ALGORITHM
from starlette.requests import Request
from sqlalchemy import update
from datetime import datetime
from typing import Dict, Any,Union
from jose import JWTError, jwt
import user_agent
from datetime import datetime
from caerp_auth.oauth2 import oauth2_scheme,custom_oauth2_scheme_client

from sqlalchemy import text
from sqlalchemy.sql import text
router = APIRouter(
    tags=['Authentication']
)






@router.post('/customer-login')
def get_client_login(request_data: CustomerLoginRequest = Depends(), db: Session = Depends(get_db)):
    try:
        customer = db.query(models.CustomerRegister).filter(models.CustomerRegister.email_id == request_data.email).first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
        
        hashed_password_from_db = customer.password
        plain_text_password_from_request = request_data.password

        if not Hash.verify(hashed_password_from_db, plain_text_password_from_request):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid password')

        # Provide the necessary data for creating the access token
        data = {'user_id': customer.id}  # You may need to adjust this depending on your user model
        
        access_token = oauth2.create_access_token(data)  # Pass the data to create_access_token()

        return {'access_token': access_token, 'token_type': 'bearer'}

    except Exception as e:
        print("Exception occurred:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error')




from fastapi import APIRouter, Depends, HTTPException, Header, Request, status


import geoip2.database
import geoip2.errors
from caerp_db.database import get_db
from caerp_db import models
from caerp_db.hash import Hash
from caerp_auth import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from user_agents import parse

from starlette.requests import Request
from fastapi import Header
import geoip2.database
import os

# Path to the GeoLite2-City.mmdb file
GEOIP_DATABASE_PATH = "C:\\fapi_8001\\geoip_database\\GeoLite2-City.mmdb"

geoip2_reader = geoip2.database.Reader(GEOIP_DATABASE_PATH)
# print("mmmmm",geoip2_reader)
# ip_address = '8.8.8.8'
# response = geoip2_reader.city(ip_address)

# # Print the location information
# print("Country:", response.country.name)
# print("City:", response.city.name)
# print("Subdivision:", response.subdivisions.most_specific.name)



@router.post('/admin-login')
def get_token(request_data: OAuth2PasswordRequestForm = Depends(), user_agent: str = Header(None), request: Request = None, db: Session = Depends(get_db)):
    # Parse user agent string
    user_agent_info = parse(user_agent)

    # Extract browser information
    browser_type = user_agent_info.browser.family
    browser_version = user_agent_info.browser.version_string

    # Extract operating system information
    operating_system = user_agent_info.os.family
    os_version = user_agent_info.os.version_string

    # Your existing code continues from here...
    user = db.query(models.AdminUser).filter(models.AdminUser.user_name == request_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid credentials')
    hashed_password_from_db = user.password
    plain_text_password_from_request = request_data.password
    if not Hash.verify(hashed_password_from_db, plain_text_password_from_request):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid password')

    # If the user exists and the password is valid, create a dictionary with user data
    data = {
        'user_id': user.id,
        'role_id': user.role_id
    }
    
    # Generate an access token using the data and the create_access_token function from oauth2.py
    access_token = oauth2.create_access_token(data=data)
    
    # Extract user IP address
    user_ip = request.client.host
    print("user_ip", user_ip)

    # Extract referrer from request headers
    referrer = request.headers.get('referer')

    city = None
    region = None
    country = None

    # Lookup geographic location based on IP address
    try:
        response = geoip2_reader.city(user_ip)
        city = response.city.name if response.city.name else ""
        region = response.subdivisions.most_specific.name if response.subdivisions.most_specific.name else ""
        country = response.country.name if response.country.name else ""
    except geoip2.errors.AddressNotFoundError:
        pass  # Handle error if needed

    # Insert login details into app_admin_log table
    db.execute(
        text("INSERT INTO app_admin_log (user_id, logged_in_ip, browser_type, browser_family, browser_version, operating_system, os_family, os_version, referrer, city,region,country) "
             "VALUES (:user_id, :logged_in_ip, :browser_type, :browser_family, :browser_version, :operating_system, :os_family, :os_version, :referrer, :city,:region,:country)"),
        {
            'user_id': user.id,
            'logged_in_ip': user_ip,
            'browser_type': browser_type,
            'browser_family': browser_type,  # Keeping it same as browser_type, you may adjust as needed
            'browser_version': browser_version,
            'operating_system': operating_system,
            'os_family': operating_system,  # Keeping it same as operating_system, you may adjust as needed
            'os_version': os_version,
            'referrer': referrer,
            'city': city,
            'region': region,
            'country': country
        }
    )

    # Commit the transaction
    db.commit()

    # Return a JSON response with the access token and additional information
    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }

def authenticate_user(token: str) -> Dict[str, Union[int, None]]:
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        role_id = payload.get("role_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id, "role_id": role_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    



@router.post('/admin-logout')
def logout_admin(request: Request, db: Session = Depends(get_db),
                 token: str = Depends(oauth2.oauth2_scheme)):

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]

    # Update logged_out_on field
    db.execute(
        update(models.AdminLog).
        where(models.AdminLog.user_id == user_id).
        values(logged_out_on=datetime.utcnow())
    )



    # Commit the transaction
    db.commit()

    # Return a response indicating successful logout
    return {'message': 'Logged out successfully'}

    
    


