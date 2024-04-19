
from fastapi import APIRouter, Depends,HTTPException, UploadFile,status,File
from typing import List, Optional
from UserDefinedConstants.user_defined_constants import DeletedStatus
from caerp_auth.authentication import authenticate_user
from caerp_db.models import  AdminUser, Designation,PriceListProductModuleView,PriceListProductModule,PriceListProductMasterView,PriceListProductMaster, InstallmentDetails, InstallmentMaster, ProductCategory, ProductMaster, ProductModule, ProductVideo, UserRole
from caerp_schemas import AdminUserBaseForDelete, AdminUserChangePasswordSchema, AdminUserCreateSchema, AdminUserDeleteSchema, AdminUserListResponse, AdminUserUpdateSchema, DesignationDeleteSchema, DesignationInputSchema, DesignationListResponse, DesignationListResponses, DesignationSchemaForDelete, DesignationUpdateSchema, InstallmentCreate, InstallmentDetail, InstallmentDetailsBase, InstallmentDetailsCreate, InstallmentMasterBase,  InstallmentMasterForGet, ProductCategorySchema, ProductMasterSchema, ProductModuleSchema, ProductVideoSchema, User, UserImageUpdateSchema, UserLoginResponseSchema, UserLoginSchema, UserRoleDeleteSchema, UserRoleForDelete, UserRoleInputSchema, UserRoleListResponse, UserRoleListResponses, UserRoleSchema, UserRoleUpdateSchema
from sqlalchemy.orm import Session
from starlette.requests import Request

from settings import BASE_URL

from caerp_db.database import get_db
from caerp_db import db_product
from caerp_db.hash import Hash
import jwt
from datetime import datetime, timedelta,date
from caerp_auth.oauth2 import oauth2_scheme,SECRET_KEY, ALGORITHM
from caerp_auth import oauth2
import os
from jose import JWTError, jwt
from sqlalchemy import and_


def save_product_video(db: Session,  request: ProductVideoSchema, user_id: int):

    # if product_video_id == 0:
        # Add operation
        product_video_data_dict = request.dict()
        product_video_data_dict["created_on"] = datetime.utcnow()
        product_video_data_dict["created_by"] = user_id
        new_product_video = ProductVideo(**product_video_data_dict)
        db.add(new_product_video)
        db.commit()
        db.refresh(new_product_video)
        return new_product_video


    
def update_product_video(db: Session,  request: ProductVideoSchema, video_id: int, user_id: int):

        # Update operation
        product_video = db.query(ProductVideo).filter(ProductVideo.id == video_id).first()
        if product_video is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Video not found")
        product_video_data_dict = request.dict(exclude_unset=True)
        for key, value in product_video_data_dict.items():
            setattr(product_video, key, value)
        product_video.modified_by = user_id
        product_video.modified_on = datetime.utcnow()
        db.commit()
        db.refresh(product_video)
        return product_video









# =========================================================================

#  PRODUCT MODULE SECTION 
# ==========================================================================

def save_product_module(db: Session, request: ProductModuleSchema,display_order:int, user_id: int ):

    # if product_module_id == 0:
        # Add operation
        product_module_data_dict = request.dict()
        product_module_data_dict["created_on"] = datetime.utcnow()
        product_module_data_dict["created_by"] = user_id
        product_module_data_dict["display_order"] = display_order
        new_product_module = ProductModule(**product_module_data_dict)
        db.add(new_product_module)
        db.commit()
        db.refresh(new_product_module)
        return new_product_module
    
def update_product_module(db: Session,  request: ProductModuleSchema, module_id: int, user_id: int):

        # Update operation
        product_module = db.query(ProductModule).filter(ProductModule.id == module_id).first()
        if product_module is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Module not found")
        product_module_data_dict = request.dict(exclude_unset=True)
        for key, value in product_module_data_dict.items():
            setattr(product_module, key, value)
        product_module.modified_by = user_id
        product_module.modified_on = datetime.utcnow()  
        db.commit()
        db.refresh(product_module)
        return product_module


#=========================================================================

# product master section 

#=========================================================

def save_product_master(db: Session,  request: ProductMasterSchema, user_id: int ):

   
        # Add operation
        product_master_data_dict = request.dict()
        product_master_data_dict["created_on"] = datetime.utcnow()
        product_master_data_dict["created_by"] = user_id
        new_product_master = ProductMaster(**product_master_data_dict)
        db.add(new_product_master)
        db.commit()
        db.refresh(new_product_master)
        return new_product_master
    
def update_product_master(db: Session,  request: ProductMasterSchema, product_master_id: int, user_id: int):    

        # Update operation
        product_master = db.query(ProductMaster).filter(ProductMaster.id == product_master_id).first()
        if product_master is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Master not found")
        product_master_data_dict = request.dict(exclude_unset=True)
        for key, value in product_master_data_dict.items():
            setattr(product_master, key, value)
        product_master.modified_by = user_id
        product_master.modified_on = datetime.utcnow()   
        db.commit()
        db.refresh(product_master)
        return product_master





def get_all_product_master_by_deleted_status(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(ProductMaster).filter(ProductMaster.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(ProductMaster).filter(ProductMaster.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(ProductMaster).all()
    else:
       
        raise ValueError("Invalid deleted_status")




def get_product_master_by_id(db: Session,id: int):
        
        return db.query(ProductMaster).filter(ProductMaster.id== id).all()
    


def get_product_master_by_code(db: Session,code: str):
        
        return db.query(ProductMaster).filter(ProductMaster.product_code== code).all()



def delete_product_master(db: Session, product_id: int,action_type:str,deleted_by: int):
    existing_product = db.query(ProductMaster).filter(ProductMaster.id == product_id).first()

    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if(action_type== 'DELETE'):

            existing_product.is_deleted = 'yes'
            existing_product.deleted_by = deleted_by
            existing_product.deleted_on = datetime.utcnow()
            
            # Mark related installment details as deleted
            db.query(ProductModule).filter(ProductModule.product_master_id == product_id).update({
                ProductModule.is_deleted: 'yes',
                ProductModule.is_deleted_with_master: 'yes',
                ProductModule.deleted_by: deleted_by,
                ProductModule.deleted_on: datetime.utcnow()
            }, synchronize_session=False)
        
            db.commit()

            return {
                "message": "Product marked as deleted successfully",

            }
    if(action_type == 'UNDELETE'):
            existing_product.is_deleted = 'no'
            existing_product.deleted_by = None
            existing_product.deleted_on = None
            db.commit()

            return {
                "message": "Product marked as Undeleted successfully",

            }


# =========================================================================

#  PRODUCT CATEGORY SECTION 
# ==========================================================================

def save_product_category(db: Session,  request: ProductCategorySchema, product_category_id: int,user_id: int):

    if product_category_id == 0:
        # Add operation
        product_category_data_dict = request.dict()
        product_category_data_dict["created_on"] = datetime.utcnow()
        product_category_data_dict["created_by"] = user_id
        new_product_category = ProductCategory(**product_category_data_dict)
        db.add(new_product_category)
        db.commit()
        db.refresh(new_product_category)
        return new_product_category
    
    else:
        # Update operation
        product_category = db.query(ProductCategory).filter(ProductCategory .id == product_category_id).first()
        if product_category is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Category not found")
        product_category_data_dict = request.dict(exclude_unset=True)
        for key, value in product_category_data_dict.items():
            setattr(product_category, key, value)
        product_category.modified_by = user_id
        product_category.modified_on = datetime.utcnow()
        
        db.commit()
        db.refresh(product_category)
        return product_category





def get_all_product_category_by_deleted_status(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(ProductCategory).filter(ProductCategory.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(ProductCategory).filter(ProductCategory.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(ProductCategory).all()
    else:
       
        raise ValueError("Invalid deleted_status")




def get_product_category_by_id(db: Session,id: int):
        
        return db.query(ProductCategory).filter(ProductCategory.id== id).all()


def delete_product_category(db: Session, category_id: int,deleted_by: int):
    existing_product = db.query(ProductCategory).filter(ProductCategory.id == category_id).first()

    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product category not found")

    existing_product.is_deleted = 'yes'
    existing_product.deleted_by = deleted_by
    existing_product.deleted_on = datetime.utcnow()
   
    db.commit()

    return {
        "message": "Product category marked as deleted successfully",

    }



def get_product_module_by_id(db: Session,id: int):
        return db.query(ProductModule).filter(ProductModule.id== id).all()
    


def get_product_module_by_product_id(db: Session,id: int):
        return db.query(ProductModule).filter(and_(ProductModule.product_master_id == id, ProductModule.is_deleted == "no")).all()


def delete_product_module(db: Session, module_id: int,action_type:str,deleted_by: int):
    existing_product = db.query(ProductModule).filter(ProductModule.id == module_id).first()

    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product module not found")
    if(action_type== 'DELETE'):

        existing_product.is_deleted = 'yes'
        existing_product.is_deleted_directly= 'yes'
        existing_product.deleted_by = deleted_by
        existing_product.deleted_on = datetime.utcnow()
    
        db.commit()

        return {
            "message": "Product module marked as deleted successfully",

        }
    if(action_type == 'UNDELETE'):
            existing_product.is_deleted = 'no'
            existing_product.deleted_by = None
            existing_product.deleted_on = None
            existing_product.is_deleted_directly = 'no'
            existing_product.is_deleted_with_master = 'no'

            db.commit()

            return {
                "message": "Product module marked as Undeleted successfully",

            }




# =========================================================================

#  PRODUCT VIDEO SECTION 
# ==========================================================================




def get_all_product_video_by_deleted_status(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(ProductVideo).filter(ProductVideo.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(ProductVideo).filter(ProductVideo.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(ProductVideo).all()
    else:
       
        raise ValueError("Invalid deleted_status")




def get_product_video_by_id(db: Session,id: int):
        
        return db.query(ProductVideo).filter(ProductVideo.id== id).all()
    



def get_product_video_by_product_master_id(db: Session, id: int):
    return db.query(ProductVideo).filter(and_(ProductVideo.product_master_id == id, ProductVideo.is_deleted == "no")).all()


def delete_product_video(db: Session, video_id: int,deleted_by: int):
    existing_video = db.query(ProductVideo).filter(ProductVideo.id == video_id).first()

    if existing_video is None:
        raise HTTPException(status_code=404, detail="Product video not found")

    existing_video.is_deleted = 'yes'
    existing_video.deleted_by = deleted_by
    existing_video.deleted_on = datetime.utcnow()
   
    db.commit()

    return {
        "message": "Product video marked as deleted successfully",

    }






 
    
   


    
    
def get_installment_details_by_id(db: Session, id: int):
    return db.query(InstallmentDetails).filter(InstallmentDetails.id == id).first()






def create_installments(db: Session, installment_data: InstallmentCreate, user_id: int):
    # Create the installment master record
    db_installment_master = InstallmentMaster(
        number_of_installments=installment_data.number_of_installments,
        is_active=installment_data.is_active,
        active_from_date=datetime.utcnow(),  
        created_by=user_id
    )
    db.add(db_installment_master)
    db.commit()
    db.refresh(db_installment_master)
    
    # Create the installment details records
    installment_details = []
    for detail in installment_data.installment_details:
        installment_detail = InstallmentDetails(
            installment_master_id=db_installment_master.id,
            installment_name=detail.installment_name,
            payment_rate=detail.payment_rate,
            due_date=detail.due_date,
            created_by=user_id
        )
        db.add(installment_detail)
        installment_details.append(installment_detail)
    
    db.commit()
    
    return db_installment_master, installment_details


def update_installment_master(db: Session, installment_id: int, data: dict, user_id: int):
    db_installment = db.query(InstallmentMaster).filter(InstallmentMaster.id == installment_id).first()
    if db_installment:
        for key, value in data.items():
            setattr(db_installment, key, value)
        db_installment.modified_by = user_id
        db_installment.modified_on = datetime.utcnow()   
        db.commit()
        db.refresh(db_installment)
        return db_installment
    return None

def update_installment_details(db: Session, installment_id: int, data: dict, user_id: int):
    db_installment_details = db.query(InstallmentDetails).filter(InstallmentDetails.installment_master_id == installment_id).all()
    if db_installment_details:
        for installment_detail in db_installment_details:
            for key, value in data.items():
                setattr(installment_detail, key, value)
            installment_detail.modified_by = user_id
            installment_detail.modified_on = datetime.utcnow()   
        db.commit()
        return db_installment_details
    return None



def delete_installment_master(db: Session, id: int, deleted_by: int):
    existing_installment_master = db.query(InstallmentMaster).filter(InstallmentMaster.id == id).first()

    if existing_installment_master is None:
        raise HTTPException(status_code=404, detail="Installment master not found")

    # Mark the installment master as deleted
    existing_installment_master.is_deleted = 'yes'
    existing_installment_master.deleted_by = deleted_by
    existing_installment_master.deleted_on = datetime.utcnow()

    # Mark related installment details as deleted
    db.query(InstallmentDetails).filter(InstallmentDetails.installment_master_id == id).update({
        InstallmentDetails.is_deleted: 'yes',
        InstallmentDetails.deleted_by: deleted_by,
        InstallmentDetails.deleted_on: datetime.utcnow()
    }, synchronize_session=False)

    db.commit()

    return {
        "message": "Installment master and related details deleted successfully",
    }

#=======================================================================================

def get_all_price_list_product_master(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(PriceListProductMaster).filter(PriceListProductMaster.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(PriceListProductMaster).filter(PriceListProductMaster.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(PriceListProductMaster).all()
    else:
       
        raise ValueError("Invalid deleted_status")



# def get_price_list_product_master_by_id(db: Session, id: int, requested_date: datetime):
#     return db.query(PriceListProductMaster).filter(
#         PriceListProductMaster.id == id,
#         PriceListProductMaster.effective_from_date <= requested_date,
#         PriceListProductMaster.effective_to_date >= requested_date
#     ).order_by(PriceListProductMaster.effective_from_date.desc()).limit(1).all()

def get_price_list_product_master_by_id(db: Session, id: int, requested_date: date):
    if requested_date is None:
        return db.query(PriceListProductMasterView).filter(
            PriceListProductMasterView.module_id == id
        ).order_by(PriceListProductMasterView.effective_from_date.desc()).all()
    else :
        return db.query(PriceListProductMasterView).filter(
        PriceListProductMasterView.product_master_id == id,
        PriceListProductMasterView.effective_from_date <= requested_date,
        PriceListProductMasterView.effective_to_date >= requested_date
    # ).order_by(PriceListProductMasterView.effective_from_date.desc()).limit(1).all()
    ).order_by(PriceListProductMasterView.effective_from_date.desc()).all()

def get_price_list_product_master_by_code(db: Session, product_code: int, requested_date: date):
   return db.query(PriceListProductMasterView).filter(
        PriceListProductMasterView.product_code == product_code,
        PriceListProductMasterView.effective_from_date <= requested_date,
        PriceListProductMasterView.effective_to_date >= requested_date
    ).order_by(PriceListProductMasterView.effective_from_date.desc()).limit(1).all()
  

def save_price_list_product_master(db: Session, request: PriceListProductMaster, price_list_id: int,user_id: int):
     
    if price_list_id == 0:
        # Add operation
        price_list_data_dict = request.dict()
        price_list_data_dict["created_on"] = datetime.utcnow()
        price_list_data_dict["created_by"] = user_id
        # price_list_data_dict["effective_from_date"] = datetime.utcnow()
        new_price_list = PriceListProductMaster(**price_list_data_dict)
        db.add(new_price_list)
        db.commit()
        db.refresh(new_price_list)
        return new_price_list
    
    else:
        # Update operation
        price_list = db.query(PriceListProductMaster).filter(PriceListProductMaster .id == price_list_id).first()
        if price_list is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price List not found")
        price_list_data_dict = request.dict(exclude_unset=True)
        for key, value in price_list_data_dict.items():
            setattr(price_list, key, value)
        price_list.modified_by = user_id
        price_list.modified_on = datetime.utcnow()
        
        db.commit()
        db.refresh(price_list)
        return price_list
    
def update_price_list_product_master(db: Session, request:PriceListProductMaster,price_list_id:int , user_id: int):
        
        price_list_data_dict = request.dict()
        price_list_data_dict["created_on"] = datetime.utcnow()
        price_list_data_dict["created_by"] = user_id
        new_price_list = PriceListProductMaster(**price_list_data_dict)
        # price_list_data_dict["effective_from_date"] = datetime.utcnow()
        existing_price_list = db.query(PriceListProductMaster).filter(PriceListProductMaster .id == price_list_id).first()
        if existing_price_list is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price List not found")
        
        existing_price_list.effective_to_date = new_price_list.effective_from_date
        db.add(new_price_list)
        db.commit()
        db.refresh(new_price_list)
        return new_price_list



def delete_price_list_product_master(db: Session, price_list_product_master_id: int,action_type:str,deleted_by: int):
    existing_price_list = db.query(PriceListProductMaster).filter(PriceListProductMaster.id == price_list_product_master_id).first()

    if existing_price_list is None:
        raise HTTPException(status_code=404, detail="Price list not found")
    if(action_type== 'DELETE'):

        existing_price_list.is_deleted = 'yes'
        existing_price_list.is_deleted_directly= 'yes'
        existing_price_list.deleted_by = deleted_by
        existing_price_list.deleted_on = datetime.utcnow()
    
        db.commit()

        return {
            "message": "Price list marked as deleted successfully",

        }
    if(action_type == 'UNDELETE'):
            existing_price_list.is_deleted = 'no'
            existing_price_list.deleted_by = None
            existing_price_list.deleted_on = None
            existing_price_list.is_deleted_directly = 'no'
            existing_price_list.is_deleted_with_master = 'no'

            db.commit()

            return {
                "message": "Price list marked as Undeleted successfully",

            }


#=======================================================================================

def get_all_price_list_product_module(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(PriceListProductModuleView).filter(PriceListProductModuleView.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(PriceListProductModuleView).filter(PriceListProductModuleView.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(PriceListProductModuleView).all()
    else:
       
        raise ValueError("Invalid deleted_status")



# # def get_price_list_product_module_by_id(db: Session, id: int, requested_date: date):
# #     return db.query(PriceListProductModule).filter(
# #         PriceListProductModule.module_id == id,
# #         PriceListProductModule.effective_from_date <= requested_date,
# #         PriceListProductModule.effective_to_date >= requested_date
# #     ).order_by(PriceListProductModule.effective_from_date.desc()).limit(1).all()

def get_price_list_product_module_by_id(db: Session, id: int, requested_date: date):
    if requested_date is None:
        return db.query(PriceListProductModuleView).filter(
            PriceListProductModuleView.module_id == id
        ).order_by(PriceListProductModuleView.module_effective_from_date.desc()).all()
    else :
        return db.query(PriceListProductModuleView).filter(
            PriceListProductModuleView.module_id == id,
            PriceListProductModuleView.module_effective_from_date <= requested_date,
            PriceListProductModuleView.module_effective_to_date >= requested_date
        ).order_by(PriceListProductModuleView.module_effective_from_date.desc()).all()

        # ).order_by(PriceListProductModuleView.effective_from_date.desc()).limit(1).all()

def get_price_list_product_module_by_code(db: Session, product_code: int, requested_date: date):
   return db.query(PriceListProductModuleView).filter(
        PriceListProductModuleView.product_code == product_code,
        PriceListProductModuleView.module_effective_from_date <= requested_date,
        PriceListProductModuleView.module_effective_from_date >= requested_date
    # ).order_by(PriceListProductModuleView.effective_from_date.desc()).limit(1).all()
    ).order_by(PriceListProductModuleView.module_effective_from_date.desc()).all()
  

def save_price_list_product_module(db: Session, request: PriceListProductModule, price_list_id: int,user_id: int):
     
    if price_list_id == 0:
        # Add operation
        price_list_data_dict = request.dict()
        price_list_data_dict["created_on"] = datetime.utcnow()
        price_list_data_dict["created_by"] = user_id
        # price_list_data_dict["effective_from_date"] = datetime.utcnow()
        new_price_list = PriceListProductModule(**price_list_data_dict)
        db.add(new_price_list)
        db.commit()
        db.refresh(new_price_list)
        return new_price_list
    
    else:
        # Update operation
        price_list = db.query(PriceListProductModule).filter(PriceListProductModule .id == price_list_id).first()
        if price_list is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price List not found")
        price_list_data_dict = request.dict(exclude_unset=True)
        for key, value in price_list_data_dict.items():
            setattr(price_list, key, value)
        price_list.modified_by = user_id
        price_list.modified_on = datetime.utcnow()
        
        db.commit()
        db.refresh(price_list)
        return price_list
    
def update_price_list_product_module(db: Session, request:PriceListProductModule,price_list_id:int , user_id: int):
        
        price_list_data_dict = request.dict()
        price_list_data_dict["created_on"] = datetime.utcnow()
        price_list_data_dict["created_by"] = user_id
        new_price_list = PriceListProductModule(**price_list_data_dict)
        # price_list_data_dict["effective_from_date"] = datetime.utcnow()
        existing_price_list = db.query(PriceListProductModule).filter(PriceListProductModule .id == price_list_id).first()
        if existing_price_list is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price List not found")
        
        existing_price_list.effective_to_date = new_price_list.effective_from_date
        db.add(new_price_list)
        db.commit()
        db.refresh(new_price_list)
        return new_price_list



def delete_price_list_product_module(db: Session, price_list_product_module_id: int,action_type:str,deleted_by: int):
    existing_price_list = db.query(PriceListProductModule).filter(PriceListProductModule.id == price_list_product_module_id).first()

    if existing_price_list is None:
        raise HTTPException(status_code=404, detail="Price list not found")
    if(action_type== 'DELETE'):

        existing_price_list.is_deleted = 'yes'
        existing_price_list.is_deleted_directly= 'yes'
        existing_price_list.deleted_by = deleted_by
        existing_price_list.deleted_on = datetime.utcnow()
    
        db.commit()

        return {
            "message": "Price list marked as deleted successfully",

        }
    if(action_type == 'UNDELETE'):
            existing_price_list.is_deleted = 'no'
            existing_price_list.deleted_by = None
            existing_price_list.deleted_on = None
            existing_price_list.is_deleted_directly = 'no'
            existing_price_list.is_deleted_with_master = 'no'

            db.commit()

            return {
                "message": "Price list marked as Undeleted successfully",

            }
