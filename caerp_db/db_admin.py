
from fastapi import HTTPException,status
from caerp_db.models import AdminUser, Designation, UserRole
from caerp_schemas import AdminUserCreateSchema, AdminUserUpdateSchema, DesignationDeleteSchema, DesignationInputSchema, DesignationUpdateSchema, UserRoleDeleteSchema, UserRoleInputSchema, UserRoleUpdateSchema
from sqlalchemy.orm import Session
from caerp_db.hash import Hash
from caerp_db import models
from datetime import datetime



def get_all_roles(db: Session):
    return db.query(UserRole).all()



def get_user_role_by_id(db: Session, role_id: int):
    return db.query(UserRole).filter(UserRole.id == role_id).first()






def add_user_role(db: Session, role: str, created_by: int):
    new_role = models.UserRole(role=role, created_by=created_by)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role




def update_user_role(db: Session, role_id: int, role_input: UserRoleUpdateSchema, modified_by: int):
    existing_role = db.query(UserRole).filter(UserRole.id == role_id).first()

    if existing_role is None:
        raise HTTPException(status_code=404, detail="Role not found")

    for field, value in role_input.dict(exclude_unset=True).items():
        setattr(existing_role, field, value)

    existing_role.modified_by = modified_by
    existing_role.modified_on = datetime.utcnow()

    db.commit()
    db.refresh(existing_role)

    return existing_role





def delete_user_role(
    db: Session,
    role_id: int,
    role_input: UserRoleDeleteSchema,
    deleted_by: int
):
    existing_role = db.query(UserRole).filter(UserRole.id == role_id).first()

    if existing_role is None:
        raise HTTPException(status_code=404, detail="Role not found")

    existing_role.is_deleted = 'yes'
    existing_role.deleted_by = deleted_by
    existing_role.deleted_on = datetime.utcnow()

    db.commit()

    # Construct the response with the desired message
    response = {
        "message": "Deleted successfully",
        "role": role_input.role,
        "deleted_by": deleted_by,
        "deleted_on": datetime.utcnow()
    }

    return response



def get_all_designation(db: Session):
    return db.query(Designation).all()


def get_designation_by_id(db: Session, designation_id: int):
    return db.query(Designation).filter(Designation.id == designation_id).first()





def add_designation(db: Session, designation: str, created_by: int):
    new_designation = models.Designation(
        designation=designation,
        created_by=created_by
    )

    db.add(new_designation)
    db.commit()
    db.refresh(new_designation)

    return new_designation




def update_designation(db: Session, designation_id: int, role_input: DesignationUpdateSchema,modified_by: int):
    designation = db.query(Designation).filter(Designation.id == designation_id).first()

    if designation is None:
        raise HTTPException(status_code=404, detail="Designation not found")

    for field, value in role_input.dict(exclude_unset=True).items():
        setattr(designation, field, value)

        designation.modified_by = modified_by
        designation.modified_on = datetime.utcnow()
    db.commit()
    db.refresh(designation)

    return designation



def delete_designation(db: Session, designation_id: int, role_input: DesignationDeleteSchema,deleted_by: int):
    existing_designation = db.query(Designation).filter(Designation.id == designation_id).first()
    if existing_designation is None:
        raise HTTPException(status_code=404, detail="Designation not found")
    
    existing_designation.is_deleted = 'yes'
    existing_designation.deleted_by = deleted_by
    existing_designation.deleted_on = datetime.utcnow()
    db.commit()
    return {
        "message": "Role marked as deleted successfully",
        "role_id": designation_id,
        "deleted_by": deleted_by,
        "deleted_on": existing_designation.deleted_on
    }

 

    
    





# def create_admin_user(db: Session, user_data: AdminUserCreateSchema, user_id: int):
#     user_data_dict = user_data.dict()
#     user_data_dict["created_by"] = user_id
#     user_data_dict["created_on"] = datetime.utcnow()
#     # Hash the password using bcrypt
#     user_data_dict["password"] = Hash.bcrypt(user_data_dict["password"])
#     new_user = AdminUser(**user_data_dict)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# def create_admin_user(db: Session, user_data: AdminUserCreateSchema, user_id: int):
#     user_data_dict = user_data.dict()
#     user_data_dict["created_by"] = user_id
#     user_data_dict["created_on"] = datetime.utcnow()
#     # Hash the password using bcrypt
#     user_data_dict["password"] = Hash.bcrypt(user_data_dict["password"])
#     new_user = AdminUser(**user_data_dict)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
from sqlalchemy.exc import SQLAlchemyError


def create_admin_user(db: Session, user_data: AdminUserCreateSchema, user_id: int):
    try:
        user_data_dict = user_data.dict()
        print("User data dictionary:", user_data_dict) 
        user_data_dict["created_by"] = user_id
        user_data_dict["created_on"] = datetime.utcnow()
        # Hash the password using bcrypt
        user_data_dict["password"] = Hash.bcrypt(user_data_dict["password"])
        
        new_user = AdminUser(**user_data_dict)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    except SQLAlchemyError as e:
        # Rollback changes if an exception occurs
        db.rollback()
        print(f"An error occurred: {e}")
        raise e


def update_admin_user(db: Session, id: int, user_data: AdminUserUpdateSchema, user_id: int):
    user = db.query(AdminUser).filter(AdminUser.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_data_dict = user_data.dict(exclude_unset=True)
   
    for key, value in user_data_dict.items():
        setattr(user, key, value)
    user.modified_by = user_id
    user.modified_on = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user



def get_all_admin_users(db: Session):
    return db.query(AdminUser).all()

def get_user_by_username(db: Session, user_name: str):
    return db.query(AdminUser).filter(AdminUser.user_name == user_name).first()


def get_admin_users_by_id(db: Session, id: int):
    return db.query(AdminUser).filter(AdminUser.id == id).first()





def delete_admin_user(db: Session, id: int, role_input: AdminUserCreateSchema, deleted_by: int):
    deleted_user = db.query(AdminUser).filter(AdminUser.id == id).first()
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    deleted_user.is_deleted = 'yes'
    deleted_user.deleted_by = deleted_by
    deleted_user.deleted_on = datetime.utcnow()
    db.commit()
    return {
        "message": "User marked as deleted successfully",
        "deleted_by": deleted_by,
        "deleted_on": deleted_user.deleted_on
    }


def get_admin_user_by_id(db: Session, user_id: int):
    return db.query(AdminUser).filter(AdminUser.id == user_id).first()