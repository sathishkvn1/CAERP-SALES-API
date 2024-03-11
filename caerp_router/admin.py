from fastapi import APIRouter, Depends,HTTPException, UploadFile,status,File
from typing import List, Optional
from UserDefinedConstants.user_defined_constants import DeletedStatus
from caerp_auth.authentication import authenticate_user


from caerp_db.models import  AdminLog, AdminUser, Designation, UserRole
from caerp_schemas import AdminLogSchema, AdminUserActiveInactiveSchema, AdminUserBaseForDelete, AdminUserChangePasswordSchema, AdminUserCreateSchema, AdminUserDeleteSchema, AdminUserListResponse, AdminUserUpdateSchema, DesignationDeleteSchema, DesignationInputSchema, DesignationListResponse, DesignationListResponses, DesignationSchemaForDelete, DesignationUpdateSchema, User, UserImageUpdateSchema, UserLoginResponseSchema, UserLoginSchema, UserRoleDeleteSchema, UserRoleForDelete, UserRoleInputSchema, UserRoleListResponse, UserRoleListResponses, UserRoleSchema, UserRoleUpdateSchema
from sqlalchemy.orm import Session
from starlette.requests import Request

from settings import BASE_URL

from caerp_db.database import get_db
from caerp_db import db_admin
from caerp_db.hash import Hash
import jwt
from datetime import datetime, timedelta
from caerp_auth.oauth2 import oauth2_scheme,SECRET_KEY, ALGORITHM
from caerp_auth import oauth2
import os
from jose import JWTError, jwt

UPLOAD_DIR_ADMIN_PROFILE = "uploads/admin_profile"

router = APIRouter(
    # prefix="/admin",
    tags=["ADMIN"]
)

@router.get("/get_all_user_role", response_model=List[UserRoleListResponse])
def get_all_roles(db: Session = Depends(get_db)):

    user_role = db_admin.get_all_roles(db)
    return [{"roles": user_role}]
#---------------------------------------------------------------------------------------------------------------

@router.get("/get_user_role_by_id/{role_id}", response_model=UserRoleListResponse)
def get_user_role_by_id(role_id: int,
                        db: Session = Depends(get_db)):
    
    role_detail = db_admin.get_user_role_by_id(db, role_id)
    if role_detail is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"roles": [role_detail]}


#---------------------------------------------------------------------------------------------------------------


@router.post("/add/user_role", response_model=UserRoleInputSchema)
def create_new_user_role(
                         
                         role_input: UserRoleInputSchema,
                         db: Session = Depends(get_db),
                         token: str = Depends(oauth2.oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    new_user = db_admin.add_user_role(db=db, role=role_input.role, created_by=user_id)
    return {"role": role_input.role}  
    
    
#---------------------------------------------------------------------------------------------------------------


@router.post("/update/user_role/{role_id}", response_model=UserRoleUpdateSchema)
def update_user_role(
                    
                     role_id: int,
                     role_input: UserRoleUpdateSchema,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    return db_admin.update_user_role(db, role_id, role_input, modified_by=user_id)


#---------------------------------------------------------------------------------------------------------------



@router.delete("/delete/user_role/{role_id}", response_model=UserRoleDeleteSchema)
def delete_user_role(
    role_id: int,
    role_input: UserRoleDeleteSchema,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    return db_admin.delete_user_role(db, role_id, role_input, deleted_by=user_id)

#---------------------------------------------------------------------------------------------------------------

@router.get("/get_all_user_role/",response_model=List[UserRoleForDelete])
async def get_all_user_role(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                              ):
    return get_user_role_by_deleted_status(db, deleted_status)



def get_user_role_by_deleted_status(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(UserRole).filter(UserRole.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(UserRole).filter(UserRole.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(UserRole).all()
    else:
        # Handle invalid state or raise an error
        raise ValueError("Invalid deleted_status")

#---------------------------------------------------------------------------------------------------------------

@router.get("/get_all_designation_status/",response_model=List[DesignationSchemaForDelete])
async def get_all_designation(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                              ):
    return get_designations_by_deleted_status(db, deleted_status)




def get_designations_by_deleted_status(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(Designation).filter(Designation.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(Designation).filter(Designation.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(Designation).all()
    else:
        # Handle invalid state or raise an error
        raise ValueError("Invalid deleted_status")
#---------------------------------------------------------------------------------------------------------------    

@router.get("/get_all_designation/{designation_id}", response_model=DesignationListResponse)
def get_all_designation_by_id(designation_id: int,
                        db: Session = Depends(get_db),
                        ):

    designation_detail = db_admin.get_designation_by_id(db, designation_id)
    if designation_detail is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"designations": [designation_detail]}


#---------------------------------------------------------------------------------------------------------------




@router.post("/create_designation")
def create_designation(
    
    designation_data: DesignationInputSchema,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    # Check if token is missing
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]

    # Add designation
    new_designation = db_admin.add_designation(db=db, designation=designation_data.designation, created_by=user_id)

    # Return response
    return {"message": "Designation created successfully", "designation": new_designation}


#---------------------------------------------------------------------------------------------------------------


@router.post("/update/designation/{designation_id}", response_model=DesignationUpdateSchema)
def update_user_role(
                    
                     designation_id: int,
                     role_input: DesignationUpdateSchema,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
   
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    return db_admin.update_designation(db, designation_id, role_input, modified_by=user_id)


#---------------------------------------------------------------------------------------------------------------


@router.delete("/delete/designation/{designation_id}", response_model=DesignationDeleteSchema)
def delete_designation(
                     request: Request,
                     designation_id: int,
                     role_input: DesignationDeleteSchema,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    
    return db_admin.delete_designation(db, designation_id, role_input, deleted_by=user_id)


#---------------------------------------------------------------------------------------------------------------




@router.post('/add/admin_users', response_model=AdminUserCreateSchema)
def create_admin_user(
    user_data: AdminUserCreateSchema=Depends(),
    image_file: UploadFile = File(None),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    try:
        new_user = db_admin.create_admin_user(db, user_data, user_id)
        # If image provided, save it
        if image_file:
            file_content = image_file.file.read()
            file_path = f"{UPLOAD_DIR_ADMIN_PROFILE}/{new_user.id}.jpg"
            with open(file_path, "wb") as f:
                f.write(file_content)
        return new_user
    except Exception as e:
        error_detail = [{
            "loc": ["server"],
            "msg": "Internal server error",
            "type": "internal_server_error"
        }]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)
  
#---------------------------------------------------------------------------------------------------------------  
@router.post('/update/admin_users/{id}', response_model=AdminUserUpdateSchema)
def update_admin_user(
    id: int,
    user_data: AdminUserUpdateSchema=Depends(),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]

    try:
        updated_user = db_admin.update_admin_user(db, id, user_data, user_id)
        return updated_user
    except Exception as e:
        error_detail = [{
            "loc": ["server"],
            "msg": "Internal server error",
            "type": "internal_server_error"
        }]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)
    
#---------------------------------------------------------------------------------------------------------------
@router.post('/change_password/{id}', response_model=AdminUserCreateSchema)
def change_password(
        id: int,
        password_data: AdminUserChangePasswordSchema,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    # Check authorization, find user, and check permissions as before
    
    # Retrieve user from the database
    user = db.query(AdminUser).filter(AdminUser.id == id).first()
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



@router.post('/update_admin_user_image/{id}', response_model=AdminUserCreateSchema)
def update_admin_user_image(
        id: int,
        image_file: UploadFile = File(...),  # Required image file
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    # Check if the user exists
    user = db.query(AdminUser).filter(AdminUser.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Save the new image
    file_content = image_file.file.read()
    file_path = f"{UPLOAD_DIR_ADMIN_PROFILE}/{user.id}.jpg"
    with open(file_path, "wb") as f:
        f.write(file_content)

    # Return the updated user data
    return user


#---------------------------------------------------------------------------------------------------------------

@router.delete("/delete/admin_user/{id}", response_model=AdminUserDeleteSchema)
def delete_admin_user(
                     
                     id: int,
                     role_input: AdminUserCreateSchema,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]

    return db_admin.delete_admin_user(db, id, role_input, deleted_by=user_id)


#---------------------------------------------------------------------------------------------------------------

@router.get("/get_all_admin_users/",response_model=List[AdminUserBaseForDelete])
async def get_all_admin_users(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                              ):
    return get_users_by_deleted_status(db, deleted_status)



def get_users_by_deleted_status(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(AdminUser).filter(AdminUser.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(AdminUser).filter(AdminUser.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(AdminUser).all()
    else:
        # Handle invalid state or raise an error
        raise ValueError("Invalid deleted_status")

#---------------------------------------------------------------------------------------------------------------


@router.get("/get_admin_users/{id}", response_model=AdminUserListResponse)
def get_admin_users_by_id(id: int,
                          db: Session = Depends(get_db)
                          ):
    
    user_detail = db_admin.get_admin_users_by_id(db, id)
    if user_detail is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"users": [user_detail]}

#---------------------------------------------------------------------------------------------------------------
@router.get("/logged_in_user", response_model=AdminUserBaseForDelete)
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
        AdminUserBaseForDelete: Details of the logged-in user.

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

    logged_in_user = db_admin.get_admin_user_by_id(db, user_id)

    if not logged_in_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User details not found"
        )

    return logged_in_user

#---------------------------------------------------------------------------------------------------------------
 


# @router.get("/logged_in_admin_user/image_url", response_model=dict)
# def get_logged_in_admin_user_image_url(
#         db: Session = Depends(get_db),
#         token: str = Depends(oauth2.oauth2_scheme)):
    
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token is missing"
#         )

#     auth_info = authenticate_user(token)
#     user_id = auth_info["user_id"]
    
#     profile_photo_filename = f"{user_id}.jpg"  
#     BASE_URL = "http://127.0.0.1:5000/"
#     return {"photo_url": f"{BASE_URL}admin_profile/{profile_photo_filename}"}


#---------------------------------------------------------------------------------------------------------------

@router.get("/logged_in_admin_user/image_url", response_model=dict)
def get_logged_in_admin_user_image_url(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    """
    Retrieve the URL of the profile image for the logged-in admin user or for a specific admin user if the `user_id` parameter is provided.

    Args:
        user_id (int, optional): The ID of the admin user whose image URL is to be retrieved. If not provided, the image URL for the currently logged-in user will be returned. Defaults to None.
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).
        token (str): Authentication token obtained during login.

    Returns:
        dict: A JSON object containing the image URL.

    Raises:
        HTTPException: If the authentication token is missing or invalid.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing"
        )

    if user_id is not None:
        # Use the provided user_id
        profile_photo_filename = f"{user_id}.jpg"
    else:
        # Use the user_id extracted from the token
        auth_info = authenticate_user(token)
        user_id = auth_info["user_id"]
        profile_photo_filename = f"{user_id}.jpg"
    
    # Construct the photo URL
    photo_url = f"{BASE_URL}/admin/add/admin_users/{profile_photo_filename}"
    
    return {"photo_url": photo_url}


#---------------------------------------------------------------------------------------------------------------

@router.post("/admin_users/activate_deactivate", response_model=AdminUserActiveInactiveSchema)
def update_admin_user_status(user_data: AdminUserActiveInactiveSchema=Depends(), db: Session = Depends(get_db)):
    user = db.query(AdminUser).filter(AdminUser.id == user_data.id).first()
    if user:
        user.is_active = user_data.is_active
        db.commit()
        return user_data
    else:
        raise HTTPException(status_code=404, detail="User not found")
    


#---------------------------------------------------------------------------------------------------------------


@router.get("/get_admin_logs_by_user_id/", response_model=List[AdminLogSchema])
def get_admin_logs_by_user_id(db: Session = Depends(get_db), token: str = Depends(oauth2.oauth2_scheme)):
    """
    Retrieve all admin log details for the currently logged-in user.

    Args:
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).
        token (str): Authentication token obtained during login.

    Returns:
        List[AdminLogSchema]: List of admin log details for the currently logged-in user.

    Raises:
        HTTPException: If the token is missing or invalid, or if there are no admin logs for the user.
    """

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing"
        )
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]

    admin_logs = db.query(AdminLog).filter(AdminLog.user_id == user_id).all()
    if not admin_logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin logs not found for this user")
    
    
    admin_logs_schema = [AdminLogSchema.from_orm(admin_log) for admin_log in admin_logs]
    
    return admin_logs_schema

#---------------------------------------------------------------------------------------------------------------
@router.get("/get_all_admin_logs/", response_model=List[AdminLogSchema])
def get_all_admin_logs(db: Session = Depends(get_db), token: str = Depends(oauth2.oauth2_scheme)):
    """
    Retrieve all admin log details from the database.

    Args:
        db (Session, optional): SQLAlchemy database session. Defaults to Depends(get_db).
        token (str): Authentication token obtained during login.

    Returns:
        List[AdminLogSchema]: List of admin log details.

    Raises:
        HTTPException: If the token is missing or invalid.
    """

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing"
        )

  
    # Query all admin logs
    admin_logs = db.query(AdminLog).all()

    return admin_logs
#---------------------------------------------------------------------------------------------------------------

