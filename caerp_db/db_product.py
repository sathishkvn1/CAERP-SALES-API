
from fastapi import APIRouter, Depends,HTTPException, UploadFile,status,File
from typing import List, Optional,Dict,Any
from UserDefinedConstants.user_defined_constants import DeletedStatus,Operator,Status,RecordActionType,ApplyTo
from UserDefinedConstants.user_defined_constants import ActiveStatus, InstallmentStatus
from caerp_auth.authentication import authenticate_user
from caerp_db.models import  AdminUser,ProductMasterPrice,OfferDetails,OfferMaster,OfferCategory,ProductModulePrice, Designation,ProductRating,ViewProductModulePrice,CustomerRegister,ViewProductMasterPrice,InstallmentDetails, InstallmentMaster, ProductCategory, ProductMaster, ProductModule, ProductVideo, UserRole
from caerp_db.models import CartDetails,CouponMaster,ProductFeatures, ProductGroup, CouponDetails, CustomerCompanyProfile, CustomerProfessionalQualification,ProductTrialFeatures
from caerp_schemas import AdminUserBaseForDelete,CartDetailsSchema,CouponMasterSchema, InstallmentDetailsResponse,OfferDetailsSchema, SaveOfferDetailsRequest,ProductMasterPriceSchema,OfferMasterSchema,ProductModulePriceSchema, AdminUserChangePasswordSchema, AdminUserCreateSchema, AdminUserDeleteSchema, AdminUserListResponse, AdminUserUpdateSchema, DesignationDeleteSchema, DesignationInputSchema, DesignationListResponse, DesignationListResponses, DesignationSchemaForDelete, DesignationUpdateSchema, InstallmentCreate, InstallmentDetail, InstallmentDetailsBase, InstallmentDetailsCreate, InstallmentMasterBase,  InstallmentMasterForGet, ProductCategorySchema, ProductMasterSchema, ProductModuleSchema, ProductVideoSchema, User, UserImageUpdateSchema, UserLoginResponseSchema, UserLoginSchema, UserRoleDeleteSchema, UserRoleForDelete, UserRoleInputSchema, UserRoleListResponse, UserRoleListResponses, UserRoleSchema, UserRoleUpdateSchema, ProductFeaturesSchema, ProductFeaturesSchemaResponse, ProductMasterSchemaResponse, SaveCouponDetails, CouponDetailsSchema, CouponMasterSchemaResponse,OfferMasterSchemaResponse, InstallmentDetailsForGet,UpdateInstallmentRequest, ProductTrialFeatureSchema
from sqlalchemy.orm import Session
from starlette.requests import Request
from sqlalchemy import text, select
from settings import BASE_URL
from typing import Union
from caerp_db.database import get_db
from caerp_db import db_product
from caerp_db.hash import Hash
import jwt
from datetime import datetime, timedelta,date
from caerp_auth.oauth2 import oauth2_scheme,SECRET_KEY, ALGORITHM
from caerp_auth import oauth2
from caerp_router.common_functions import get_info
import os
from jose import JWTError, jwt
from sqlalchemy import and_,or_
from sqlalchemy.exc import SQLAlchemyError,IntegrityError,OperationalError
import logging
from fastapi.responses import FileResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# def save_product_video(db: Session,  request: ProductVideoSchema, user_id: int):

#     # if product_video_id == 0:
#         # Add operation
#         product_video_data_dict = request.dict()
#         product_video_data_dict["created_on"] = datetime.utcnow()
#         product_video_data_dict["created_by"] = user_id
#         new_product_video = ProductVideo(**product_video_data_dict)
#         db.add(new_product_video)
#         db.commit()
#         db.refresh(new_product_video)
#         return new_product_video




def save_product_video_in_db(db: Session, product_master_id: int, video_title: str, video_description: str, user_id: int):
    try:
        product_video_data_dict = {
            "product_master_id": product_master_id,
            "video_title": video_title,
            "video_description": video_description,
            "created_on": datetime.utcnow(),
            "created_by": user_id
        }

        new_product_video = ProductVideo(**product_video_data_dict)
        db.add(new_product_video)
        db.commit()
        db.refresh(new_product_video)

        return new_product_video

    except Exception as e:
        print("DB Error:", str(e))
        db.rollback()
        raise HTTPException(status_code=500, detail="Database operation failed")

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

# def save_product_module(db: Session, request: ProductModuleSchema,display_order:int, user_id: int ):

#     # if product_module_id == 0:
#         # Add operation
#         product_module_data_dict = request.dict()
#         product_module_data_dict["created_on"] = datetime.utcnow()
#         product_module_data_dict["created_by"] = user_id
#         product_module_data_dict["display_order"] = display_order
#         new_product_module = ProductModule(**product_module_data_dict)
#         db.add(new_product_module)
#         db.commit()
#         db.refresh(new_product_module)
#         master_price_id =db.query(ProductMasterPrice.id).filter(ProductMasterPrice.product_master_id == new_product_module.product_master_id).first()
#         # master_price_id = new_product_module.product_master_id
#         print("price id",master_price_id)
#         new_product_module_price = ProductModulePrice(
#         module_id=new_product_module.id,  
#         product_master_price_id= master_price_id,
#         module_price=0.0,
#         gst_rate = 0.0,
#         cess_rate = 0.0,
#         created_on= datetime.utcnow(),
#         created_by = user_id,
#         effective_from_date= date.today(),
#         effective_to_date = None
#         )
#         try:
             
#             db.add(new_product_module_price)
#             db.commit()
#             db.refresh(new_product_module_price)
#         except Exception as e:
#              print(f"An error occurred: {e}") 
             
#         return new_product_module



def save_product_module(db: Session, request: ProductModuleSchema, display_order: int, user_id: int):
    
        # Add operation
        product_module_data_dict = request.dict()
        product_module_data_dict["created_on"] = datetime.utcnow()
        product_module_data_dict["created_by"] = user_id
        product_module_data_dict["display_order"] = display_order
        new_product_module = ProductModule(**product_module_data_dict)
        db.add(new_product_module)
        db.commit()
        db.refresh(new_product_module)
        # Query the master_price_id
        result = db.query(ProductMasterPrice.id).filter(
             ProductMasterPrice.product_master_id == new_product_module.product_master_id
             
             ).order_by(ProductMasterPrice.effective_from_date.desc()).first()
        # Check if result is found and extract the master_price_id
        if result:
            master_price_id = result[0]
        else:
            raise ValueError("ProductMasterPrice not found for the given product_master_id")
        new_product_module_price = ProductModulePrice(
            module_id=new_product_module.id,  
            product_master_price_id=master_price_id,
            module_base_price=0.0,
            additional_price_per_user=0.0,
            gst_rate=0.0,
            cess_rate=0.0,
            created_on=datetime.utcnow(),
            created_by=user_id,
            effective_from_date=date.today(),
            effective_to_date=None
        )
        db.add(new_product_module_price)
        db.commit()
        db.refresh(new_product_module_price)
        return new_product_module
    
    
    # except SQLAlchemyError as e:
    #     db.rollback()
    #     print(f"An error occurred: {e}")
    #     raise
    # except Exception as e:
    #     db.rollback()
    #     print(f"An unexpected error occurred: {e}")
    #     raise
    # finally:
        # db.close()



def update_product_module(db: Session,  request: ProductModuleSchema, module_id: int, user_id: int):

        # Update operation
        product_module = db.query(ProductModule).filter(ProductModule.id == module_id).first()
        if product_module is None:
           return [] 
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

        new_product_master_price = ProductMasterPrice(
        product_master_id=new_product_master.id,  # Use the ID of the newly inserted product
        base_price=0.0,
        additional_price_per_user=0.0,
        gst_rate = 0.0,
        cess_rate = 0.0,
        created_on= datetime.utcnow(),
        created_by = user_id,
        effective_from_date= date.today(),
        effective_to_date = None
        )
        db.add(new_product_master_price)
        db.commit()
        db.refresh(new_product_master_price)

        return new_product_master



def update_product_master(db: Session,  request: ProductMasterSchema, product_master_id: int, user_id: int):    

        # Update operation
        product_master = db.query(ProductMaster).filter(ProductMaster.id == product_master_id).first()
        if product_master is None:
           return [] 
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



def get_product_master_by_id(db: Session, id: int):
    stmt = (
        select(
            ProductMaster.id,
            ProductMaster.category_id,
            ProductCategory.category_name,
            ProductMaster.group_id,
            ProductGroup.group_name,
            ProductMaster.product_code,
            ProductMaster.product_name,
            ProductMaster.product_description_main,
            ProductMaster.product_description_sub,
            ProductMaster.has_module,
            ProductMaster.min_no_of_users,
            ProductMaster.max_no_of_users,
            ProductMaster.has_instalments,
            ProductMaster.is_deleted
        )
        .join(ProductCategory, ProductMaster.category_id == ProductCategory.id)
        .join(ProductGroup, ProductMaster.group_id == ProductGroup.id)
        .where(ProductMaster.id == id)
        .where(ProductMaster.is_deleted == 'no')
    )
    
    result = db.execute(stmt).first()
    if result:
       product = ProductMasterSchemaResponse(**result._asdict())
       return product
    else:
       return None




def get_product_master_by_code(db: Session,code: str):
        
        return db.query(ProductMaster).filter(ProductMaster.product_code== code).all()



def delete_product_master(db: Session, product_id: int,action_type:str,deleted_by: int):
    existing_product = db.query(ProductMaster).filter(ProductMaster.id == product_id).first()

    if existing_product is None:
       return [] 
    if(action_type== 'DELETE'):

            existing_product.is_deleted = 'yes'
            existing_product.deleted_by = deleted_by
            existing_product.deleted_on = datetime.utcnow()
            
            # Mark related installment details as deleted
            db.query(ProductModule).filter(ProductModule.product_master_id == product_id).update({
                ProductModule.is_deleted: 'yes',
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
           return []
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
       return [] 

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
       return [] 
    if(action_type== 'DELETE'):

        existing_product.is_deleted = 'yes'
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
       return [] 
    
    existing_video.is_deleted = 'yes'
    existing_video.deleted_by = deleted_by
    existing_video.deleted_on = datetime.utcnow()
   
    db.commit()
    return {
        "message": "Product video marked as deleted successfully",
    }



# =========================================================================

#  PRODUCT FEATURES SECTION 
# ==========================================================================

def save_product_features(db: Session,  request: ProductFeaturesSchema, product_feature_id: int):

    if product_feature_id == 0:
        # Add operation
        product_feature_data_dict = request.dict()
        new_product_feature = ProductFeatures(**product_feature_data_dict)
        db.add(new_product_feature)
        db.commit()
        db.refresh(new_product_feature)
        return new_product_feature
    else:
        # Update operation
        product_feature = db.query(ProductFeatures).filter(ProductFeatures.id == product_feature_id).first()
        
        if product_feature is None:
           return []
        product_feature_data_dict = request.dict(exclude_unset=True)
        for key, value in product_feature_data_dict.items():
            setattr(product_feature, key, value)
                
        db.commit()
        db.refresh(product_feature)
        return product_feature



def get_product_feature_by_id(db: Session, product_master_id: int, product_feature_id: Optional[int] = None):
    
    query = db.query(ProductFeatures).filter(
        ProductFeatures.product_master_id == product_master_id,
        ProductFeatures.is_deleted == 'no'
    )
    
    if product_feature_id:
        query = query.filter(ProductFeatures.id == product_feature_id)
        feature_data = query.first()
        if feature_data:
            return [feature_data]  # Return as a list containing a single item
        else:
            return []
    else:
        feature_data = query.all()
        return feature_data



def delete_product_feature(db: Session, feature_id: int):
    existing_feature = db.query(ProductFeatures).filter(ProductFeatures.id == feature_id).first()

    if existing_feature is None:
       return [] 
    
    existing_feature.is_deleted = 'yes'
    
    db.commit()
    return {
        "message": "Product Feature marked as deleted successfully",
    }


####################################################################################################################


def save_product_trial_features(db: Session,  request: ProductTrialFeatureSchema, product_trial_feature_id: int):

    if product_trial_feature_id == 0:
        # Add operation
        product_trial_feature_data_dict = request.dict()
        new_product_trial_feature = ProductTrialFeatures(**product_trial_feature_data_dict)
        db.add(new_product_trial_feature)
        db.commit()
        db.refresh(new_product_trial_feature)
        return new_product_trial_feature
    else:
        # Update operation
        product_trial_feature = db.query(ProductTrialFeatures).filter(ProductTrialFeatures.id == product_trial_feature_id).first()
        
        if product_trial_feature is None:
           return []
        
        product_trial_feature_data_dict = request.dict(exclude_unset=True)
        for key, value in product_trial_feature_data_dict.items():
            setattr(product_trial_feature, key, value)
                
        db.commit()
        db.refresh(product_trial_feature)
        return product_trial_feature




def get_product_trial_features(db: Session, product_master_id: int, trial_features_id: Optional[int] = None):
    
    query = db.query(ProductTrialFeatures).filter(
        ProductTrialFeatures.product_master_id == product_master_id,
        ProductTrialFeatures.is_deleted == 'no'
    )
    
    if trial_features_id:
        query = query.filter(ProductTrialFeatures.id == trial_features_id)
        trial_feature_data = query.first()
        if trial_feature_data:
           return [trial_feature_data]  # Return as a list
        else:
           return []
    else:
        trial_feature_data = query.all()
        return trial_feature_data


#################################################################################################################   

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
            # id=detail.id,
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


# def delete_installment_master(db: Session, id: int, deleted_by: int):
#     existing_installment_master = db.query(InstallmentMaster).filter(InstallmentMaster.id == id).first()

#     if existing_installment_master is None:
#        return []

#     # Mark the installment master as deleted
#     existing_installment_master.is_deleted = 'yes'
#     existing_installment_master.deleted_by = deleted_by
#     existing_installment_master.deleted_on = datetime.utcnow()

#     # Mark related installment details as deleted
#     db.query(InstallmentDetails).filter(InstallmentDetails.installment_master_id == id).update({
#         InstallmentDetails.is_deleted: 'yes',
#         InstallmentDetails.deleted_by: deleted_by,
#         InstallmentDetails.deleted_on: datetime.utcnow()
#     }, synchronize_session=False)

#     db.commit()
#     return {
#         "message": "Installment master and related details deleted successfully",
#     }



#=======================================================================================

# def save_price_list_product_module(db: Session, request: PriceListProductModule, price_list_id: int,user_id: int):
     
#     if price_list_id == 0:
#         # Add operation
#         price_list_data_dict = request.dict()
#         price_list_data_dict["created_on"] = datetime.utcnow()
#         price_list_data_dict["created_by"] = user_id
#         # price_list_data_dict["effective_from_date"] = datetime.utcnow()
#         new_price_list = PriceListProductModule(**price_list_data_dict)
#         db.add(new_price_list)
#         db.commit()
#         db.refresh(new_price_list)
#         return new_price_list
    
#     else:
#         # Update operation
#         price_list = db.query(PriceListProductModule).filter(PriceListProductModule .id == price_list_id).first()
#         if price_list is None:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price List not found")
#         price_list_data_dict = request.dict(exclude_unset=True)
#         for key, value in price_list_data_dict.items():
#             setattr(price_list, key, value)
#         price_list.modified_by = user_id
#         price_list.modified_on = datetime.utcnow()
        
#         db.commit()
#         db.refresh(price_list)
#         return price_list
    
#================================================================================



def get_price_list_master(db:Session,product_id: Optional[int]=None,product_price_id: Optional[int]=None, product_name: Optional[str]= None,requested_date: Optional[date]=None, operator : Optional[Operator] = None):
    # query = db.query(ViewProductMasterPrice)
    query = db.query(ViewProductMasterPrice).filter(ViewProductMasterPrice.is_deleted == 'no')

    if requested_date is None : 
         requested_date = date.today() 
    if product_id:
        query = query.filter(ViewProductMasterPrice.product_master_id == product_id)
    
    if product_name:
         query = query.filter(ViewProductMasterPrice.product_master_product_name.ilike(f"%{product_name}%"))
     
    if operator:
        if product_price_id:
            query = query.filter(ViewProductMasterPrice.product_master_price_id == product_price_id)
        else:
             
            if operator == Operator.EQUAL_TO:
                query = query.filter(
                    ViewProductMasterPrice.effective_from_date <= requested_date,
                    or_(
                        ViewProductMasterPrice.effective_to_date >= requested_date,
                        ViewProductMasterPrice.effective_to_date == None
                    )
                )
            elif operator == Operator.GREATER_THAN:
                query = query.filter(ViewProductMasterPrice.effective_from_date > requested_date)
            elif operator == Operator.LESS_THAN :
                query = query.filter(ViewProductMasterPrice.effective_to_date < requested_date)
            
    
    price_list_results = query.all()
    print(query.statement.compile(compile_kwargs={"literal_binds": True}))
    return price_list_results


# def delete_price_list_master(db:Session,price_i).fid:int):
#      existing_price= db.query(ProductMasterPricelter(ProductMasterPrice.id == price_id).first()

# def set_new_price(db:Session, price_data:ProductMasterPriceSchema,user_id: int,record_actions:RecordActionType,price_id:Optional[int]):
        
#        price_list_data_dict = price_data.dict(exclude_unset=True)# Ensure effective_to_date is properly handled
#        if 'effective_to_date' in price_list_data_dict:
#                 if price_list_data_dict['effective_to_date'] == '':
#                     price_list_data_dict['effective_to_date'] = None
#        product_master_id = price_list_data_dict.get("product_master_id")
       
#        price_list = db.query(ProductMasterPrice).filter(ProductMasterPrice .product_master_id == product_master_id).first()
#        if price_list and price_list.base_price == 0:
#             price_id= price_list.id
#             record_actions = RecordActionType.UPDATE_ONLY
#     #    if price_list.effective_to_date >= price_list_data_dict['effective_from_date']:
#     #          print("effective_to_date", price_list.effective_to_date)
#     #          price_list_data_dict['effective_from_date']= price_list.effective_to_date+1
#        if record_actions==RecordActionType.UPDATE_ONLY:
#             price_list = db.query(ProductMasterPrice).filter(ProductMasterPrice .id == price_id).first()
#             if price_list is None:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Price List not found")
           
#             for key, value in price_list_data_dict.items():
#                 setattr(price_list, key, value)
#             price_list.modified_by = user_id
#             price_list.modified_on = datetime.utcnow()
            
#             db.commit()
#             db.refresh(price_list)
#             return price_list

#        else:
       
#         # price_list_data_dict = price_data.dict()
#         product_master_id = price_list_data_dict.get("product_master_id")
#         existing_price_list = db.query(ProductMasterPrice).filter(
#                     ProductMasterPrice.product_master_id == product_master_id).order_by(
#                     ProductMasterPrice.effective_from_date.desc()).first()
#         # if not existing_price_list:
#         price_list_data_dict["created_on"] = datetime.utcnow()
#         price_list_data_dict["created_by"] = user_id
#         new_price_list = ProductMasterPrice(**price_list_data_dict)
#         if existing_price_list is not None:
#             existing_price_list.modified_on = datetime.utcnow()
#             existing_price_list.modified_by = user_id
#             existing_price_list.effective_to_date = new_price_list.effective_from_date
#         db.add(new_price_list)
#         db.commit()
#         db.refresh(new_price_list)
#         return new_price_list
     


def set_new_price(
    db: Session,
    price_data: ProductMasterPriceSchema,
    user_id: int,
    record_actions: RecordActionType,
    price_id: Optional[int]
):
    # Ensure effective_to_date is properly handled
    price_list_data_dict = price_data.dict(exclude_unset=True)
    if 'effective_to_date' in price_list_data_dict:
        if price_list_data_dict['effective_to_date'] == '':
            price_list_data_dict['effective_to_date'] = None

    product_master_id = price_list_data_dict.get("product_master_id")

    # Check if the product is deleted
    product = db.query(ProductMaster).filter(ProductMaster.id == product_master_id).first()
    if product and product.is_deleted == 'yes':
       return {"message": "Cannot set price for a deleted product"} 
    
    # Check if there is an existing price list for the product
    price_list = db.query(ProductMasterPrice).filter(ProductMasterPrice.product_master_id == product_master_id).first()
    if price_list and price_list.base_price == 0:
        price_id = price_list.id
        record_actions = RecordActionType.UPDATE_ONLY

    if record_actions == RecordActionType.UPDATE_ONLY:
        price_list = db.query(ProductMasterPrice).filter(ProductMasterPrice.id == price_id).first()
        if price_list is None:
           return []

        for key, value in price_list_data_dict.items():
            setattr(price_list, key, value)
        price_list.modified_by = user_id
        price_list.modified_on = datetime.utcnow()

        db.commit()
        db.refresh(price_list)
        return price_list
    else:
        # Create a new price list entry
        existing_price_list = db.query(ProductMasterPrice).filter(
            ProductMasterPrice.product_master_id == product_master_id,
            ProductMasterPrice.is_deleted == 'no'
        ).order_by(ProductMasterPrice.effective_from_date.desc()).first()

        price_list_data_dict["created_on"] = datetime.utcnow()
        price_list_data_dict["created_by"] = user_id
        new_price_list = ProductMasterPrice(**price_list_data_dict)

        if existing_price_list is not None:
            existing_price_list.modified_on = datetime.utcnow()
            existing_price_list.modified_by = user_id
            existing_price_list.effective_to_date = new_price_list.effective_from_date - timedelta(days=1)

        db.add(new_price_list)
        db.commit()
        db.refresh(new_price_list)
        return new_price_list



def get_price_list_module(db:Session,product_id: Optional[int]=None,
                           module_name: Optional[str]=None,module_id: Optional[int]= None,product_module_price_id:Optional[int]=None,
                           product_master_price_id: Optional[int]=None,requested_date: Optional[date]=None, 
                           operator : Optional[Operator] = None):
    # query = db.query(ViewProductModulePrice)
    query = db.query(ViewProductModulePrice).filter(ViewProductModulePrice.is_deleted == 'no')

    if requested_date is None : 
       requested_date = date.today() 

    if product_id:
        query = query.filter(ViewProductModulePrice.product_master_id == product_id)
    
    if module_id:
         query = query.filter(ViewProductModulePrice.module_id == module_id)
    if product_master_price_id:
         query = query.filter(ViewProductModulePrice.product_master_price_id == product_master_price_id)     
    # if module_price_id:
    #      query = query.filter(ViewProductModulePrice.product_module_price_id == module_price_id)
     
    if module_name:
         query = query.filter(ViewProductModulePrice.module_name.ilike(f"%{module_name}%"))
     
    if operator:
        if product_module_price_id:
         query = query.filter(ViewProductModulePrice.product_modules_price_id == product_module_price_id)
        else:
             
            if operator == Operator.EQUAL_TO:
                query = query.filter(
                    ViewProductModulePrice.effective_from_date <= requested_date,
                    or_(
                        ViewProductModulePrice.effective_to_date >= requested_date,
                        ViewProductModulePrice.effective_to_date == None
                    )
                )
            elif operator == Operator.GREATER_THAN:
                query = query.filter(ViewProductModulePrice.effective_from_date > requested_date)
            elif operator == Operator.LESS_THAN :
                query = query.filter(ViewProductModulePrice.effective_to_date < requested_date )
        
        # Optional: Print the SQL query and its parameters for debugging
    # print(str(query.statement))
    print(str(query.statement))
    print(query.params)
    
    price_list_results = query.all()
    return price_list_results
   

  
def set_new_module_price(db:Session, price_data:ProductModulePriceSchema,user_id: int,record_actions:RecordActionType,price_id:Optional[int]):
    
       price_list_data_dict = price_data.dict(exclude_unset=True)# Ensure effective_to_date is properly handled
       if 'effective_to_date' in price_list_data_dict:
                if price_list_data_dict['effective_to_date'] == '':
                    price_list_data_dict['effective_to_date'] = None
       module_id = price_list_data_dict.get("module_id")
       existing_price_list = db.query(ProductModulePrice).filter(
                    ProductModulePrice.module_id == module_id).order_by(
                    ProductModulePrice.effective_from_date.desc()).first()
       if existing_price_list.module_base_price == 0:
            price_id = existing_price_list.id
            record_actions= RecordActionType.UPDATE_ONLY
       print("existing_price_list :", existing_price_list.module_base_price)
       if record_actions==RecordActionType.UPDATE_ONLY:
            price_list = db.query(ProductModulePrice).filter(ProductModulePrice .id == price_id).first()
            if price_list is None:
               return [] 
            # price_list_data_dict = price_data.dict(exclude_unset=True)# Ensure effective_to_date is properly handled
            # if 'effective_to_date' in price_list_data_dict:
            #     if price_list_data_dict['effective_to_date'] == '':
            #         price_list_data_dict['effective_to_date'] = None

            for key, value in price_list_data_dict.items():
                setattr(price_list, key, value)
            price_list.modified_by = user_id
            price_list.modified_on = datetime.utcnow()
            
            db.commit()
            db.refresh(price_list)
            return price_list

       else:
        # price_list_data_dict = price_data.dict()
        product_master_price_id = price_list_data_dict.get("product_master_price_id")
        module_id = price_list_data_dict.get("module_id")
        existing_price_list = db.query(ProductModulePrice).filter(
                    ProductModulePrice.product_master_price_id == product_master_price_id,
                    ProductModulePrice.module_id == module_id,
                    ProductModulePrice.is_deleted == 'no'
                    ).order_by(
                    ProductModulePrice.effective_from_date.desc()).first()
        # if not existing_price_list:
        price_list_data_dict["created_on"] = datetime.utcnow()
        price_list_data_dict["created_by"] = user_id
        new_price_list = ProductModulePrice(**price_list_data_dict)
        if existing_price_list is not None:
            existing_price_list.modified_on = datetime.utcnow()
            existing_price_list.modified_by = user_id
            existing_price_list.effective_to_date = new_price_list.effective_from_date - timedelta(days=1)
        db.add(new_price_list)
        db.commit()
        db.refresh(new_price_list)
        return new_price_list



def save_product_rating(db: Session, request: ProductRating, id: int,user_id: int):
     
    if id == 0:
        # Add operation
        product_rating_data_dict = request.dict()
        product_rating_data_dict["created_on"] = datetime.utcnow()
        product_rating_data_dict["user_id"] = user_id
        # price_list_data_dict["effective_from_date"] = datetime.utcnow()
        new_product_rating = ProductRating(**product_rating_data_dict)
        db.add(new_product_rating)
        db.commit()
        db.refresh(new_product_rating)
        return new_product_rating
    else:
        # Update operation
        product_rating = db.query(ProductRating).filter(ProductRating .id == id).first()
        if product_rating is None:
           return [] 
        product_rating_data_dict = request.dict(exclude_unset=True)
        for key, value in product_rating_data_dict.items():
            setattr(product_rating, key, value)
        product_rating.modified_by = user_id
        product_rating.modified_on = datetime.utcnow()
        
        db.commit()
        db.refresh(product_rating)
        return product_rating
   
   
     
def get_product_complete_details(product_id : Optional[int]=None, page: Optional[int] = None, page_size: Optional[int] = None, db: Session = Depends(get_db)):
    requested_date = datetime.today()
    requested_date = requested_date.date()

    product_ratings = [
    {"star": '1', "count": 0},
    {"star": '2', "count": 0},
    {"star": '3', "count": 0},
    {"star": '4', "count": 0},
    {"star": '5', "count": 0}
   ]
    # Fetch product master data
    product_master_query = db.query(ViewProductMasterPrice).filter(
         ViewProductMasterPrice.is_deleted =='no',
        ViewProductMasterPrice.effective_from_date <= requested_date,       
          or_(
               ViewProductMasterPrice.effective_to_date >= requested_date,
               ViewProductMasterPrice.effective_to_date == None
             )
          )
                   
    # Query for total rating count and average rating
    if product_id:
       
        discount_query = text(
            "SELECT product_master_id, offer_details_id, offer_name, offer_percentage, "
            "effective_from_date, effective_to_date "
            "FROM view_offer_details "
            "WHERE product_master_id = :product_id "
            "AND ((effective_from_date <= :requested_date AND effective_to_date >= :requested_date OR effective_to_date IS NULL) "
            "AND offer_details_is_deleted = 'no')"
        )
       
        discount_details = db.execute(discount_query, {'product_id': product_id, 'requested_date':requested_date}).fetchall()
        # discount_details = db.execute(discount_query, {'product_id': product_id}).fetchall()

        total_query = text(
            "SELECT product_master_id, COUNT(product_master_id) AS total_rating_count, "
            "AVG(rating) AS average_rating, "
            "SUM(CASE WHEN comment != '' THEN 1 ELSE 0 END) AS total_review_count "
            "FROM product_rating "
            "WHERE product_master_id = :product_id  "
            "GROUP BY product_master_id"
        )
        total_results = db.execute(total_query, {'product_id': product_id}).fetchall()
    else:
        discount_query = text(
            "SELECT product_master_id, offer_details_id, offer_name, offer_percentage, "
            "effective_from_date, effective_to_date "
            "FROM view_offer_details "
            "WHERE (effective_from_date <= :requested_date AND effective_to_date >= :requested_date OR effective_to_date IS NULL) "
            "AND offer_details_is_deleted = 'no'"
        )
        discount_details = db.execute(discount_query, {'requested_date': requested_date}).fetchall()
        # discount_details = db.execute(discount_query).fetchall()
        
        total_query = text(
           
            "SELECT product_master_id, COUNT(product_master_id) AS total_rating_count, AVG(rating) AS average_rating ,SUM(CASE WHEN comment != '' THEN 1 ELSE 0 END) AS total_review_count  "
            "FROM product_rating "
            "GROUP BY product_master_id"
            
        )
        total_results = db.execute(total_query).fetchall()
    # discount_data = {}
    # for discount in discount_details:
    #     if discount.offer_amount:
    #         discount_percentage = discount_details.offer_amount*
    #         print("discount amount", discount_percentage)
    total_ratings_map = {}
    for row in total_results:
        total_ratings_map[row[0]] = {
              "total_rating_count": row[1],
            "average_rating"      : row[2],
            "total_review_count"  : row[3]            
        }

    discount_data ={}
    for row in discount_details:
        discount_data[row[0]] = {
            # "product_master_id" : row[0],
            "offer_name"     : row[2],
            # "offer_amount" : row[4],
            "offer_percentage":row[3]
        }
    # print("discount_data ------------------",discount_data)
    if product_id:
        individual_query = text(
            "SELECT product_master_id, rating, COUNT(rating) AS rating_count "
            "FROM product_rating "
            "WHERE product_master_id = :product_id "
            "GROUP BY product_master_id, rating"
        )
        individual_results = db.execute(individual_query, {'product_id': product_id}).fetchall()
    
    else:
        individual_query = text(
            "SELECT product_master_id, rating, COUNT(rating) AS rating_count "
            "FROM product_rating "
            "GROUP BY product_master_id, rating"
        )
        individual_results = db.execute(individual_query).fetchall()
    for row in individual_results:
            rating = row[1]
            count = row[2]
            if rating == 1:
                product_ratings[0]["count"] = count
            elif rating == 2:
                product_ratings[1]["count"] = count
            elif rating == 3:
                product_ratings[2]["count"] = count
            elif rating == 4:
                product_ratings[3]["count"] = count
            elif rating == 5:
                product_ratings[4]["count"] = count

       # print(product_master_query.statement.compile(compile_kwargs={"literal_binds": True}))
    
    if product_id:
        product_master_query = product_master_query.filter(
            ViewProductMasterPrice.product_master_id == product_id,
        )

        # if page is not None or page_size is not None:
        #    return {"message": "page and page size is not required when product master id is given"}
        
        product_master_data = product_master_query.all()
        if not  product_master_data:
          return []
        
        product_master_image_filename= f"{product_id}.jpg"
        # image_path = os.path.join(UPLOAD_DIR_MASTER_IMAGE_VIDEO, product_master_image_filename)
        # image_path = f"{BASE_URL}/uploads/product_master_image_video/{product_master_image_filename}"
        image_path = f"{BASE_URL}/product/save_product_master/{product_master_image_filename}"

        # if os.path.exists(image_path):
        #     image_path = f"{BASE_URL}/product/save_product_master/{product_master_image_filename}"
            # return FileResponse(image_path)
        # else:
        #     image_path = ""
        response = []
        for product_data in product_master_data:
            product_id = product_data.product_master_id
            # discount_data= {}
            # for discount in discount_details:
            discount = discount_data.get(product_id)
            discount_amount = 0
            discount_percentage = 0
            discount_name = ""
            
            if discount: 
                # if discount['offer_amount']:
                #         discount_percentage = (discount['offer_amount']/product_data.price)*100
                #         discount_amount     = discount['offer_amount']
                #         discount_name       =  discount['offer_name']
                        # print("discount amount", discount_percentage)
                if discount['offer_percentage']:
                        discount_amount     = product_data.base_price*(discount['offer_percentage']/100)
                        discount_percentage = discount['offer_percentage']
                        discount_name       = discount['offer_name']
                discount_info = {
                        "discount_percentage" : discount_percentage,
                        "discount_amount"     : discount_amount,
                        "discounted_price"    : product_data.base_price - discount_amount,
                        "discount_name"       : discount_name
                    }
            price_details = None
            base_price = 0
            additional_price_per_user = 0
             
            total_rating_details = total_ratings_map.get(product_id,'')

            product_master_image_filename= f"{product_id}.jpg"

            category_id=product_data.product_category_category_id
            category_query = text(
            "SELECT category_name " 
            "FROM product_category "
            "WHERE id = :category_id "         
            )
        
            # Execute the query with parameters
            params = {'category_id': category_id}
        
            category_name = db.execute(category_query, params).first()
            # field_name = 'category_name' 
            # category_name = get_info(field_name,ProductCategory,product_data.category_id)

            group_id=product_data.product_group_id
            group_query = text(
            "SELECT group_name " 
            "FROM product_group "
            "WHERE id = :group_id "         
             )
        
            # Execute the query with parameters
            params = {'group_id': group_id}
        
            group_name = db.execute(group_query, params).first()
            
            prod_master_query = text(
                "SELECT has_instalments,min_no_of_users,max_no_of_users,is_deleted "
                "FROM product_master "
                "WHERE id = :product_id"
            )
            params = {'product_id': product_id}
            master_det = db.execute(prod_master_query, params).first()

            has_instalments = master_det.has_instalments if master_det else None
            min_no_of_users = master_det.min_no_of_users if master_det else None
            max_no_of_users = master_det.max_no_of_users if master_det else None
            # is_deleted = master_det.is_deleted if master_det else None
            
            # Fetch product features
            feature_query = text(
              "SELECT feature "
              "FROM product_features "
              "WHERE product_master_id = :product_id AND is_deleted = 'no'"
              )
            params = {'product_id': product_id}
            product_features = db.execute(feature_query, params).fetchall()

            features = [{"feature_name": feature.feature} for feature in product_features]
           
            base_price = product_data.base_price
            additional_price_per_user = product_data.additional_price_per_user
                        
            price_details = {
            "base_price"               : base_price,
            "additional_price_per_user": additional_price_per_user
            }
           
            response_item={
                "product_master_id"      : product_data.product_master_id,
                "product_master_price_id": product_data.product_master_price_id,
                "product_name"           : product_data.product_master_product_name,
                "product_code"           : product_data.product_master_product_code,
                "category_id"            : category_id,
                "category_name"          : category_name[0],
                "group_id"               : group_id,
                "group_name"             : group_name,
                "image_url"              : image_path,                
                # "price"        : product_data.price,
                # "inclusive_of_taxes": True,
                # "emi_details"       : "EMI starts at ₹3,456. No Cost EMI available",
                # "emi_options_url"   : "https://example.com/emi-options",
                "description"            : {
                            "main": product_data.product_description_main,
                            "sub": product_data.product_description_sub
                             },                
                "has_module"             : product_data.product_master_has_module,
                "minimum_user"           : min_no_of_users,
                "maximum_user"           : max_no_of_users,
                "has_instalments"        : has_instalments,
                # "is_deleted"       : is_deleted,
                "price_details"          : price_details,
                 "features"              : features,
                # "total_rating": total_ratings_map.get(product_id,''),
                # "ratings"           :  product_ratings
            }
            if product_data.product_master_has_module == 'yes':
               module_query = text(
                 "SELECT pm.id, pm.module_name, pm.module_description,pm.is_default, pmp.module_base_price, pmp.additional_price_per_user "
                 "FROM product_module pm "
                 "JOIN view_product_modules_price pmp ON pm.product_master_id = pmp.product_master_id AND pm.id = pmp.module_id "
                 "WHERE pm.product_master_id = :product_id AND pm.is_deleted = 'no'"
                )
               params = {'product_id': product_id}
               product_modules = db.execute(module_query, params).fetchall()

               modules = []
               for module in product_modules:
                   module_image_filename = f"{module.id}.jpg"
                   module_image_path = f"{BASE_URL}/product/save_product_module/{module_image_filename}"
        
                   module_info = {
                         "module_id"                : module.id,
                         "module_name"              : module.module_name,
                         "module_description"       : module.module_description,
                         "is_default"               : module.is_default,
                         "module_base_price"        : module.module_base_price,
                         "additional_price_per_user": module.additional_price_per_user,
                         "module_image_url"         : module_image_path
                   }
                   modules.append(module_info)

               response_item["modules"] = modules
                
            if total_rating_details:
              response_item["total_rating"] = total_rating_details
            # if product_ratings:
            response_item["ratings"] = product_ratings

            if discount:
              response_item["discount"] = discount_info

            # Append the response item to the response list
            response.append(response_item)
        return response
    else:
        # Calculate total records
        total_records = product_master_query.count()
    
        # #apply pagination
        if page and page_size:
           product_master_data = product_master_query.offset((page - 1) * page_size).limit(page_size).all()
        else:
           product_master_data = product_master_query.all()
        if not product_master_data:
           return []
    
        # Calculate total pages
        total_pages = 0
        if page_size:
           total_pages = (total_records + page_size - 1)

        response = {
            "pagination": {
                "total_records": total_records,
                "page"         : page,
                "page_size"    : page_size,
                "total_pages"  : total_pages
            },
            "products": []
          }
        
        for product_data in product_master_data:
           product_id = product_data.product_master_id
           product_master_image_filename= f"{product_id}.jpg"
           # image_path = os.path.join(UPLOAD_DIR_MASTER_IMAGE_VIDEO, product_master_image_filename)
           # image_path = f"{BASE_URL}/uploads/product_master_image_videos/{product_master_image_filename}"
           image_path = f"{BASE_URL}/product/save_product_master/{product_master_image_filename}"

           # if os.path.exists(image_path):
           #      image_path =  f"{BASE_URL}/uploads/product_master_image_videos/{product_master_image_filename}"
           # else:
           #     image_path = ""
       
           discount = discount_data.get(product_id,[])
           discount_amount = 0
           discount_percentage = 0
           discount_info ={}
           if discount:
              # if discount['offer_amount']:
              #         discount_percentage = (discount['offer_amount']/product_data.price)*100
              #         discount_amount     = discount['offer_amount']
                    # print("discount amount", discount_percentage)
              if discount['offer_percentage']:
                 discount_amount     = product_data.base_price*(discount['offer_percentage']/100)
                 discount_percentage = discount['offer_percentage']
              discount_info = {
                        "discount_percentage" : discount_percentage,
                        "discount_amount"     : discount_amount,
                        "discounted_price"    : product_data.base_price - discount_amount,
                        "discount_name"       : discount['offer_name']
                    }
           price_details = None
           base_price = 0
           additional_price_per_user = 0
            
           total_rating_details = total_ratings_map.get(product_id,'') 
           # field_name = 'category_name' 
           # category_name = get_info(field_name,ProductCategory,product_data.category_id)
           category_id=product_data.product_category_category_id
           category_query = text(
            "SELECT category_name "
            "FROM product_category "
           
            "WHERE id = :category_id "         
            )
        
           # Execute the query with parameters
           params = {'category_id': category_id}
        
           category_name = db.execute(category_query, params).first()

           group_id=product_data.product_group_id
           group_query = text(
            "SELECT group_name " 
            "FROM product_group "
            "WHERE id = :group_id "         
           )
           # Execute the query with parameters
           params = {'group_id': group_id}
        
           group_name = db.execute(group_query, params).first()
           
           # Fetch product features
           feature_query = text(
              "SELECT feature "
              "FROM product_features "
              "WHERE product_master_id = :product_id AND is_deleted = 'no'"
              )
           params = {'product_id': product_id}
           product_features = db.execute(feature_query, params).fetchall()

           features = [{"feature_name": feature.feature} for feature in product_features]

           prod_master_query = text(
                "SELECT has_instalments,min_no_of_users,max_no_of_users,is_deleted "
                "FROM product_master "
                "WHERE id = :product_id"
            )
           params = {'product_id': product_id}
           master_det = db.execute(prod_master_query, params).first()

           has_instalments = master_det.has_instalments if master_det else None
           min_no_of_users = master_det.min_no_of_users if master_det else None
           max_no_of_users = master_det.max_no_of_users if master_det else None
           is_deleted      = master_det.is_deleted if master_det else None

           base_price = product_data.base_price
           additional_price_per_user = product_data.additional_price_per_user
                      
           price_details = {
            "base_price": base_price,
            "additional_price_per_user": additional_price_per_user
          }
                   
           response_item={
            "product_master_id"      : product_data.product_master_id,
            "product_master_price_id": product_data.product_master_price_id,
            "product_name"           : product_data.product_master_product_name,
            "product_code"           : product_data.product_master_product_code,
            "category_id"            : category_id,
            "category_name"          : category_name[0],
            "group_id"               : group_id,
            "group_name"             : group_name,
            "has_module"             : product_data.product_master_has_module,
            "minimum_user"           : min_no_of_users,
            "maximum_user"           : max_no_of_users,
            "has_instalments"        : has_instalments,
            "is_deleted"             : is_deleted,
            "image_url"              : image_path,
            "price_details"          : price_details,
            "features"               : features
            # "image_url":  f"{BASE_URL}/product/save_product_master/{product_master_image_filename}",
            # "offer_price"   : product_data.price,
            #"price": product_data.price,
            # "discount"      : discount_info  if discount_info else None,
            #"total_rating": total_ratings_map.get(product_id,''),
            
           }
           
           if total_rating_details:
             response_item["total_rating"]= total_rating_details
           if discount_info:
             response_item["discount"] = discount_info
        
           # Append the response item to the response list
           response["products"].append(response_item)
       
        return response

    

# def get_product_rating_comments(db: Session , product_id: Optional[int]=None)-> List[Dict[str, Any]]:
def get_product_rating_comments(db: Session, product_id: Optional[int] = None, limit: Optional[int] = None, page: Optional[int] = None, page_size: Optional[int] = None) -> List[Dict[str, Any]]:
    requested_date = datetime.today()
    requested_date = requested_date.date()
    # Query for product details
    if product_id:
        product_master_query = db.query(ViewProductMasterPrice).filter(
            ViewProductMasterPrice.is_deleted =='no',
            ViewProductMasterPrice.product_master_id == product_id,
            ViewProductMasterPrice.effective_from_date <= requested_date,
            or_(
                ViewProductMasterPrice.effective_to_date >= requested_date,
                ViewProductMasterPrice.effective_to_date == None
            )
        )
        
        # if page is not None or page_size is not None:
        #    return {"message": "page and page size is not required when product master id is given"} 

        product_master_data= product_master_query.all()

        if not product_master_data:
           return []

        # Initialize response list
        response = []

        # Iterate over product data
        for product in product_master_data:
            product_id = product.product_master_id

            # # Query for comments
            comments_query = text(
              "SELECT pr.id, pr.user_id, cr.first_name as user_name, pr.rating,pr.comment, pr.created_on as date_of_comment "
              "FROM product_rating pr "
              "JOIN customer_register cr ON pr.user_id = cr.id "
              "WHERE pr.product_master_id = :product_id AND pr.comment !=''"
              "ORDER BY pr.created_on DESC "
              + ("LIMIT :limit" if limit is not None else "")
            )
        
            # Execute the query with parameters
            params = {'product_id': product_id}
            if limit is not None:
               params['limit'] = limit
        
            comments_results = db.execute(comments_query, params).fetchall()
         
            comments = [
              { 
                "review_id"  : row.id,
                "user_id"    : row.user_id,
                "username"   : row.user_name,
                "rating"     : row.rating,
                "comment"    : row.comment,
                "review_date": row.date_of_comment.strftime("%Y-%m-%d"),
                # "reviewer_image": f"{BASE_URL}/customer/image/add_customer_profile_image/{row.user_id}.jpg" 
              }                 # if row.user_id else f"{BASE_URL}/uploads/customer_profile_photo/default.jpg"            }
              for row in comments_results
            ]

            # Append product details to response
            response.append({
               "product_master_id": product.product_master_id,
               "product_name": product.product_master_product_name,
               "reviews": comments
             })

        return response
    else:
        product_master_query = db.query(ViewProductMasterPrice).filter(
            ViewProductMasterPrice.is_deleted =='no',
            ViewProductMasterPrice.effective_from_date <= requested_date,
            or_(
                ViewProductMasterPrice.effective_to_date >= requested_date,
                ViewProductMasterPrice.effective_to_date == None
            )
        )
        # print(product_master_query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Calculate total records
        total_records = product_master_query.count()
    
        # #apply pagination
        if page and page_size:
           product_master_data = product_master_query.offset((page - 1) * page_size).limit(page_size).all()
        else:
           product_master_data = product_master_query.all()
        if not product_master_data:
           return []
        
        # Calculate total pages
        total_pages = 0
        if page_size:
           total_pages = (total_records + page_size - 1)

        # Initialize response list
        response = []

        # Iterate over product data
        for product in product_master_data:
            product_id = product.product_master_id

            # # Query for comments
            comments_query = text(
               "SELECT pr.id, pr.user_id, cr.first_name as user_name, pr.rating,pr.comment, pr.created_on as date_of_comment "
               "FROM product_rating pr "
               "JOIN customer_register cr ON pr.user_id = cr.id "
               "WHERE pr.product_master_id = :product_id AND pr.comment !=''"
               "ORDER BY pr.created_on DESC "
               + ("LIMIT :limit" if limit is not None else "")
            )
        
            # Execute the query with parameters
            params = {'product_id': product_id}
            if limit is not None:
               params['limit'] = limit
        
            comments_results = db.execute(comments_query, params).fetchall()
         
            comments = [
              {
                "review_id"  : row.id,  
                "user_id"    : row.user_id,
                "username"   : row.user_name,
                "rating"     : row.rating,
                "comment"    : row.comment,
                "review_date": row.date_of_comment.strftime("%Y-%m-%d"),
                # "reviewer_image": f"{BASE_URL}/customer/image/add_customer_profile_image/{row.user_id}.jpg" 
              }                         # if row.user_id else f"{BASE_URL}/uploads/customer_profile_photo/default.jpg"            }
               for row in comments_results
             ]

            # Append product details to response
            response.append({
               "total_records"    : total_records,
                "page"            : page,
                "page_size"       : page_size,
                "total_pages"     : total_pages, 
               "product_master_id": product.product_master_id,
               "product_name"     : product.product_master_product_name,
               "reviews"          : comments
               })

        return response
     


def get_all_offer_list(
                        db : Session,
                        category_id : Optional[int]=None,
                        offer_master_id : Optional[int]=None ,
                        operator : Optional[Status] = None 
                      ):
    try:
        if offer_master_id:
           offer = db.query(OfferMaster).filter(OfferMaster.id == offer_master_id,OfferMaster.is_deleted == 'no').first()  

           if offer is None:
              return []
           
           details_query = db.query(OfferDetails).join(
                            ProductMaster,
                            OfferDetails.product_master_id == ProductMaster.id
                        ).filter(
                            and_(
                                OfferDetails.offer_master_id == offer.id,
                                OfferDetails.is_deleted == 'no',
                                ProductMaster.is_deleted == 'no',
                                )
                        )
           
           details_data = details_query.all()

           details = [
                        OfferDetailsSchema(
                             id                = detail.id,
                             offer_master_id   = detail.offer_master_id,
                             product_master_id = detail.product_master_id,
                             is_deleted        = detail.is_deleted
                         ) for detail in details_data
                     ] 
          
           result = []
           
           result.append(
                         OfferMasterSchemaResponse(
                             id                  = offer.id,
                             offer_category_id   = offer.offer_category_id,
                             offer_name          = offer.offer_name,
                             offer_percentage    = offer.offer_percentage,
                             effective_from_date = offer.effective_from_date,
                             effective_to_date   = offer.effective_to_date,
                             is_deleted          = offer.is_deleted,
                             details             = details
                         )
                     )
           return result
        else:
            current_date = datetime.today()
            current_date = current_date.date()
            query = db.query(OfferMaster).filter(OfferMaster.is_deleted == 'no')
        
            if category_id:
              query = query.filter(OfferMaster.offer_category_id == category_id)
                         
            if operator:
               if operator == Status.CURRENT:
                  query = query.filter(
                    OfferMaster.effective_from_date <= current_date,
                    OfferMaster.effective_to_date >= current_date
                  )
               elif operator == Status.UPCOMMING:
                 query = query.filter(OfferMaster.effective_from_date > current_date)
               elif operator == Status.EXPIRED:
                 query = query.filter(OfferMaster.effective_to_date < current_date)
        
            offer_master_data = query.all()
           
            return offer_master_data
    except Exception as e:
        print("Error:", e)  # Print the exception message for debugging
        raise HTTPException(status_code=500, detail=str(e))
          


def save_offer_details(
    db: Session,
    id: int,
    data: SaveOfferDetailsRequest,
    user_id: int,
):
    # if action_type == RecordActionType.INSERT_ONLY and id != 0:
    #     raise HTTPException(status_code=400, detail="Invalid action: For INSERT_ONLY, id should be 0")
    # elif action_type == RecordActionType.UPDATE_ONLY and id <= 0:
    #     raise HTTPException(status_code=400, detail="Invalid action: For UPDATE_ONLY, id should be greater than 0")

    try:
        if id == 0:
            # for master_data in data.master:
           new_master_data = data.master.dict()
           new_master_data.update({
                    "created_by": user_id,
                    "created_on": datetime.utcnow()
             })
           new_master = OfferMaster(**new_master_data)
           db.add(new_master)
           db.flush()  # Ensure new_master.id is available for details
            # if apply_to == ApplyTo.SELECTED :    
           for detail_data in data.details:
               new_detail_data = detail_data.dict()
               product_master_id = new_detail_data.get("product_master_id")

               # Check if the product is deleted
               product = db.query(ProductMaster).filter(ProductMaster.id == product_master_id).first()
               if product and product.is_deleted == 'yes':
                  return {"message": "Cannot give offers for a deleted product"} 
                  #raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot give offers for a deleted product")

               new_detail_data.update({
                        "offer_master_id": new_master.id,
                        "created_by": user_id,
                        "created_on": datetime.utcnow()
                   })
               new_detail = OfferDetails(**new_detail_data)
               db.add(new_detail)
        else:
            existing_master = db.query(OfferMaster).filter(OfferMaster.id == id).first()
            if not existing_master:
               return []

            master_update_data = data.master.dict()
            for key, value in master_update_data.items():
                setattr(existing_master, key, value)
            existing_master.modified_by = user_id
            existing_master.modified_on = datetime.utcnow()
            
            existing_details = db.query(OfferDetails).filter(OfferDetails.offer_master_id == id).all()    
            for det in existing_details:
               det.is_deleted = 'yes'
               det.deleted_by = user_id
               det.deleted_on = datetime.utcnow()
            # if apply_to == ApplyTo.SELECTED :    
            
            for detail_data in data.details:
                new_detail_data = detail_data.dict()

                product_master_id = new_detail_data.get("product_master_id")

                # Check if the product is deleted
                product = db.query(ProductMaster).filter(ProductMaster.id == product_master_id).first()
                if product and product.is_deleted == 'yes':
                   return {"message": "Cannot give offers for a deleted product"}

                new_detail_data.update({
                        "offer_master_id": id,
                        "created_by": user_id,
                        "created_on": datetime.utcnow()
                 })
                new_detail = OfferDetails(**new_detail_data)
                db.add(new_detail)
        
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logger.error("IntegrityError: %s", str(e))
        if 'Duplicate entry' in str(e):
            raise HTTPException(status_code=400, detail="Duplicate entry detected.")
        else:
            raise e
    except OperationalError as e:
        db.rollback()
        logger.error("OperationalError: %s", str(e))
        raise HTTPException(status_code=500, detail="Database connection error.")
    except Exception as e:
        db.rollback()
        logger.error("Exception: %s", str(e))
        raise e



def delete_offer_master(db, offer_master_id,action_type,deleted_by):
    existing_offer = db.query(OfferMaster).filter(OfferMaster.id == offer_master_id).first()

    if existing_offer is None:
       return []
    if(action_type== 'DELETE'):

            existing_offer.is_deleted = 'yes'
            existing_offer.deleted_by = deleted_by
            existing_offer.deleted_on = datetime.utcnow()
            
            
            db.query(OfferDetails).filter(OfferDetails.offer_master_id == offer_master_id).update({
                OfferDetails.is_deleted: 'yes',                
                OfferDetails.deleted_by: deleted_by,
                OfferDetails.deleted_on: datetime.utcnow()
            }, synchronize_session=False)
        
            db.commit()

            return {
                "message": "Offer marked as deleted successfully",

            }
    if(action_type == 'UNDELETE'):
            existing_offer.is_deleted = 'no'
            existing_offer.deleted_by = None
            existing_offer.deleted_on = None
            db.commit()

            return {
                "message": "Offer marked as Undeleted successfully",
            }



# def delete_offer(db, offer_master_id,action_type,deleted_by,table):
#     if table =='Master':
#         existing_offer = db.query(OfferMaster).filter(OfferMaster.id == offer_master_id).first()
#     else:
#         existing_offer = db.query(OfferDetails).filter(OfferDetails.id == offer_master_id).first()
 
#     if existing_offer is None:
#         raise HTTPException(status_code=404, detail="Offer  not found")
#     if(action_type== 'DELETE'):

#             existing_offer.is_deleted = 'yes'
#             existing_offer.deleted_by = deleted_by
#             existing_offer.deleted_on = datetime.utcnow()
            
#             if table== 'Master':
#                 db.query(OfferDetails).filter(OfferDetails.offer_master_id == offer_master_id).update({
#                     OfferDetails.is_deleted: 'yes',                
#                     OfferDetails.deleted_by: deleted_by,
#                     OfferDetails.deleted_on: datetime.utcnow()
#                 }, synchronize_session=False)
        
#             db.commit()

#             return {
#                 "message": "Offer marked as deleted successfully",

#             }
#     if(action_type == 'UNDELETE'):
#             existing_offer.is_deleted = 'no'
#             existing_offer.deleted_by = None
#             existing_offer.deleted_on = None
#             db.commit()

#             return {
#                 "message": "Product marked as Undeleted successfully",

#             }


# def get_cart_details(
#           db: Session,
#           customer_id: Optional[int] = None,
#           product_master_id: Optional[int] = None,
#           saved_for_later : ActiveStatus = ActiveStatus.ALL
#         #   deleted_status : DeletedStatus = DeletedStatus.ALL

# ):
#     try:
#         query = db.query(CartDetails).filter(CartDetails.is_deleted == 'no')
        
#         if customer_id is not None:
#             query = query.filter(CartDetails.customer_id == customer_id)
            
#         if product_master_id is not None:
#             query = query.filter(CartDetails.product_master_id == product_master_id)
        
#         if saved_for_later ==  ActiveStatus.YES:
#             query = query.filter(CartDetails.saved_for_later== ActiveStatus.YES)
#         if saved_for_later == ActiveStatus.NO:
#             query = query.filter(CartDetails.saved_for_later == ActiveStatus.NO)

#         cart_item =  query.all() 
#         response = []
#         for item in cart_item:
#             print(item.product_master_id)

#             product_details = get_product_complete_details(item.product_master_id,db)
#             if product_details and isinstance(product_details, list) and 'error' not in product_details[0]:
#                  # Remove ratings and total rating details
#                 # print("product _details : ",product_details[0])
#                 product_details_list = [product_details]

#                 for product_details in product_details_list:
#                     if 'ratings' in product_details:
#                         print("Product Ratings: ", product_details['ratings'])
#                         del product_details['ratings']
#                     if 'total_rating' in product_details:
#                         print("Total Rating: ", product_details['total_rating'])
#                         del product_details['total_rating']
#                 print("product_details :",product_details['ratings'] )
#                 product_detail = product_details[0]  # Assuming only one product is returned
#                 cart_item_response = {
#                     "cart_id": item.id,
#                     "customer_id": item.customer_id,
#                     "saved_for_later": item.saved_for_later,
#                     "product_details": product_detail
#                 }
#                 response.append(cart_item_response)

#         return response
#     except Exception as e:
#         print("Error:", e)  # Print the exception message for debugging
#         raise HTTPException(status_code=500, detail=str(e))



def save_cart_details(db: Session , cart_data : CartDetailsSchema, action_type: RecordActionType, id: int):
    if action_type == RecordActionType.INSERT_ONLY and id != 0:
        raise HTTPException(status_code=400, detail="Invalid action: For INSERT_ONLY, id should be 0")
    elif action_type == RecordActionType.UPDATE_ONLY and id <= 0:
        raise HTTPException(status_code=400, detail="Invalid action: For UPDATE_ONLY, id should be greater than 0")

    try:
        if action_type == RecordActionType.INSERT_ONLY:
            for cart_details in cart_data:
                new_cart_details = cart_details.dict()
               
                new_cart = CartDetails(**new_cart_details)
                db.add(new_cart)
                db.commit()
                db.refresh(new_cart)
                # db.flush()  
                return new_cart
            
        elif action_type == RecordActionType.UPDATE_ONLY:
            existing_cart = db.query(CartDetails).filter(CartDetails.id == id).first()
            if not existing_cart:
                raise HTTPException(status_code=404, detail=" record not found")

            # Use the first item from data.master for update
            update_data = cart_data[0].dict()
            for key, value in update_data.items():
                setattr(existing_cart, key, value)
            
        db.commit()
        return update_data
    except IntegrityError as e:
        db.rollback()
        logger.error("IntegrityError: %s", str(e))
        if 'Duplicate entry' in str(e):
            raise HTTPException(status_code=400, detail="Duplicate entry detected.")
        else:
            raise e
    except OperationalError as e:
        db.rollback()
        logger.error("OperationalError: %s", str(e))
        raise HTTPException(status_code=500, detail="Database connection error.")
    except Exception as e:
        db.rollback()
        logger.error("Exception: %s", str(e))
        raise e



def get_cart_product_details_with_prices(
    db: Session,
    customer_id: Optional[int] = None,
    product_master_id: Optional[int] = None,
    saved_for_later: ActiveStatus = ActiveStatus.ALL
):
    try:
        query = db.query(CartDetails).filter(CartDetails.is_deleted == 'no')

        if customer_id is not None:
            query = query.filter(CartDetails.customer_id == customer_id)
            

        if product_master_id is not None:
            query = query.filter(CartDetails.product_master_id == product_master_id)

        if saved_for_later == ActiveStatus.ACTIVE:
            query = query.filter(CartDetails.saved_for_later == ActiveStatus.ACTIVE)
        if saved_for_later == ActiveStatus.NOT_ACTIVE:
            query = query.filter(CartDetails.saved_for_later == ActiveStatus.NOT_ACTIVE)

        cart_items = query.all()

        cart_item_responses = []
        total_price = 0.0
        total_discount_amount = 0.0

        for cart_item in cart_items:
            product_details_list = get_product_complete_details(product_id=cart_item.product_master_id, db=db)

            # Ensure product_details_list is a list
            if not isinstance(product_details_list, list):
                product_details_list = [product_details_list]

            for product_details in product_details_list:
                # Ensure product_details is a dictionary
                if isinstance(product_details, dict):
                    if 'ratings' in product_details:
                        del product_details['ratings']
                    if 'total_rating' in product_details:
                        del product_details['total_rating']
                    if 'description' in product_details:
                        del product_details['description']

                    # Accumulate price and discount
                    total_price += product_details.get('price', 0.0)
                    discount = product_details.get('discount', {})
                    total_discount_amount += discount.get('discount_amount', 0.0)

                    cart_item_response = {
                        "cart_id"        : cart_item.id,
                        "customer_id"    : cart_item.customer_id,
                        "saved_for_later": cart_item.saved_for_later,
                        "product_details": product_details,
                    }
                    cart_item_responses.append(cart_item_response)
        total_price_before_tax = total_price - total_discount_amount
        tax_rate = 0.18  # 18% tax rate
        tax_amount = total_price_before_tax * tax_rate
        final_price = total_price_before_tax + tax_amount
        price_item_response = {
             
                "total_price"          : total_price,
                "total_discount_amount": total_discount_amount,
                "tax_percentage"       : "18 %",
                "tax_amount"           : tax_amount,
                "final_price"          : final_price
            }
        
        if cart_item_responses:
           
            response = {
            "cart_details" : cart_item_responses,
            "price_details": price_item_response
        }
        else:
                response = {"message": "cart is empty"}

        return response

        # return response

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=str(e))



def save_coupon(db: Session , id: int, coupon_data: SaveCouponDetails, user_id: int):
     
    # if action_type == RecordActionType.INSERT_ONLY and id != 0:
    #     raise HTTPException(status_code=400, detail="Invalid action: For INSERT_ONLY, id should be 0")
    # elif action_type == RecordActionType.UPDATE_ONLY and id <= 0:
    #     raise HTTPException(status_code=400, detail="Invalid action: For UPDATE_ONLY, id should be greater than 0")

    try:
        if id == 0:
           new_coupon_details = coupon_data.master.dict()
           new_coupon_details["created_on"] = datetime.utcnow()
           new_coupon_details["created_by"] = user_id
           new_coupon = CouponMaster(**new_coupon_details)
           db.add(new_coupon)
           # db.commit()
           # db.refresh(new_coupon)
           # return new_coupon
           db.flush()  
           for detail_data in coupon_data.details:
               new_detail_data = detail_data.dict()

               product_master_id = new_detail_data.get("product_master_id")

               # Check if the product is deleted
               product = db.query(ProductMaster).filter(ProductMaster.id == product_master_id).first()
               if product and product.is_deleted == 'yes':
                  return {"message": "Cannot give coupon for a deleted product"}

               new_detail_data.update({
                        "coupon_master_id": new_coupon.id,
                        "created_by": user_id,
                        "created_on": datetime.utcnow()
                 })
               new_detail = CouponDetails(**new_detail_data)
               db.add(new_detail)
        else:
           existing_coupon = db.query(CouponMaster).filter(CouponMaster.id == id).first()
           if not existing_coupon:
             return []
            
           # Use the first item from coupon_data.master for update
           update_data = coupon_data.master.dict()
           for key, value in update_data.items():
              setattr(existing_coupon, key, value) 

           existing_details = db.query(CouponDetails).filter(CouponDetails.coupon_master_id == id).all()    
           for det in existing_details:
               det.is_deleted = 'yes'
               det.deleted_by = user_id
               det.deleted_on = datetime.utcnow()

           for detail_data in coupon_data.details:
               new_detail_data = detail_data.dict()
               product_master_id = new_detail_data.get("product_master_id")

               # Check if the product is deleted
               product = db.query(ProductMaster).filter(ProductMaster.id == product_master_id).first()
               if product and product.is_deleted == 'yes':
                  return {"message": "Cannot give coupon for a deleted product"}

               new_detail_data.update({
                  "coupon_master_id": id,
                  "created_by": user_id,
                  "created_on": datetime.utcnow()
                 })
               new_detail = CouponDetails(**new_detail_data)
               db.add(new_detail)
            
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logger.error("IntegrityError: %s", str(e))
        if 'Duplicate entry' in str(e):
            raise HTTPException(status_code=400, detail="Duplicate entry detected.")
        else:
            raise e
    except OperationalError as e:
        db.rollback()
        logger.error("OperationalError: %s", str(e))
        raise HTTPException(status_code=500, detail="Database connection error.")
    except Exception as e:
        db.rollback()
        logger.error("Exception: %s", str(e))
        raise e


     
def apply_coupon(db:Session , amount: float , coupon_code : str):
     tax_rate =18.0
     current_date = datetime.today()
     coupon_details = db.query(CouponMaster).filter(CouponMaster.coupon_code== coupon_code,
                                                    CouponMaster.effective_from_date <= current_date,
                                                    CouponMaster.effective_to_date >= current_date).first()
     if coupon_details:   
        if coupon_details.coupon_percentage:
            discount_amount = amount*(coupon_details.coupon_percentage/100)
        
        else:
            discount_amount =  coupon_details.coupon_amount
        net_price = amount-discount_amount
        tax_amount = net_price * (tax_rate / 100)
        final_price = net_price + tax_amount

        response = {
            "coupon_amount": discount_amount,
            "net_price": net_price,
            "tax_percentage" : "18 %",
            "tax_amount": tax_amount,
            "final_price": final_price
        }
     else:
        response = {
            "error": "Coupon not valid"
        }
    
     return response    



def get_all_coupon_list(
                        db : Session,
                        coupon_master_id : Optional[int]=None ,
                        operator : Optional[Status] = None 
                       ):
    try:
                        
        if coupon_master_id:
          coupon = db.query(CouponMaster).filter(CouponMaster.id == coupon_master_id,CouponMaster.is_deleted == 'no').first()  

          if coupon is None:
             return []  

          details_query = db.query(CouponDetails).join(
                            ProductMaster,
                            CouponDetails.product_master_id == ProductMaster.id
                        ).filter(
                        and_(
                            CouponDetails.coupon_master_id == coupon.id,
                            CouponDetails.is_deleted == 'no',
                            ProductMaster.is_deleted == 'no'
                          )
                        )
          details_data = details_query.all()

          details = [
                        CouponDetailsSchema(
                            id                = detail.id,
                            coupon_master_id  = detail.coupon_master_id,
                            product_master_id = detail.product_master_id,
                            is_deleted        = detail.is_deleted
                        ) for detail in details_data
                    ] 
          
          result = []
           
          result.append(
                        CouponMasterSchemaResponse(
                            id                  = coupon.id,
                            coupon_name         = coupon.coupon_name,
                            coupon_code         = coupon.coupon_code,
                            coupon_percentage   = coupon.coupon_percentage,
                            effective_from_date = coupon.effective_from_date,
                            effective_to_date   = coupon.effective_to_date,
                            is_deleted          = coupon.is_deleted,
                            details             = details
                        )
                    )
          return result
        else:
          current_date = datetime.today()
          current_date = current_date.date()
          query = db.query(CouponMaster).filter(CouponMaster.is_deleted == 'no')
        #   query = query.filter(CouponMaster.id == coupon_master_id)
        
          if operator:
            if operator == Status.CURRENT:
                query = query.filter(
                    CouponMaster.effective_from_date <= current_date,
                    CouponMaster.effective_to_date >= current_date
                )
            elif operator == Status.UPCOMMING:
                query = query.filter(CouponMaster.effective_from_date > current_date)
            elif operator == Status.EXPIRED:
                query = query.filter(CouponMaster.effective_to_date < current_date)
        
          coupon_master_data = query.all()
          
          return coupon_master_data
    except Exception as e:
        print("Error:", e)  # Print the exception message for debugging
        raise HTTPException(status_code=500, detail=str(e))



def delete_coupon_master(db, coupon_master_id,action_type,deleted_by):
    existing_coupon = db.query(CouponMaster).filter(CouponMaster.id == coupon_master_id).first()

    if existing_coupon is None:
      return []
    
    if(action_type== 'DELETE'):
       existing_coupon.is_deleted = 'yes'
       existing_coupon.deleted_by = deleted_by
       existing_coupon.deleted_on = datetime.utcnow()
            
            
       db.query(CouponDetails).filter(CouponDetails.coupon_master_id == coupon_master_id).update({
         CouponDetails.is_deleted: 'yes',                
         CouponDetails.deleted_by: deleted_by,
         CouponDetails.deleted_on: datetime.utcnow()
        }, synchronize_session=False)
        
       db.commit()
       return {
          "message": "Coupon marked as deleted successfully",
         }
    if(action_type == 'UNDELETE'):
        existing_coupon.is_deleted = 'no'
        existing_coupon.deleted_by = None
        existing_coupon.deleted_on = None
        db.commit()

        return {
                "message": "Coupon marked as Undeleted successfully",
            }     



def get_all_installments(
                        db : Session,
                        status : InstallmentStatus,
                        installment_master_id : Optional[int]=None,
                        installment_detail_id : Optional[int] = None,
                    ):
    if installment_master_id is None and installment_detail_id is None:
       query = db.query(InstallmentMaster)

       # Filter by status
       if InstallmentStatus:
          if status == InstallmentStatus.ACTIVE:
             query = query.filter(InstallmentMaster.is_active == 'yes')
          elif status == InstallmentStatus.INACTIVE:
             query = query.filter(InstallmentMaster.is_active == 'no')
    
       # Get the results
       installment_masters = query.all()

       if not installment_masters:
          return []
    
       result = []
       for master in installment_masters:
           master_details_query = db.query(InstallmentDetails).filter(InstallmentDetails.installment_master_id == master.id)
           master_details = master_details_query.all()
        
           details=[
                InstallmentDetailsForGet(
                    id                    = detail.id,
                    # installment_master_id = detail.installment_master_id,
                    installment_name      = detail.installment_name,
                    payment_rate          = detail.payment_rate,
                    due_date              = detail.due_date
                  )
                for detail in master_details
             ]
                 
           result.append(
                      InstallmentMasterForGet(
                      id                     = master.id,
                      number_of_installments = master.number_of_installments,
                      is_active              = master.is_active,
                      details                = details
                     )
             )   
       return result
    elif installment_master_id and installment_detail_id is None:
       query = db.query(InstallmentMaster).filter(InstallmentMaster.id == installment_master_id)

       # Filter by status
       if InstallmentStatus:
          if status == InstallmentStatus.ACTIVE:
             query = query.filter(InstallmentMaster.is_active == 'yes')
          elif status == InstallmentStatus.INACTIVE:
             query = query.filter(InstallmentMaster.is_active == 'no')

       # Get the results
       installment_master = query.all()

       if not installment_master:
          return []
    
       result = []
       for master in installment_master:
           details_query = db.query(InstallmentDetails).filter(
            InstallmentDetails.installment_master_id == master.id
           )
        
           master_details = details_query.all()

           details = [
            InstallmentDetailsForGet(
                id                    = detail.id,
                # installment_master_id = detail.installment_master_id,
                installment_name      = detail.installment_name,
                payment_rate          = detail.payment_rate,
                due_date              = detail.due_date,
              )
                for detail in master_details
             ]
                 
           result.append(
            InstallmentMasterForGet(
                id                     = master.id,
                number_of_installments = master.number_of_installments,
                is_active              = master.is_active,
                details                = details
              )
            )   
    
           return result           
    elif installment_master_id is None and installment_detail_id:
       query = db.query(InstallmentDetails).filter(InstallmentDetails.id == installment_detail_id)
       
       # Get the results
       installment_details = query.all()

       if not installment_details:
          return []

       details=[
                InstallmentDetailsResponse(
                    # id                    = detail.id,
                    installment_master_id = detail.installment_master_id,
                    installment_name      = detail.installment_name,
                    payment_rate          = detail.payment_rate,
                    due_date              = detail.due_date
                )
                for detail in installment_details
            ]
       return details
    elif installment_master_id and installment_detail_id:
       query = db.query(InstallmentMaster).filter(InstallmentMaster.id == installment_master_id)

       # Filter by status
       if InstallmentStatus:
          if status == InstallmentStatus.ACTIVE:
             query = query.filter(InstallmentMaster.is_active == 'yes')
          elif status == InstallmentStatus.INACTIVE:
             query = query.filter(InstallmentMaster.is_active == 'no') 
      
       result = []
       installment_masters = query.all()

    for master in installment_masters:
        details_query = db.query(InstallmentDetails).filter(
            InstallmentDetails.id == installment_detail_id,
            InstallmentDetails.installment_master_id == master.id  # Ensure details are linked to the master
        )
        
        master_details = details_query.all()

        details = [
            InstallmentDetailsForGet(
                id                    = detail.id,
                # installment_master_id = detail.installment_master_id,
                installment_name      = detail.installment_name,
                payment_rate          = detail.payment_rate,
                due_date              = detail.due_date
                )
            for detail in master_details
        ]
                 
        result.append(
            InstallmentMasterForGet(
                id                     = master.id,
                number_of_installments = master.number_of_installments,
                is_active              = master.is_active,
                details                = details
            )
        )
    
    return result



def update_installments(
    db : Session,
    request: UpdateInstallmentRequest,
    installment_status : InstallmentStatus,
    user_id: int,
    installment_master_id : int
   ):
    try:
       db_installment_master = db.query(InstallmentMaster).filter(InstallmentMaster.id == installment_master_id).first()
    
       for key, value in request.installment_master.dict().items():
           setattr(db_installment_master, key, value)
       db_installment_master.modified_by = user_id
       db_installment_master.modified_on = datetime.utcnow()

       # Update InstallmentDetails if provided
       if request.installment_details:
          for detail in request.installment_details:
              if detail.id:  # Ensure the ID is provided for the details to be updated
                 db_installment_detail = db.query(InstallmentDetails).filter(
                    InstallmentDetails.installment_master_id == installment_master_id,
                    InstallmentDetails.id == detail.id
                 ).first()
                 if db_installment_detail:
                    for key, value in detail.dict().items():
                        if key != 'id':  # Exclude the primary key field from being updated
                           setattr(db_installment_detail, key, value)
                 else:
                   raise ValueError(f"InstallmentDetails with id {detail.id} not found")

       db.commit()
       db.refresh(db_installment_master)
       return db_installment_master
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))



# def get_all_installments(
#     db: Session,
#     status: InstallmentStatus,
#     installment_master_id: Optional[int] = None,
#     installment_detail_id: Optional[int] = None,
# ):
#     # Start with base query for InstallmentMaster
#     query = db.query(InstallmentMaster).filter(InstallmentMaster.is_deleted == 'no')

#     # Apply status filter
#     if status == InstallmentStatus.ACTIVE:
#         query = query.filter(InstallmentMaster.is_active == 'yes')
#     elif status == InstallmentStatus.INACTIVE:
#         query = query.filter(InstallmentMaster.is_active == 'no')

#     # Handle cases based on provided parameters

#     # Case 1: Both `installment_master_id` and `installment_detail_id` are None
#     if installment_master_id is None and installment_detail_id is None:
#         # Fetch all InstallmentMaster records
#         installment_masters = query.all()

#     # Case 2: Only `installment_master_id` is provided
#     elif installment_master_id is not None and installment_detail_id is None:
#         # Filter by `installment_master_id`
#         query = query.filter(InstallmentMaster.id == installment_master_id)
#         # Fetch relevant InstallmentMaster records
#         installment_masters = query.all()

#     # Case 3: Only `installment_detail_id` is provided
#     elif installment_master_id is None and installment_detail_id is not None:
#         # Fetch all InstallmentMaster records first
#         installment_masters = query.all()
#         # For each InstallmentMaster, filter details by `installment_detail_id`
#         result = []
#         for master in installment_masters:
#             master_details_query = db.query(InstallmentDetails).filter(InstallmentDetails.installment_master_id == master.id)
#             master_details_query = master_details_query.filter(InstallmentDetails.id == installment_detail_id)
#             master_details = master_details_query.all()
#             details = [
#                 InstallmentDetailsForGet(
#                     id=detail.id,
#                     installment_master_id=detail.installment_master_id,
#                     installment_name=detail.installment_name,
#                     payment_rate=detail.payment_rate,
#                     due_date=detail.due_date,
#                     is_deleted=detail.is_deleted
#                 )
#                 for detail in master_details
#             ]
#             result.append(
#                 InstallmentMasterForGet(
#                     id=master.id,
#                     number_of_installments=master.number_of_installments,
#                     is_active=master.is_active,
#                     active_from_date=master.active_from_date,
#                     is_deleted=master.is_deleted,
#                     details=details
#                 )
#             )
#         return result

#     # Case 4: Both `installment_master_id` and `installment_detail_id` are provided
#     elif installment_master_id is not None and installment_detail_id is not None:
#         # Filter by `installment_master_id`
#         query = query.filter(InstallmentMaster.id == installment_master_id)
#         # Fetch relevant InstallmentMaster records
#         installment_masters = query.all()
#         # For each InstallmentMaster, filter details by `installment_detail_id`
#         result = []
#         for master in installment_masters:
#             master_details_query = db.query(InstallmentDetails).filter(InstallmentDetails.installment_master_id == master.id)
#             master_details_query = master_details_query.filter(InstallmentDetails.id == installment_detail_id)
#             master_details = master_details_query.all()
#             details = [
#                 InstallmentDetailsForGet(
#                     id=detail.id,
#                     installment_master_id=detail.installment_master_id,
#                     installment_name=detail.installment_name,
#                     payment_rate=detail.payment_rate,
#                     due_date=detail.due_date,
#                     is_deleted=detail.is_deleted
#                 )
#                 for detail in master_details
#             ]
#             result.append(
#                 InstallmentMasterForGet(
#                     id=master.id,
#                     number_of_installments=master.number_of_installments,
#                     is_active=master.is_active,
#                     active_from_date=master.active_from_date,
#                     is_deleted=master.is_deleted,
#                     details=details
#                 )
#             )
#         return result

#     return []

    
                  