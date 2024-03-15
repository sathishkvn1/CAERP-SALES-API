from fastapi import APIRouter, Depends,File,HTTPException, UploadFile,status
from typing import List
from caerp_db.models import FaqCategoryDB, FaqDB, ImageGalleryDB, OurDirectorDB, OurTeam, PrimeCustomer, SocialMediaURL, TrendingNews
from caerp_schemas import  AboutUsResponse, AboutUsSchema, AboutUsUpdateSchema, CompanyMasterBase, ContactDetailResponse, ContactDetailsSchema, FAQBase, FAQCategoryID, FaqCategory, FaqCategoryResponse, FaqCategorySchemaForDelete, FaqResponse, FaqSchema, FaqSchemaForDelete, GeneralContactDetailsResponse, GeneralContactDetailsSchema, HomeBannerSchema, HomeBannerSchemaResponse, HomeMiracleAutomationSchema, HomeMiracleAutomationSchemaResponse, HomeTrendingNewsSchema, HomeTrendingNewsSchemaResponse, ImageGalleryResponse, ImageGallerySchema, ImageGallerySchemaForGet, JobApplicationSchema, JobApplicationSchemaResponse, JobVacancieSchema, JobVacancieSchemaResponse, MiracleFeaturesSchema, MiracleFeaturesSchemaResponse, OurDirectorResponse, OurDirectorSchema, OurDirectorSchemaforDelete, OurTeamSchema, OurTeamSchemaResponse, OurTeamSchemaforDelete, PrimeCustomerSchema, PrimeCustomerSchemaResponse, PrivacyPolicyResponse, PrivacyPolicySchema, SiteLegalAboutUsBase, SiteLegalAboutUsBaseResponse, SocialMediaResponse, SocialMediaSchema, SocialMediaURLSchema, SubContentUpdateSchema, TermsAndConditionResponse, TermsAndConditionSchema, TrendingNewsResponse, TrendingNewsSchema, TrendingNewsSchemaForDeletedStatus
from sqlalchemy.orm import Session
from caerp_db.database import get_db
from caerp_db import db_sitemanager
from caerp_auth import oauth2
from UserDefinedConstants.user_defined_constants import DeletedStatus
from starlette.requests import Request
from caerp_auth.authentication import authenticate_user
import logging
from settings import BASE_URL

# Configure logging
logging.basicConfig(level=logging.DEBUG)

UPLOAD_DIR = "uploads/our_directors"
UPLOAD_DIR_TEAM = "uploads/our_teams"
UPLOAD_DIR_NEWS = "uploads/trending_news"
UPLOAD_DIR_IMAGEGALLERY = "uploads/image_gallery"
UPLOAD_DIR_CUSTOMER="uploads/prime_customers"


router = APIRouter(
    # prefix="/sitemanager",
    tags=["SITEMANAGER"]
)

@router.get("/about_us", response_model=List[AboutUsResponse])
def get_about_us_details(db: Session = Depends(get_db)):
    
    about_us_details = db_sitemanager.get_about_us_details(db)
    return [{"aboutus": about_us_details}]

#---------------------------------------------------------------------------------------------------------------
@router.post("/update/about_us/main_content{id}", response_model=AboutUsUpdateSchema)
def update_main_content(id: int,
                     role_input: AboutUsUpdateSchema,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    return db_sitemanager.update_maincontent(db, id, role_input)

#---------------------------------------------------------------------------------------------------------------

@router.post("/update/about_us/sub_content{id}", response_model=SubContentUpdateSchema)
def update_sub_content(id: int,
                     role_input: SubContentUpdateSchema,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    return db_sitemanager.update_subcontent(db, id, role_input)

         
#------------------------------------------------------------------------------------------------------------

@router.post('/save_team/{team_id}', response_model=OurTeamSchema)
def save_team(
       
        team_id: int = 0,  # Default to 0 for add operation
        team_data: OurTeamSchema = Depends(),
        image_file: UploadFile = File(None),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    """
    Endpoint to save or update team information.

    Parameters:
    - team_id (int, optional): The ID of the team to update. Defaults to 0 for add operation.
    - team_data (OurTeamSchema): The data of the team to save or update.
    - image_file (UploadFile, optional): The image file to upload for the team.
    - db (Session): The database session.
    - token (str): The authorization token.

    Returns:
    - OurTeamSchema: The saved or updated team.
    """
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
   
    
    try:
        new_team = db_sitemanager.save_team(db, team_data, team_id, user_id)
        
        # If image provided, save it
        if image_file:
            file_content = image_file.file.read()
            file_path = f"{UPLOAD_DIR_TEAM}/{new_team.id}.jpg"
            with open(file_path, "wb") as f:
                f.write(file_content)
        
        return new_team
    except Exception as e:
        error_detail = [{
            "loc": ["server"],
            "msg": "Internal server error",
            "type": "internal_server_error"
        }]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)


#--------------------------------------------------------------------------------------------------------------

@router.delete("/delete/team/{team_id}")
def delete_team(
                     request: Request,
                     team_id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    return db_sitemanager.delete_team(db, team_id, deleted_by=user_id)

#---------------------------------------------------------------------------------------------------------------

@router.get("/get_all_teams/" , response_model=List[OurTeamSchemaforDelete])
async def get_all_teams(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):
    return get_all_team_by_deleted_status(db, deleted_status)



def get_all_team_by_deleted_status(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(OurTeam).filter(OurTeam.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(OurTeam).filter(OurTeam.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(OurTeam).all()
    else:
       
        raise ValueError("Invalid deleted_status")
    
    
    
#---------------------------------------------------------------------------------------------------------------


@router.get("/our_teams/images/{user_id}", response_model=dict)
def get_our_team_image_url(user_id: int):
    
    profile_photo_filename = f"{user_id}.jpg"  
    return {"photo_url": f"{BASE_URL}/sitemanager/save_team/{profile_photo_filename}"}

#---------------------------------------------------------------------------------------------------------------
@router.get("/get_teams_by_id/{team_id}", response_model=OurTeamSchemaResponse)
def get_teams_by_id(team_id: int,
                        db: Session = Depends(get_db)):
    
    team_detail = db_sitemanager.get_our_teams_by_id(db, team_id)
    if team_detail is None:
        raise HTTPException(status_code=404, detail=f"Team not found with ID {team_id}")
    return {"team": [team_detail]}


#---------------------------------------------------------------------------------------------------------------

@router.post('/save_director/{director_id}', response_model=OurDirectorSchema)
def save_director(
    director_id: int = 0,  # Default to 0 for add operation
    director_data: OurDirectorSchema = Depends(),
    image_file: UploadFile = File(None),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    """
    Endpoint to save or update director information.

    Parameters:
    - director_id (int, optional): The ID of the director to update. Defaults to 0 for add operation.
    - director_data (OurDirectorSchema): The data of the director to save or update.
    - image_file (UploadFile, optional): The image file to upload for the director.
    - db (Session): The database session.
    - token (str): The authorization token.

    Returns:
    - OurDirectorSchema: The saved or updated director.
    """
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    
    try:
        new_director = db_sitemanager.save_director(db, director_data,director_id, user_id)
        director_id = new_director.id

        
        # If image provided, save it
        if image_file:
            file_content = image_file.file.read()
            file_path = f"{UPLOAD_DIR}/{director_id}.jpg"
            with open(file_path, "wb") as f:
                f.write(file_content)
        
        return new_director
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed operation")

#---------------------------------------------------------------------------------------------------------------

@router.delete("/delete/directors/{id}")
def delete_director_details(
                     
                     id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    
    
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]

    return db_sitemanager.delete_director_details(db, id, deleted_by=user_id)

#---------------------------------------------------------------------------------------------------------------
@router.get("/get_all_directors/",response_model=List[OurDirectorSchemaforDelete])
async def get_all_directors(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):
    return get_all_directors_by_deleted_status(db, deleted_status)

def get_all_directors_by_deleted_status(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(OurDirectorDB).filter(OurDirectorDB.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(OurDirectorDB).filter(OurDirectorDB.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(OurDirectorDB).all()
    else:
       
        raise ValueError("Invalid deleted_status")
    
#---------------------------------------------------------------------------------------------------------------    

@router.get("/our_directors/images/{user_id}", response_model=dict)
def get_our_team_image_url(user_id: int):
    
    profile_photo_filename = f"{user_id}.jpg"  
    return {"photo_url": f"{BASE_URL}/sitemanager/save_director/{profile_photo_filename}"}

#---------------------------------------------------------------------------------------------------------------    
@router.get("/get_directors_by_id/{id}", response_model=OurDirectorResponse)
def get_teams_by_id(id: int,
                        db: Session = Depends(get_db)):
    
    director_detail = db_sitemanager.get_directors_by_id(db, id)
    if director_detail is None:
        raise HTTPException(status_code=404, detail=f"Director not found with ID {id}")
    return {"director": [director_detail]}


#---------------------------------------------------------------------------------------------------------------    

@router.post("/save_faq_category/{id}", response_model=FaqCategory)
def save_faq_category(
    faq_category: FaqCategory,
    id: int = 0,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    return db_sitemanager.save_faq_category(db, id, faq_category, user_id)



#---------------------------------------------------------------------------------------------------------------
@router.delete("/delete/faq_category/{id}")
def delete_faq_category(
                     id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    
    
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    return db_sitemanager.delete_faq_category(db, id, deleted_by=user_id)

#---------------------------------------------------------------------------------------------------------------
@router.get("/get_all_faq_category/",response_model=List[FaqCategorySchemaForDelete])
async def get_all_faq_category(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):

    return get_all_faq_category_by_deleted_status(db, deleted_status)



def get_all_faq_category_by_deleted_status(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(FaqCategoryDB).filter(FaqCategoryDB.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(FaqCategoryDB).filter(FaqCategoryDB.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(FaqCategoryDB).all()
    else:
       
        raise ValueError("Invalid deleted_status")
    
#---------------------------------------------------------------------------------------------------------------
@router.get("/get_all_faq_category_by_id/{id}", response_model=FaqCategoryResponse)
def get_all_faq_category_by_id(id: int,
                        db: Session = Depends(get_db)):
    
    faq_detail = db_sitemanager.get_all_faq_category_by_id(db, id)
    if faq_detail is None:
        raise HTTPException(status_code=404, detail=f"Faq Category not found with ID {id}")
    return {"faq": [faq_detail]}

#---------------------------------------------------------------------------------------------------------------
@router.post("/save/faq/{id}", response_model=FaqSchema)
def save_faq(
    
    faq: FaqSchema,
    id: int = 0,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    return db_sitemanager.save_faq(db, id, faq, user_id)

#---------------------------------------------------------------------------------------------------------------    
@router.delete("/delete/faq/{id}")
def delete_faq(
                     
                     id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    
    
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    return db_sitemanager.delete_faq(db, id, deleted_by=user_id)

 #---------------------------------------------------------------------------------------------------------------       
@router.get("/get_all_faq/",response_model=List[FaqSchemaForDelete])
async def get_all_faq(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):
    return get_all_faq_by_deleted_status(db, deleted_status)



def get_all_faq_by_deleted_status(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(FaqDB).filter(FaqDB.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(FaqDB).filter(FaqDB.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(FaqDB).all()
    else:
       
        raise ValueError("Invalid deleted_status")

#---------------------------------------------------------------------------------------------------------------    
@router.get("/get_all_faq_by_id/{id}", response_model=FaqResponse)
def get_all_faq_by_id(id: int,
                        db: Session = Depends(get_db)):
    
    faq_detail = db_sitemanager.get_all_faq_by_id(db, id)
    if faq_detail is None:
        raise HTTPException(status_code=404, detail=f"Not found with ID {id}")
    return {"faq": [faq_detail]}

#---------------------------------------------------------------------------------------------------------------    




#---------------------------------------------------------------------------------------------------------------    
@router.post("/save/social_media_url/{id}", response_model=SocialMediaURLSchema)
def save_social_media_url(
    data: SocialMediaURLSchema,
    id: int = 0,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    return db_sitemanager.save_social_media_url(db, id, data, user_id)


#---------------------------------------------------------------------------------------------------------------    
@router.delete("/delete/social_media_url/{id}")
def delete_social_media_url(
                    
                     id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    
    
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    return db_sitemanager.delete_social_media_url(db, id, deleted_by=user_id)


#---------------------------------------------------------------------------------------------------------------    



@router.get("/get_all_social_media_url/", response_model=List[SocialMediaSchema])
async def get_all_social_media_url(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                                    db: Session = Depends(get_db)):
    return get_all_social_media_url_by_deleted_status(db, deleted_status)

def get_all_social_media_url_by_deleted_status(db: Session, deleted_status: DeletedStatus):
    query = db.query(SocialMediaURL)
    
    if deleted_status == DeletedStatus.DELETED:
        query = query.filter(SocialMediaURL.is_deleted == 'yes')
    elif deleted_status == DeletedStatus.NOT_DELETED:
        query = query.filter(SocialMediaURL.is_deleted == 'no')

    return query.all()
    
 #---------------------------------------------------------------------------------------------------------------       
@router.get("/get_social_media_by_id/{id}", response_model=SocialMediaResponse)
def get_social_media_by_id(id: int,
                        db: Session = Depends(get_db)):
    
    detail = db_sitemanager.get_social_media_by_id(db, id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Not found with ID {id}")
    return {"social_media": [detail]}
#---------------------------------------------------------------------------------------------------------------       




@router.post("/update/contact_details{id}", response_model=ContactDetailsSchema)
def update_contact_details(id: int,
                     
                     role_input: ContactDetailsSchema,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    return db_sitemanager.update_contact_details(db, id, role_input,modified_by=user_id)

#--------------------------------------------------------------------------------------------------------------- 
 
@router.get("/get_contact_details", response_model=List[ContactDetailResponse])
def get_contact_details(db: Session = Depends(get_db)):
    
    contact_details = db_sitemanager.get_contact_details(db)
    return [{"contact": contact_details}]

#--------------------------------------------------------------------------------------------------------------- 
@router.post("/update/privacy_policy{id}", response_model=PrivacyPolicySchema)
def update_privacy_policy(id: int,
                          
                     role_input: PrivacyPolicySchema,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    return db_sitemanager.update_privacy_policy(db, id, role_input,modified_by=user_id)

#--------------------------------------------------------------------------------------------------------------- 

@router.get("/get_privacy_policy", response_model=List[PrivacyPolicyResponse])
def get_privacy_policy(db: Session = Depends(get_db)):
    
    privacy_policy = db_sitemanager.get_privacy_policy(db)
    return [{"privacy_policy": privacy_policy}]

#--------------------------------------------------------------------------------------------------------------- 
@router.post("/update/terms_and_condition{id}", response_model=TermsAndConditionSchema)
def update_terms_and_condition(id: int,
                        
                     role_input: TermsAndConditionSchema,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    return db_sitemanager.update_terms_and_condition(db, id, role_input,modified_by=user_id)
#--------------------------------------------------------------------------------------------------------------- 
 
@router.get("/get_terms_and_condition", response_model=List[TermsAndConditionResponse])
def get_terms_and_condition(db: Session = Depends(get_db)):
    
    terms_and_condition = db_sitemanager.get_terms_and_condition(db)
    return [{"terms_and_condition": terms_and_condition}]


#--------------------------------------------------------------------------------------------------------------- 


@router.post('/save_image_gallery/{gallery_id}', response_model=ImageGallerySchema)
def save_image_gallery(
    
    gallery_id: int = 0,  # Default to 0 for add operation
    data: ImageGallerySchema = Depends(),
    image_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    """
    Endpoint to save or update image gallery information.

    Parameters:
    - gallery_id (int, optional): The ID of the image gallery to update. Defaults to 0 for add operation.
    - data (ImageGallerySchema): The data of the image gallery to save or update.
    - image_file (UploadFile): The image file to upload for the image gallery.
    - db (Session): The database session.
    - token (str): The authorization token.

    Returns:
    - ImageGallerySchema: The saved or updated image gallery.
    """
    # Log request information
    logging.debug("Received request to add/update image gallery.")

    # Validate token and user session
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    try:
        if gallery_id == 0:
            # Add operation
            new_images = db_sitemanager.add_images(db, data, user_id)
            gallery_id = new_images.id
        else:
            # Update operation
            new_images = db_sitemanager.update_image_gallery(db, gallery_id, data, user_id)
        
        # Save uploaded image
        if image_file:
            file_content = image_file.file.read()
            file_path = f"{UPLOAD_DIR_IMAGEGALLERY}/{gallery_id}.jpg"
            with open(file_path, "wb") as f:
                f.write(file_content)
        
        # Log success message
        logging.debug("Image gallery saved/updated successfully.")
        
        return new_images
    except Exception as e:
        # Log error details
        logging.error(f"Failed to save/update image gallery: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save/update image gallery")



    
#------------------------------------------------------------------------------------------------------------------------------------------- 
@router.delete("/delete/image_gallery_details/{id}")
def delete_image_gallery_details(
                     
                     id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    
    
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    return db_sitemanager.delete_image_gallery_details(db, id, deleted_by=user_id)

#------------------------------------------------------------------------------------------------------------------------------------------- 
@router.get("/get_all_image_gallery_items/" , response_model=List[ImageGallerySchemaForGet])
async def get_all_image_gallery_items(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):
    return get_all_image_gallery_items(db, deleted_status)



def get_all_image_gallery_items(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(ImageGalleryDB).filter(ImageGalleryDB.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(ImageGalleryDB).filter(ImageGalleryDB.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(ImageGalleryDB).all()
    else:
       
        raise ValueError("Invalid deleted_status")
		

#------------------------------------------------------------------------------------------------------------------------------------------- 
@router.get("/get_image_gallery_by_id/{id}", response_model=ImageGalleryResponse)
def get_image_gallery_by_id(id: int,
                        db: Session = Depends(get_db)):
    
    detail = db_sitemanager.get_image_gallery_by_id(db, id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Not found with ID {id}")
    return {"gallery": [detail]}

#------------------------------------------------------------------------------------------------------------------------------------------- 


@router.get("/image_gallery/images/{user_id}", response_model=dict)
def get_our_team_image_url(user_id: int):
    
    profile_photo_filename = f"{user_id}.jpg"  
   
    return {"photo_url": f"{BASE_URL}/sitemanager/save_image_gallery/{profile_photo_filename}"}

#------------------------------------------------------------------------------------------------------------------------------------------- 

@router.post("/update/general_contact_details/{id}", response_model=GeneralContactDetailsSchema)
def update_general_contact_details(
        id: int,
        role_input: GeneralContactDetailsSchema,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    return db_sitemanager.update_general_contact_details(db, id, role_input, modified_by=user_id)

#------------------------------------------------------------------------------------------------------------------------------------------- 
@router.get("/get_general_contact_details", response_model=List[GeneralContactDetailsResponse])
def get_general_contact_details(db: Session = Depends(get_db)):
    
    contact_details = db_sitemanager.get_general_contact_details(db)
    return [{"contact_details": contact_details}]

#------------------------------------------------------------------------------------------------------------------------------------------- 

# @router.post('/save_trending_news/', response_model=TrendingNewsSchema)
# def save_trending_news(
        
#         id: int = 0,  # Default to 0 for add operation
#         data: TrendingNewsSchema = Depends(),
#         image_file: UploadFile = File(None),  
#         db: Session = Depends(get_db),
#         token: str = Depends(oauth2.oauth2_scheme)
# ):
    
#     """
#     Endpoint to save or update trending news.

#     Parameters:
#     - id (int, optional): The ID of the trending news to update. Defaults to 0 for add operation.
#     - data (TrendingNewsSchema): The data of the trending news to save or update.
#     - image_file (UploadFile, optional): The image file to upload for the trending news.
#     - db (Session): The database session.
#     - token (str): The authorization token.

#     Returns:
#     - TrendingNewsSchema: The saved or updated trending news.
#     """
#     # Check authorization
#     if not token:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
#     auth_info = authenticate_user(token)
#     user_id = auth_info["user_id"]
    
#     try:
#         if id == 0:
#             # Add operation
#             trending_news = db_sitemanager.add_trending_news(db, data, user_id)
            
#             # If image provided, save it
#             if image_file:
#                 file_content = image_file.file.read()
#                 file_path = f"{UPLOAD_DIR_NEWS}/{trending_news.id}.jpg"
#                 with open(file_path, "wb") as f:
#                     f.write(file_content)
#         else:
            
#             # Update operation
#             print("Update parameters:")
#             print("id:", id)
#             print("data:", data)
#             print("user_id:", user_id)
#             trending_news = db_sitemanager.update_trending_news(db, id, data, user_id)
            
#             # If image provided, save it
#             if image_file:
#                 file_content = image_file.file.read()
#                 file_path = f"{UPLOAD_DIR_NEWS}/{id}.jpg"
#                 with open(file_path, "wb") as f:
#                     f.write(file_content)
        
#         return trending_news
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed operation")

import logging

logger = logging.getLogger(__name__)

@router.post('/save_trending_news/', response_model=TrendingNewsSchema)
def save_trending_news(
        id: int = 0,  # Default to 0 for add operation
        data: TrendingNewsSchema = Depends(),
        image_file: UploadFile = File(None),  
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    """
    Endpoint to save or update trending news.
    """
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    try:
        if id == 0:
            # Add operation
            trending_news = db_sitemanager.add_trending_news(db, data,user_id)
        else:
            # Update operation
            trending_news = db_sitemanager.update_trending_news(db, id, data, user_id)
        
        # If image provided, save it
        if image_file:
            file_content = image_file.file.read()
            file_path = f"{UPLOAD_DIR_NEWS}/{trending_news.id}.jpg"
            with open(file_path, "wb") as f:
                f.write(file_content)
        
        return trending_news
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception("Failed to save or update trending news")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to save or update trending news")



#------------------------------------------------------------------------------------------------------------------------------------------- 


@router.get("/trending_news/images/{user_id}", response_model=dict)
def get_our_team_image_url(user_id: int):
    
    profile_photo_filename = f"{user_id}.jpg"  
    return {"photo_url": f"{BASE_URL}/sitemanager/save_trending_news/{profile_photo_filename}"}


#------------------------------------------------------------------------------------------------------------------------------------------- 

@router.get("/get_all_trending_news/" , response_model=List[TrendingNewsSchemaForDeletedStatus])
async def get_all_trending_news(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):
    return get_all_trending_news(db, deleted_status)



def get_all_trending_news(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(TrendingNews).filter(TrendingNews.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(TrendingNews).filter(TrendingNews.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(TrendingNews).all()
    else:
       
        raise ValueError("Invalid deleted_status")
		    
    
#------------------------------------------------------------------------------------------------------------------------------------------- 

@router.get("/get_trending_news_by_id/{id}", response_model=TrendingNewsResponse)
def get_trending_news_by_id(id: int,
                        db: Session = Depends(get_db)):
    
    detail = db_sitemanager.get_trending_news_by_id(db, id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Not found with ID {id}")
    return {"news": [detail]}

#------------------------------------------------------------------------------------------------------------------------------------------- 

@router.delete("/delete/trending_news_details/{id}")
def delete_trending_news_details(
                     
                     id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    
    
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    return db_sitemanager.delete_trending_news_details(db, id, deleted_by=user_id)


#------------------------------------------------------------------------------------------------------------------------------------------- 

@router.get("/get_legal_about_us", response_model=List[SiteLegalAboutUsBaseResponse])
def get_legal_about_us(db: Session = Depends(get_db)):
    
    about_us_legal_details = db_sitemanager.get_legal_about_us(db)
    return [{"legalaboutus": about_us_legal_details}]

#---------------------------------------------------------------------------------------------------------------
@router.post("/update/legal_about_us{id}", response_model=SiteLegalAboutUsBase)
def update_legal_about_us(id: int,
                     role_input: SiteLegalAboutUsBase,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    return db_sitemanager.update_legal_about_us(db, id, role_input)




@router.get("/home_banner", response_model=List[HomeBannerSchemaResponse])
def get_home_banner_details(
    db: Session = Depends(get_db)
    
):
    # Check authorization
   
    home_banner_details = db_sitemanager.get_all_home_banner(db)
    return home_banner_details



@router.post("/home_banner_update/{banner_id}", response_model=List[HomeBannerSchema])
def update_home_banner_details(        
        home_banner_data : HomeBannerSchema ,
        banner_id : int ,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    new_home_banner = db_sitemanager.update_home_banner(db, home_banner_data,banner_id,user_id)
        
    return [new_home_banner]





@router.get("/home_miracle_of_automation", response_model=List[HomeMiracleAutomationSchemaResponse])
def get_home_miracle_of_automation_details(
    db: Session = Depends(get_db)
   
    ):
    home_miracle_details = db_sitemanager.get_all_home_miracle(db)
    return home_miracle_details



@router.post("/home_miracle_of_automation_update/{miracle_id}", response_model=List[HomeMiracleAutomationSchema])
def update_home_miracle_details(        
        home_miracle_data : HomeMiracleAutomationSchema ,
        miracle_id : int ,
        db: Session = Depends(get_db),token: str = Depends(oauth2.oauth2_scheme)
):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    new_home_miracle = db_sitemanager.update_home_miracle(db, home_miracle_data,miracle_id,user_id)
        
    return [new_home_miracle]





@router.get("/get_home_trending_news_by_status/", response_model=List[HomeTrendingNewsSchemaResponse])
async def get_home_trending_news_details(
    deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db)
                           
):
    
    home_trending_news_details = db_sitemanager.get_all_home_trending_news(db,deleted_status)
    return  home_trending_news_details




@router.post('/save_home_trending_news/{news_id}', response_model=HomeTrendingNewsSchema)
def save_home_trending_news(
        request: Request,
        id: int = 0,  # Default to 0 for add operation
        trending_news_details: HomeTrendingNewsSchema = Depends(),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
    ):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
      
    try:
       
            # Add operation
        trending_news = db_sitemanager.save_home_trending_news(db, trending_news_details,id,user_id)
           
        return trending_news
    except Exception as e:
        error_detail = [{
            "loc": ["server"],
            "msg": "Internal server error",
            "type": "internal_server_error"
        }]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)



@router.delete("/delete/home_trending_news/{news_id}")
def delete_home_trending_news(
                     news_id: int,
                     db: Session = Depends(get_db),
                    token: str = Depends(oauth2.oauth2_scheme)
    ):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    
    return db_sitemanager.delete_home_trending_news(db, news_id,user_id)









@router.get("/get_prime_customer_by_status/",response_model=List[PrimeCustomerSchemaResponse])
async def get_prime_customer_details(
    deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
    db: Session = Depends(get_db)
):
    
    prime_customer_details = db_sitemanager.get_all_prime_customer(db,deleted_status)
    return prime_customer_details




@router.post('/save_prime_customer', response_model=PrimeCustomerSchema)
def save_prime_customer(
        request: Request,
        prime_customer_details: PrimeCustomerSchema = Depends(),
        image_file: UploadFile = File(None),
        db: Session = Depends(get_db),
        # token: str = Depends(oauth2.oauth2_scheme)
    ):
    # Check authorization
   
    
   
    # try:
       
            # Add operation
            prime_customer = db_sitemanager.save_prime_customer(db, prime_customer_details)
            if image_file:
               
                    id = prime_customer.id
                    file_content = image_file.file.read()
                    file_path = f"{UPLOAD_DIR_CUSTOMER}/{id}.jpg"
                    with open(file_path, "wb") as f:
                        f.write(file_content)
                
            return prime_customer
    


    
@router.post('/update_prime_customer/{id}', response_model=PrimeCustomerSchema)
def update_prime_customer(
        request: Request,
        id: int = 0,  # Default to 0 for add operation
        prime_customer_details: PrimeCustomerSchema = Depends(),
        db: Session = Depends(get_db)
        # token: str = Depends(oauth2.oauth2_scheme)
    ):
    # Check authorization
   
    
   
    try:
       
            # Add operation
            prime_customer = db_sitemanager.update_prime_customer(db, prime_customer_details,id)
            
            return prime_customer
    except Exception as e:
        error_detail = [{
            "loc": ["server"],
            "msg": "Internal server error",
            "type": "internal_server_error"
        }]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

#--------------------------   
    
@router.post('/update_prime_customer_image/{id}', response_model=PrimeCustomerSchema)
def update_prime_customer_image(
        id: int,
        image_file: UploadFile = File(...),  # Required image file
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    # Check if the user exists
    user = db.query(PrimeCustomer).filter(PrimeCustomer.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Save the new image
    file_content = image_file.file.read()
    file_path = f"{UPLOAD_DIR_CUSTOMER}/{user.id}.jpg"
    with open(file_path, "wb") as f:
        f.write(file_content)

    # Return the updated user data
    return user    


#--------------------------  

@router.get("/image/get_prime_customer_image/{id}", response_model=dict)
def get_prime_customer_image(
        id: int
        # token: str = Depends(oauth2.oauth2_scheme)
):

    
    profile_photo_filename = f"{id}.jpg"  
    
   
    return {"photo_url": f"{BASE_URL}/sitemanager/save_prime_customer/{profile_photo_filename}"}








@router.delete("/delete/prime_customer/{customer_id}")
def delete_prime_customer(
                     customer_id: int,
                     db: Session = Depends(get_db),
                    token: str = Depends(oauth2.oauth2_scheme)
):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    
    return db_sitemanager.delete_prime_customer(db, customer_id,user_id)



@router.get("/get_job_vacancies_by_status/", response_model=List[JobVacancieSchemaResponse])
async def get_job_vacancies_details(
    deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
    db: Session = Depends(get_db)
    
):
    # Check authorization
   
    job_vacancies_details = db_sitemanager.get_all_job_vacancies(db,deleted_status)
    return job_vacancies_details






@router.post('/save_job_vacancies/{id}', response_model=JobVacancieSchema)
def save_job_vacancies(
        request: Request,
        id: int = 0,  # Default to 0 for add operation
        job_vacancies_details: JobVacancieSchema = Depends(),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]

    try:
       
            # Add operation
            job_vacancies = db_sitemanager.save_job_vacancies(db, job_vacancies_details,id,user_id)
           
            return job_vacancies
    except Exception as e:
        error_detail = [{
            "loc": ["server"],
            "msg": "Internal server error",
            "type": "internal_server_error"
        }]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)




@router.delete("/delete/job_vacancies/{id}")
def delete_job_vacancies(
                     id: int,
                     db: Session = Depends(get_db),
                     
                    token: str = Depends(oauth2.oauth2_scheme)
):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    
    return db_sitemanager.delete_job_vacancies(db, id, user_id)


#------------------------------------------------------------------------------------------

#       JOB APPLICATION SECTION

#--------------------------------------------------------------------------------------------


@router.get("/job_application", response_model=List[JobApplicationSchemaResponse])
def get_job_application_details(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2.oauth2_scheme)
):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    job_application_details = db_sitemanager.get_all_job_application(db)
    return job_application_details



@router.post('/save_job_application', response_model=JobApplicationSchema)
def save_job_application(
        request: Request,
       
        job_application_details: JobApplicationSchema = Depends(),
        db: Session = Depends(get_db),
       
    ):
    
    
    try:
       
            # Add operation
        job_application = db_sitemanager.save_job_application(db, job_application_details)
           
        return job_application
    except Exception as e:
        error_detail = [{
            "loc": ["server"],
            "msg": "Internal server error",
            "type": "internal_server_error"
        }]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)




#------------------------------------------------------------------------------------------

#        MIRACLE FEATURES SECTION

#--------------------------------------------------------------------------------------------


@router.get("/get_miracle_features/", response_model=List[MiracleFeaturesSchemaResponse])
async def get_all_miracle_features(
    deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
    db: Session = Depends(get_db)
    
):
    # Check authorization
   
    miracle_features_details = db_sitemanager.get_all_miracle_features(db,deleted_status)
    return miracle_features_details




# @router.post('/save_miracle_features', response_model=MiracleFeaturesSchema)
# def save_miracle_features(
#         request: Request,
       
#         miracle_features_details: MiracleFeaturesSchema = Depends(),
#         db: Session = Depends(get_db),
       
#     ):
    
    
#     try:
       
#             # Add operation
#         miracle_features = db_sitemanager.save_miracle_features(db, miracle_features_details)
           
#         return miracle_features
#     except Exception as e:
#         error_detail = [{
#             "loc": ["server"],
#             "msg": "Internal server error",
#             "type": "internal_server_error"
#         }]
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)


@router.post('/save_miracle_features', response_model=MiracleFeaturesSchema)
def save_miracle_features(
        request: Request,
        id: int =0,
        miracle_features_details: MiracleFeaturesSchema = Depends(),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
    ):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    if id ==0:

      try:
       
            # Add operation
        miracle_features = db_sitemanager.save_miracle_features(db, miracle_features_details,user_id)
           
        return miracle_features
      except Exception as e:
        error_detail = [{
            "loc": ["server"],
            "msg": "Internal server error",
            "type": "internal_server_error"
        }]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)
    else:
        try:
       
            # Add operation
            miracle_features = db_sitemanager.update_miracle_features(db, miracle_features_details,id,user_id)
           
            return miracle_features
        except Exception as e:
            error_detail = [{
                "loc": ["server"],
                "msg": "Internal server error",
                "type": "internal_server_error"
            }]
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)



@router.delete("/delete/miracle_features/{miracle_id}")
def delete_miracle_features(
                     
                     team_id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    return db_sitemanager.delete_miracle_features(db, team_id, deleted_by=user_id)
     