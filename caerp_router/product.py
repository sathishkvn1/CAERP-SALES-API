

from fastapi import APIRouter, Depends,HTTPException, UploadFile,status,File,Query,Request
from typing import List, Optional,Dict
from UserDefinedConstants.user_defined_constants import BooleanFlag, DeletedStatus,Operator,ActiveStatus,ActionType,RecordActions
from caerp_auth.authentication import authenticate_user
from typing import Union

from caerp_db.models import  AdminUser, Designation, InstallmentDetails, InstallmentMaster, ProductRating,ProductMaster, ProductModule, UserRole
from caerp_schemas import AdminUserBaseForDelete, AdminUserChangePasswordSchema, AdminUserCreateSchema, AdminUserDeleteSchema, AdminUserListResponse, AdminUserUpdateSchema, DesignationDeleteSchema, DesignationInputSchema, DesignationListResponse, DesignationListResponses, DesignationSchemaForDelete, DesignationUpdateSchema, InstallmentCreate,  InstallmentDetailsForGet, InstallmentEdit, InstallmentFilter, InstallmentMasterForGet, ProductCategorySchema, ProductMasterSchema, ProductModuleSchema, ProductVideoSchema, User, UserImageUpdateSchema, UserLoginResponseSchema, UserLoginSchema, UserRoleDeleteSchema, UserRoleForDelete, UserRoleInputSchema, UserRoleListResponse, UserRoleListResponses, UserRoleSchema, UserRoleUpdateSchema
from caerp_schemas import ProductMasterPriceSchema,PriceListProductMasterView,ProductRating,PriceListProductModuleResponse,PriceListProductModuleView,PriceListProductMasterResponse,PriceListProductModule,PriceListProductMaster,ProductMasterSchemaResponse,ProductVideoSchemaResponse,ProductModuleSchemaResponse,ProductCategorySchemaResponse
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
from sqlalchemy import and_, or_

# UPLOAD_DIR_MASTER       = "uploads/product_master_videos"
# UPLOAD_DIR_MASTER_IMAGE = "uploads/product_master_images"
UPLOAD_DIR_MODULE       = "uploads/product_module_images"
UPLOAD_DIR_VIDEO        = "uploads/product_master_additional_videos"
UPLOAD_DIR_MASTER_IMAGE_VIDEO = "uploads/product_master_image_video"


router = APIRouter(
    # prefix="/admin",
    tags=["PRODUCTS"]
)



#/////////////////////

@router.get("/get_all_product_master/", response_model=List[ProductMasterSchemaResponse])
async def get_all_products(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):

    product = db_product.get_all_product_master_by_deleted_status(db, deleted_status)
    # return {"product master": product}
    return product





@router.post('/save_product_master/', response_model=ProductMasterSchema)
def save_product_master(
        product_master_data: ProductMasterSchema =Depends(),
        # product_id: int =0,  # Default to 0 for add operation
        video_file: UploadFile = File(None),
        image_file: UploadFile = File(None),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
       
):
     # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    # try:
    new_product = db_product.save_product_master(db, product_master_data,user_id)
        
    if video_file:
            
                product_id = new_product.id
                file_content = video_file.file.read()
                file_path = f"{UPLOAD_DIR_MASTER_IMAGE_VIDEO}/{product_id}.mp4"
                with open(file_path, "wb") as f:
                    f.write(file_content)
            
    if image_file:
            
                product_id = new_product.id
                file_content = image_file.file.read()
                file_path = f"{UPLOAD_DIR_MASTER_IMAGE_VIDEO}/{product_id}.jpg"
                with open(file_path, "wb") as f:
                    f.write(file_content)
    return new_product

   


@router.post('/update_product_master/{product_id}', response_model=ProductMasterSchema)
def update_product_master(
        product_master_data: ProductMasterSchema =Depends(),
        product_id: int =0,  # Default to 0 for add operation
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
       
):
     # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    try:
        new_product = db_product.update_product_master(db, product_master_data,product_id,user_id)
        
        return new_product
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed operation")
   



@router.post('/upload_product_main_video/{id}', response_model=ProductMasterSchema)
def upload_product_main_video(
        id: int,
        video_file: UploadFile = File(...),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    """
    Uploads the main video for a product master.

    Parameters:
    - id (int): The ID of the product master.
    - video_file (UploadFile): The video file to upload.

    Returns:
    - ProductMaster: The updated product master including the uploaded video URL.
    """
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    # Check if the product master exists
    product_master = db.query(ProductMaster).filter(ProductMaster.id == id).first()
    if not product_master:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product master not found")

    try:
        # Save the new video file
        file_content = video_file.file.read()
        file_path = f"{UPLOAD_DIR_MASTER_IMAGE_VIDEO}/{product_master.id}.mp4"
        with open(file_path, "wb") as f:
            f.write(file_content)

       
        db.commit()

        # Return the updated product master data
        return product_master

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to upload video")
   
#...........................................................
@router.get("/video/get_product_master_video/{id}", response_model=dict)
def get_product_master_video(id: int):
    
    product_master_video_filename = f"{id}.mp4"  
    # BASE_URL="http://127.0.0.1:8010/"
    return {"photo_url": f"{BASE_URL}/product/save_product_master/{product_master_video_filename}"}

@router.post('/update_product_master_image/{id}', response_model=ProductMasterSchema)
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
    product = db.query(ProductMaster).filter(ProductMaster.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Save the new image
    file_content = image_file.file.read()
    file_path = f"{UPLOAD_DIR_MASTER_IMAGE_VIDEO}/{product.id}.jpg"
    with open(file_path, "wb") as f:
        f.write(file_content)

    # Return the updated user data
    return product

  
@router.get("/image/get_product_master_image/{id}", response_model=dict)
def get_product_master_image(id: int):
    
    product_master_image_filename = f"{id}.jpg"  
    # BASE_URL="http://127.0.0.1:8010/"
    return {"photo_url": f"{BASE_URL}/product/save_product_master/{product_master_image_filename}"}



@router.get("/get_product_master_by_id/{product_id}", response_model=List[ProductMasterSchemaResponse])
def get_product_master_by_id(product_id: int, db: Session = Depends(get_db)):
    product_master_details = db_product.get_product_master_by_id(db, product_id)
    if not product_master_details:
        raise HTTPException(status_code=404, detail="No products found for this id")
    return product_master_details


@router.get("/get_product_master_by_code/{product_code}", response_model=List[ProductMasterSchemaResponse])
def get_product_master_by_code(product_code: str, db: Session = Depends(get_db)):
    product_master_details = db_product.get_product_master_by_code(db, product_code)
    if not product_master_details:
        raise HTTPException(status_code=404, detail="No products found for this id")
    return product_master_details




@router.delete("/delete/product_master/{product_id}")
def delete_product_master(
                     product_id: int,
                     action_type: ActionType = ActionType.UNDELETE,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)
                    ):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    
    return db_product.delete_product_master(db, product_id,action_type,deleted_by=user_id)




# @router.delete("/delete/product_master/{product_id}")
# def delete_product_master(
#                      product_id: int,
#                      db: Session = Depends(get_db),
#                      token: str = Depends(oauth2.oauth2_scheme)
#                     ):
#     if not token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

#     auth_info = authenticate_user(token)
#     user_id = auth_info["user_id"]
    
    
#     return db_product.delete_product_master(db, product_id,deleted_by=user_id)





@router.get("/get_all_product_category/", response_model=List[ProductCategorySchemaResponse])
async def get_all_product_category(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):

    product = db_product.get_all_product_category_by_deleted_status(db, deleted_status)
    return product

@router.post('/save_product_category/{category_id}', response_model=ProductCategorySchema)
def save_product_category(
        product_category_data: ProductCategorySchema ,
        category_id: int =0,  # Default to 0 for add operation
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    try:
        new_product = db_product.save_product_category(db, product_category_data,category_id,user_id)
    
        return new_product
    except Exception as e:
        error_detail = [{
            "loc": ["server"],
            "msg": "Internal server error",
            "type": "internal_server_error"
        }]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)



@router.get("/get_product_category_by_id/{category_id}", response_model=List[ProductCategorySchemaResponse])
def get_product_category_by_id(
    category_id: int,
     db: Session = Depends(get_db)
     ):
    product_category_details = db_product.get_product_category_by_id(db, category_id)
    if not product_category_details:
        raise HTTPException(status_code=404, detail="No products found for this id")
    return product_category_details




@router.delete("/delete/product_category/{category_id}")
def delete_product_category(
                     category_id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)
                    ):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    return db_product.delete_product_category(db, category_id,deleted_by=user_id)





@router.post('/save_product_module/', response_model=ProductModuleSchema)
def save_product_module(
        display_order: int =1,
        product_module_data: ProductModuleSchema =Depends(),
        image_file: UploadFile = File(None),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
       
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    try:
        new_product = db_product.save_product_module(db, product_module_data,display_order,user_id)
        if image_file:
            
                module_id = new_product.id
                file_content = image_file.file.read()
                file_path = f"{UPLOAD_DIR_MODULE}/{module_id}.jpg"
                with open(file_path, "wb") as f:
                    f.write(file_content)
  
        return new_product    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed operation")



@router.post('/update_product_module/{module_id}', response_model=ProductModuleSchema)
def update_product_module(
        product_module_data: ProductModuleSchema =Depends(),
        module_id: int =0,  # Default to 0 for add operation
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
       
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    new_product = db_product.update_product_module(db, product_module_data,module_id,user_id)
    return new_product    


#_____________________________________________________
@router.post('/update_product_module_image/{id}', response_model=ProductModuleSchemaResponse)
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
    user = db.query(ProductModule).filter(ProductModule.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Save the new image
    file_content = image_file.file.read()
    file_path = f"{UPLOAD_DIR_MODULE}/{user.id}.jpg"
    with open(file_path, "wb") as f:
        f.write(file_content)

    # Return the updated user data
    return user




#_____________________________________________________


@router.get("/get_product_module/images/{id}", response_model=dict)
def get_product_module_image_url(id: int):
    
    profile_photo_filename = f"{id}.jpg"  
    # BASE_URL="http://127.0.0.1:8010/"
    return {"photo_url": f"{BASE_URL}/product/save_product_module/{profile_photo_filename}"}


@router.get("/get_product_module_by_id/{module_id}", response_model=List[ProductModuleSchemaResponse])
def get_product_module_by_id(
    module_id: int,
     db: Session = Depends(get_db)
     ):
    product_module_details = db_product.get_product_module_by_id(db, module_id)
    if not product_module_details:
        raise HTTPException(status_code=404, detail="No products found for this id")
    return product_module_details

@router.get("/get_product_module_by_product_id/{id}", response_model=List[ProductModuleSchemaResponse])
def get_product_module_by_product_id(
     id: int,
     db: Session = Depends(get_db)
     ):
    product_module_details = db_product.get_product_module_by_product_id(db, id)
    if not product_module_details:
        raise HTTPException(status_code=404, detail="No products found for this id")
    return product_module_details




@router.delete("/delete/product_module/{module_id}")
def delete_product_module(
                     module_id: int,
                     action_type: ActionType = ActionType.UNDELETE,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)
                     
                    ):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    
    return db_product.delete_product_module(db, module_id,action_type,deleted_by=user_id)




@router.get("/get_all_product_video/", response_model=List[ProductVideoSchemaResponse])
async def get_all_product_video(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):

    product = db_product.get_all_product_video_by_deleted_status(db, deleted_status)
    return product




import logging
logger = logging.getLogger(__name__)

@router.post('/save_product_additional_videos/', response_model=ProductVideoSchema)
def save_product_video(
        product_video_data: ProductVideoSchema = Depends(),
        video_file: UploadFile = File(None),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    try:
        new_product_video = db_product.save_product_video(db, product_video_data, user_id)
        if video_file:
            # if video_id==0:
            video_id = new_product_video.id
            file_content = video_file.file.read()
            file_path = f"{UPLOAD_DIR_VIDEO}/{video_id}.mp4"
            with open(file_path, "wb") as f:
                f.write(file_content)
        
        return new_product_video
    except Exception as e:
        logger.exception("Failed to save product video")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed operation")

    

@router.post('/update_product_additional_video_details/{video_id}', response_model=ProductVideoSchema)
def update_product_video(
        product_video_data: ProductVideoSchema =Depends(),
        video_id: int =0,  # Default to 0 for add operation
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
       
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    try:
        new_product_video = db_product.update_product_video(db, product_video_data,video_id,user_id)
       
        return new_product_video
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed operation")


@router.get("/video/get_product_additonal_video/{id}", response_model=dict)
def get_product_additonal_video(id: int):
    
    profile_photo_filename = f"{id}.mp4"  
    # BASE_URL="http://127.0.0.1:5000"
    return {"photo_url": f"{BASE_URL}/product/save_product_additional_videos/{profile_photo_filename}"}





@router.get("/get_product_video_by_id/{video_id}", response_model=List[ProductVideoSchemaResponse])
def get_product_video_by_id(
    video_id: int,
     db: Session = Depends(get_db)
     ):
    product_video_details = db_product.get_product_video_by_id(db, video_id)
    if not product_video_details:
        raise HTTPException(status_code=404, detail="No products found for this id")
    return product_video_details


@router.get("/get_product_additinal_video_by_product_master_id/{video_id}", response_model=List[ProductVideoSchemaResponse])
def get_product_video_by_product_master_id(
    video_id: int,
     db: Session = Depends(get_db)
     ):
    product_video_details = db_product.get_product_video_by_product_master_id(db, video_id)
    if not product_video_details:
        raise HTTPException(status_code=404, detail="No products found for this id")
    return product_video_details


# @router.get("videos/get_product_additional_video/{user_id}", response_model=dict)
# def get_our_team_image_url(user_id: int):
    
#     video_filename = f"{user_id}.jpg"  
   
#     return {"photo_url": f"{BASE_URL}/product/save_product_additional_video/{video_filename}"}

@router.delete("/delete/product_video/{video_id}")
def delete_product_video(
                     video_id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)
                    ):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    return db_product.delete_product_video(db, video_id,deleted_by=user_id)

#////
@router.get("/get_all_installment_master/",response_model=List[InstallmentMasterForGet])
async def get_all_installment_master(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):
    return get_all_installment_master_by_status(db, deleted_status)

def get_all_installment_master_by_status(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(InstallmentMaster).filter(InstallmentMaster.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(InstallmentMaster).filter(InstallmentMaster.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(InstallmentMaster).all()
    else:
       
        raise ValueError("Invalid deleted_status")
    


@router.get("/get_installment_details_by_id/{id}", response_model=InstallmentDetailsForGet)
def get_installment_details_by_id(id: int,
                      db: Session = Depends(get_db)
                      ):


    installment_master = db_product.get_installment_details_by_id(db,id)
    if installment_master is None:
        raise HTTPException(status_code=404, detail="Not found")

    return installment_master



@router.get("/get_all_installment_details/",response_model=List[InstallmentDetailsForGet])
async def get_all_installment_details(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):
    return get_all_installment_details_by_status(db, deleted_status)

def get_all_installment_details_by_status(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(InstallmentDetails).filter(InstallmentDetails.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(InstallmentDetails).filter(InstallmentDetails.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(InstallmentDetails).all()
    else:
       
        raise ValueError("Invalid deleted_status")


@router.post("/save_installments/", response_model=None)
def create_installments(
    installment_data: InstallmentCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    
    # print(f"User ID: {user_id}")
    # print(f"Installment Data: {installment_data}")
    
    # Create the installment records
    installment_master, installment_details = db_product.create_installments(db, installment_data, user_id)
    
    # print(f"Created installment master: {installment_master}")
    # print(f"Created installment details: {installment_details}")    
    return {"installment_master": installment_master, "installment_details": installment_details}






@router.post("/edit_installments/{installment_id}", response_model=None)
def edit_installments(
    installment_id: int,
    installment_data: InstallmentEdit,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]

    db_product.update_installment_master(db, installment_id, installment_data.dict(exclude_unset=True), user_id)
    db_product.update_installment_details(db, installment_id, installment_data.dict(exclude_unset=True), user_id)
    
    return {"message": "Installment updated successfully"}


@router.delete("/delete/installment_master/{id}")
def delete_installment_master(
                     
                     id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    
    
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]

    return db_product.delete_installment_master(db, id, deleted_by=user_id)






# @router.get("/get_installment_masters/", response_model=List[InstallmentMasterForGet])
# def get_installment_masters(
#     status: ActiveStatus = Query(..., description="Filter by status: 'all' for all records, 'yes' for active records, 'no' for deleted records"),
#     db: Session = Depends(get_db)
# ):
#     query = db.query(InstallmentMaster)
    
#     if status == ActiveStatus.ACTIVE:
#         query = query.filter(InstallmentMaster.is_active == 'yes')
#     elif status == ActiveStatus.DELETED:
#         query = query.filter(InstallmentMaster.is_deleted == 'no')

#     return query.all()


@router.get("/installment_masters/", response_model=List[InstallmentMasterForGet])
def get_installment_masters(
    status: ActiveStatus = ActiveStatus.ALL,
    db: Session = Depends(get_db)
):
    query = db.query(InstallmentMaster)
    
    if status == ActiveStatus.ACTIVE:
        query = query.filter(and_(InstallmentMaster.is_active == 'yes', InstallmentMaster.is_deleted == 'no'))
    elif status == ActiveStatus.NOT_DELETED:
        query = query.filter(and_(InstallmentMaster.is_deleted == 'no'))
    elif status == ActiveStatus.DELETED:
        query = query.filter(and_(InstallmentMaster.is_deleted == 'yes'))
    elif status == ActiveStatus.ALL:
        pass  # Return all records without applying any additional filters

    return query.all()

@router.get("/get_installment_details/{installment_master_id}", response_model=List[InstallmentDetailsForGet])
def get_installment_details(
    installment_master_id: int,
    db: Session = Depends(get_db)
):
    query = db.query(InstallmentDetails).filter(InstallmentDetails.installment_master_id == installment_master_id).all()
    return query


@router.get("/installments/", response_model=List[InstallmentMasterForGet])
def get_installment_masters(
    filter: InstallmentFilter = Depends(),
    db: Session = Depends(get_db)
):
    query = db.query(InstallmentMaster)
    
    if filter.is_active:
        query = query.filter(InstallmentMaster.is_active == filter.is_active)
    if filter.is_deleted:
        query = query.filter(InstallmentMaster.is_deleted == filter.is_deleted)

    return query.all()


#====================================================================================================

@router.post('/update_price_product_module')
def update_price_product_module(
        record_actions  : RecordActions,  
        price_list_data: PriceListProductModule =Depends(),        
        price_list_product_module_id: int =0,  # Default to 0 for add operation
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    if record_actions == RecordActions.UPDATE_ONLY:
        return {"success": True, "message": "Update price list successfully"}
    elif record_actions == RecordActions.UPDATE_AND_INSERT:
        return {"success": True, "message": "Add new price list successfully"}
    else:
        return {"success": False, "message": "Invalid action"} 



@router.post('/set_new_price')
def set_new_price(
    price_data_list: List[ProductMasterPriceSchema] , 
    record_actions  : RecordActions, 
    price_id    :   Optional[int]= None,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
    ):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    if record_actions == RecordActions.UPDATE_ONLY:
        success_message = "Rate  Edited Successfully"
    if record_actions == RecordActions.UPDATE_AND_INSERT:
        success_message = "New Rates Set Successfully"
    for price_data in price_data_list:
        new_price = db_product.set_new_price(db, price_data, user_id, record_actions,price_id)
        if not new_price:
            return {"success": False, "message": f"Error inserting price for product_master_id {price_data.product_master_id}"}

    return {"success": True, "message": "New Rates Set Successfully"} 
    
    
    
@router.get('/get_price_list_master')
def get_price_list_master(
    product_id: Optional[int] = None,
    product_name: Optional[str] = None,
    requested_date: Optional[date] =None,
    operator : Operator = Operator.EQUAL_TO, # date filter parameter, 
    db: Session = Depends(get_db)
):
        price_list_results =db_product.get_price_list_master(db,product_id,product_name,requested_date,operator)

        if not price_list_results:
           raise HTTPException(status_code=404, detail="No price list found for the given criteria")

        # return price_list_results
        # products: Dict[int, Dict[str, any]] = {}
        products: List[Dict[str, any]] = []

        for result in price_list_results:
            product_master_id  =  result.product_master_id
        # Create a dictionary to represent the product and its price list
            product_data = [{

                "product_master_id": result.product_master_id,
                "product_code": result.product_code,               
                "product_name": result.product_name, 
                "product_master_price_id":result.product_master_price_id,
                "price": result.price,
                "gst_rate": result.gst_rate,
                "cess_rate": result.cess_rate,
                "effective_from_date": result.effective_from_date,
                "effective_to_date": result.effective_to_date,
                "has_module":result.has_module,
                "is_deleted": result.is_deleted
               
            }]
            products.append(product_data)
        return products
