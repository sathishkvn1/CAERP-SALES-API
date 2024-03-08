from fastapi import HTTPException, UploadFile,status
import os
from pathlib import Path
from UserDefinedConstants.user_defined_constants import DeletedStatus
from caerp_db.models import AboutUsDB, CompanyMaster,  ContactDetailsDB, FaqCategoryDB, FaqDB, GeneralContactDetailsDB, HomeBanner, HomeMiracleAutomation, HomeTrendingNews, ImageGalleryDB, JobApplication, JobVacancies, MiracleFeatures, OurDirectorDB, OurTeam, PrimeCustomer, PrivacyPolicyDB, SiteLegalAboutUs, SocialMediaURL, TermsAndConditionDB, TrendingNews
from caerp_schemas import  AboutUsUpdateSchema, CompanyMasterBase, FaqCategory, FaqSchema, GeneralContactDetailsSchema, HomeBannerSchema, HomeMiracleAutomationSchema, HomeTrendingNewsSchema, ImageGallerySchema, JobApplicationSchema, JobVacancieSchema, MiracleFeaturesSchema, OurDirectorSchema, OurTeamSchema, PrimeCustomerSchema, PrivacyPolicySchema, SiteLegalAboutUsBase, SocialMediaURLSchema, SubContentUpdateSchema, TermsAndConditionSchema, TrendingNewsSchema
from sqlalchemy.orm import Session
from datetime import datetime



import logging

logger = logging.getLogger(__name__)



def get_about_us_details(db: Session):
    return db.query(AboutUsDB).all()

def update_maincontent(db: Session, id: int, role_input: AboutUsUpdateSchema):
    about_us_update = db.query(AboutUsDB).filter(AboutUsDB.id == id).first()

    if about_us_update is None:
        raise HTTPException(status_code=404, detail="Role not found")

    for field, value in role_input.dict(exclude_unset=True).items():
        setattr(about_us_update, field, value)
    db.commit()
    db.refresh(about_us_update)

    return about_us_update


def update_subcontent(db: Session, id: int, role_input: SubContentUpdateSchema):
    sub_content_update = db.query(AboutUsDB).filter(AboutUsDB.id == id).first()

    if sub_content_update is None:
        raise HTTPException(status_code=404, detail="Role not found")

    for field, value in role_input.dict(exclude_unset=True).items():
        setattr(sub_content_update, field, value)

    db.commit()
    db.refresh(sub_content_update)

    return sub_content_update



def save_team(db: Session, team_data: OurTeamSchema, team_id: int, user_id: int):

    if team_id == 0:
        # Add operation
        team_data_dict = team_data.dict()
        team_data_dict["created_by"] = user_id
        team_data_dict["created_on"] = datetime.utcnow()
        new_team = OurTeam(**team_data_dict)
        db.add(new_team)
        db.commit()
        db.refresh(new_team)
        return new_team
    else:
        # Update operation
        team = db.query(OurTeam).filter(OurTeam.id == team_id).first()
        if team is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
        team_data_dict = team_data.dict(exclude_unset=True)
        for key, value in team_data_dict.items():
            setattr(team, key, value)
        team.modified_by = user_id
        team.modified_on = datetime.utcnow()
        db.commit()
        db.refresh(team)
        return team


def delete_team(db: Session, team_id: int, deleted_by: int):
    existing_team = db.query(OurTeam).filter(OurTeam.id == team_id).first()

    if existing_team is None:
        raise HTTPException(status_code=404, detail="Role not found")

    existing_team.is_deleted = 'yes'
    existing_team.deleted_by = deleted_by
    existing_team.deleted_on = datetime.utcnow()

    db.commit()

    return {
        "message": "Role marked as deleted successfully",

    }
    


def get_our_teams_by_id(db: Session, team_id: int):
    return db.query(OurTeam).filter(OurTeam.id == team_id).first()



import logging

logger = logging.getLogger(__name__)

def save_director(db: Session, director_data: OurDirectorSchema, director_id: int, user_id: int):

    try:
        if director_id == 0:
            # Add operation
            director_data_dict = director_data.dict()
            director_data_dict["created_by"] = user_id
            new_director = OurDirectorDB(**director_data_dict)
            db.add(new_director)
            db.commit()
            db.refresh(new_director)
            return new_director
        else:
            # Update operation
            director = db.query(OurDirectorDB).filter(OurDirectorDB.id == director_id).first()
            if director is None:
                raise HTTPException(status_code=404, detail="Director not found")
            
            director_data_dict = director_data.dict(exclude_unset=True)
            for key, value in director_data_dict.items():
                setattr(director, key, value)
            director.modified_by = user_id
            director.modified_on = datetime.utcnow()

            db.commit()
            db.refresh(director)

            return director
    except Exception as e:
        logger.error(f"Failed to save director: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed operation")




def delete_director_details(db: Session, id: int, deleted_by: int):
    existing_director = db.query(OurDirectorDB).filter(OurDirectorDB.id == id).first()

    if existing_director is None:
        raise HTTPException(status_code=404, detail="Director not found")

    existing_director.is_deleted = 'yes'
    existing_director.deleted_by = deleted_by
    existing_director.deleted_on = datetime.utcnow()

    db.commit()

    return {
        "message": "Deleted successfully",
    }




def get_directors_by_id(db: Session, id: int):
    return db.query(OurDirectorDB).filter(OurDirectorDB.id == id).first()



def save_faq_category(db: Session, faq_category_id: int, faq_category: FaqCategory, user_id: int):
    existing_category = None

    if faq_category_id == 0:
        # Add operation
        new_category = FaqCategoryDB(created_by=user_id, **faq_category.dict())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
    else:
        # Update operation
        existing_category = db.query(FaqCategoryDB).filter(FaqCategoryDB.id == faq_category_id).first()
        if existing_category is None:
            raise HTTPException(status_code=404, detail="FAQ Category not found")

        for field, value in faq_category.dict(exclude_unset=True).items():
            setattr(existing_category, field, value)

        existing_category.modified_by = user_id
        existing_category.modified_on = datetime.utcnow()
        db.commit()
        db.refresh(existing_category)
        return existing_category


def delete_faq_category(db: Session, id: int, deleted_by: int):
    faq_category = db.query(FaqCategoryDB).filter(FaqCategoryDB.id == id).first()

    if faq_category is None:
        raise HTTPException(status_code=404, detail="Director not found")

    faq_category.is_deleted = 'yes'
    faq_category.deleted_by = deleted_by
    faq_category.deleted_on = datetime.utcnow()

    db.commit()

    return {
        "message": "Deleted successfully",
    }




def get_all_faq_category_by_id(db: Session, id: int):
    return db.query(FaqCategoryDB).filter(FaqCategoryDB.id == id).first()

def save_faq(db: Session, id: int, faq: FaqSchema, user_id: int):
    if id == 0:
        # Add operation
        new_faq = FaqDB(created_by=user_id, **faq.dict())
        db.add(new_faq)
        db.commit()
        db.refresh(new_faq)
        return new_faq
    else:
        # Update operation
        existing_faq = db.query(FaqDB).filter(FaqDB.id == id).first()
        if existing_faq is None:
            raise HTTPException(status_code=404, detail="FAQ not found")
        
        for field, value in faq.dict(exclude_unset=True).items():
            setattr(existing_faq, field, value)
        
        existing_faq.modified_by = user_id
        existing_faq.modified_on = datetime.utcnow()
        db.commit()
        db.refresh(existing_faq)
        return existing_faq







def delete_faq(db: Session, id: int, deleted_by: int):
    faq_category = db.query(FaqDB).filter(FaqDB.id == id).first()

    if faq_category is None:
        raise HTTPException(status_code=404, detail="Director not found")

    faq_category.is_deleted = 'yes'
    faq_category.deleted_by = deleted_by
    faq_category.deleted_on = datetime.utcnow()

    db.commit()

    return {
        "message": "Deleted successfully",
    }
    

def get_all_faq_by_id(db: Session, id: int):
    return db.query(FaqDB).filter(FaqDB.id == id).first()


# def get_faqs_by_category(db: Session, faq_category_id: int):
#     faqs = db.query(FaqDB).filter(FaqDB.faq_category_id == faq_category_id).all()
#     return faqs

def save_social_media_url(db: Session, id: int, data: SocialMediaURLSchema, user_id: int):
    if id == 0:
        # Add operation
        new_url = SocialMediaURL(created_by=user_id, **data.dict())
        db.add(new_url)
    else:
        # Update operation
        existing_url = db.query(SocialMediaURL).filter(SocialMediaURL.id == id).first()
        if existing_url is None:
            raise HTTPException(status_code=404, detail="Social Media URL not found")
        
        for field, value in data.dict(exclude_unset=True).items():
            setattr(existing_url, field, value)
        
        existing_url.modified_by = user_id
        existing_url.modified_on = datetime.utcnow()
    
    db.commit()
    db.refresh(existing_url if id != 0 else new_url)
    return existing_url if id != 0 else new_url



def delete_social_media_url(db: Session, id: int, deleted_by: int):
    result = db.query(SocialMediaURL).filter(SocialMediaURL.id == id).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Director not found")

    result.is_deleted = 'yes'
    result.deleted_by = deleted_by
    result.deleted_on = datetime.utcnow()

    db.commit()

    return {
        "message": "Deleted successfully",
    }



def get_social_media_by_id(db: Session, id: int):
    return db.query(SocialMediaURL).filter(SocialMediaURL.id == id).first()


def update_contact_details(db: Session, id: int, role_input: AboutUsUpdateSchema,modified_by: int):
    result = db.query(ContactDetailsDB).filter(ContactDetailsDB.id == id).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Role not found")

    for field, value in role_input.dict(exclude_unset=True).items():
        setattr(result, field, value)
        
    result.modified_by = modified_by
    result.modified_on = datetime.utcnow()
    
    db.commit()
    db.refresh(result)

    return result



def get_contact_details(db: Session):
    return db.query(ContactDetailsDB).all()


def update_privacy_policy(db: Session, id: int, role_input: PrivacyPolicySchema,modified_by: int):
    result = db.query(PrivacyPolicyDB).filter(PrivacyPolicyDB.id == id).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Role not found")

    for field, value in role_input.dict(exclude_unset=True).items():
        setattr(result, field, value)
        
    result.modified_by = modified_by
    result.modified_on = datetime.utcnow()
    db.commit()
    db.refresh(result)

    return result



def get_privacy_policy(db: Session):
    return db.query(PrivacyPolicyDB).all()



def update_terms_and_condition(db: Session, id: int, role_input: TermsAndConditionSchema,modified_by: int):
    result = db.query(TermsAndConditionDB).filter(TermsAndConditionDB.id == id).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Role not found")

    for field, value in role_input.dict(exclude_unset=True).items():
        setattr(result, field, value)
        
    result.modified_by = modified_by
    result.modified_on = datetime.utcnow()
    db.commit()
    db.refresh(result)
    return result



def get_terms_and_condition(db: Session):
    return db.query(TermsAndConditionDB).all()


def add_images(db: Session, request: ImageGallerySchema, created_by: int):
    data = request.dict()
    data["created_by"] = created_by
    result = ImageGalleryDB(**data) 
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


def update_image_gallery(db: Session, id: int, input: ImageGallerySchema, modified_by: int):
    result = db.query(ImageGalleryDB).filter(ImageGalleryDB.id == id).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Director not found")

    for field, value in input.dict(exclude_unset=True).items():
        setattr(result, field, value)

    result.modified_by = modified_by
    result.modified_on = datetime.utcnow()

    db.commit()
    db.refresh(result)

    return result


def get_image_gallery_by_id(db: Session, id: int):
    return db.query(ImageGalleryDB).filter(ImageGalleryDB.id == id).first()


def delete_image_gallery_details(db: Session, id: int, deleted_by: int):
    result = db.query(ImageGalleryDB).filter(ImageGalleryDB.id == id).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Director not found")

    result.is_deleted = 'yes'
    result.deleted_by = deleted_by
    result.deleted_on = datetime.utcnow()

    db.commit()

    return {
        "message": "Deleted successfully",
    }



def update_general_contact_details(
        db: Session,
        id: int,
        role_input: GeneralContactDetailsSchema,
        modified_by: int
):
    result = db.query(GeneralContactDetailsDB).filter(GeneralContactDetailsDB.id == id).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Role not found")

    for field, value in role_input.dict(exclude_unset=True).items():
        setattr(result, field, value)
        
    result.modified_by = modified_by
    result.modified_on = datetime.utcnow()
    
    db.commit()
    db.refresh(result)
    
    return result



def get_general_contact_details(db: Session):
    return db.query(GeneralContactDetailsDB).all()


def add_trending_news(db: Session, request: TrendingNewsSchema, created_by: int):
    data = request.dict()
    data["created_by"] = created_by
    
    add_news = TrendingNews(**data) 
    db.add(add_news)
    db.commit()
    db.refresh(add_news)
    return add_news



def update_trending_news(db: Session, id: int, input: TrendingNewsSchema, modified_by: int):
    result = db.query(TrendingNews).filter(TrendingNews.id == id).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Director not found")

    for field, value in input.dict(exclude_unset=True).items():
        setattr(result, field, value)

    result.modified_by = modified_by
    result.modified_on = datetime.utcnow()

    db.commit()
    db.refresh(result)

    return result



def get_trending_news_by_id(db: Session, id: int):
    return db.query(TrendingNews).filter(TrendingNews.id == id).first()

# ##########################################test


def delete_trending_news_details(db: Session, id: int, deleted_by: int):
    result = db.query(TrendingNews).filter(TrendingNews.id == id).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Director not found")

    result.is_deleted = 'yes'
    result.deleted_by = deleted_by
    result.deleted_on = datetime.utcnow()

    db.commit()

    return {
        "message": "Deleted successfully",
    }


def get_legal_about_us(db: Session):
    return db.query(SiteLegalAboutUs).all()



def update_legal_about_us(db: Session, id: int, role_input: SiteLegalAboutUsBase):
    about_us_update = db.query(SiteLegalAboutUs).filter(SiteLegalAboutUs.id == id).first()

    if about_us_update is None:
        raise HTTPException(status_code=404, detail="Not found")

    for field, value in role_input.dict(exclude_unset=True).items():
        setattr(about_us_update, field, value)
    db.commit()
    db.refresh(about_us_update)

    return about_us_update




def get_all_home_banner(db: Session):
    return db.query(HomeBanner).all()


def update_home_banner(db: Session, request: HomeBannerSchema, id: int, user_id : int):
    home_banner = db.query(HomeBanner).filter(HomeBanner.id == id).first()
    if home_banner is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Home Banner not found")
    home_banner_data_dict = request.dict()
    for key, value in home_banner_data_dict.items():
            setattr(home_banner, key, value)
    
    db.commit()
    db.refresh(home_banner)
    return home_banner



def get_all_home_miracle(db: Session):
    return db.query(HomeMiracleAutomation).all()


def update_home_miracle(db: Session, request: HomeMiracleAutomationSchema, id: int, user_id: int):
    home_miracle = db.query(HomeMiracleAutomation).filter(HomeMiracleAutomation.id == id).first()
    if home_miracle is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Home Miracle not found")
    home_miracle_data_dict = request.dict()
    for key, value in home_miracle_data_dict.items():
            setattr(home_miracle, key, value)
    
    db.commit()
    db.refresh(home_miracle)
    return home_miracle





def get_all_home_trending_news(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(HomeTrendingNews).filter(HomeTrendingNews.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(HomeTrendingNews).filter(HomeTrendingNews.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(HomeTrendingNews).all()
    else:
        # Handle invalid state or raise an error
        raise ValueError("Invalid deleted_status")







def delete_home_trending_news(db: Session, news_id: int, user_id: int):
    existing_home_news = db.query(HomeTrendingNews).filter(HomeTrendingNews.id == news_id).first()

    if existing_home_news is None:
        raise HTTPException(status_code=404, detail="Trending News not found")

    existing_home_news.is_deleted = 'yes'
    existing_home_news.deleted_by = user_id
    existing_home_news.deleted_on = datetime.utcnow()
   
    db.commit()

    return {
        "message": "Home Trending News marked as deleted successfully",

    }






def get_all_prime_customer(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(PrimeCustomer).filter(PrimeCustomer.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(PrimeCustomer).filter(PrimeCustomer.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(PrimeCustomer).all()
    else:
        # Handle invalid state or raise an error
        raise ValueError("Invalid deleted_status")



def save_prime_customer(db: Session, customer_data: PrimeCustomerSchema):

   
        # Add operation
        customer_data_dict = customer_data.dict()
        customer_data_dict["created_on"] = datetime.utcnow()
        customer_data_dict["created_by"] =1
        new_customer = PrimeCustomer(**customer_data_dict)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer
    

def update_prime_customer(db: Session, customer_data: PrimeCustomerSchema, id: int):

        # Update operation
        customer = db.query(PrimeCustomer).filter(PrimeCustomer.id == id).first()
        if customer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        customer_data_dict = customer_data.dict(exclude_unset=True)
        for key, value in customer_data_dict.items():
            setattr(customer, key, value)
        
        db.commit()
        db.refresh(customer)
        return customer
    
    

def delete_prime_customer(db: Session, customer_id: int,deleted_by : int):
    existing_customer = db.query(PrimeCustomer).filter(PrimeCustomer.id == customer_id).first()

    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Prime Customer not found")

    existing_customer.is_deleted = 'yes'
    existing_customer.deleted_by = deleted_by
    existing_customer.deleted_on = datetime.utcnow()
   
    db.commit()

    return {
        "message": "Prime Customer marked as deleted successfully",

    }
    

def get_all_job_vacancies(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(JobVacancies).filter(JobVacancies.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(JobVacancies).filter(JobVacancies.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(JobVacancies).all()
    else:
        # Handle invalid state or raise an error
        raise ValueError("Invalid deleted_status")




def save_job_vacancies(db: Session, job_data: JobVacancieSchema, id: int, user_id: int):

    if  id == 0:
        # Add operation
        job_data_dict = job_data.dict()
        job_data_dict["created_on"] = datetime.utcnow()
        job_data_dict["created_by"] = user_id
        new_vacancy = JobVacancies(**job_data_dict)
        db.add(new_vacancy)
        db.commit()
        db.refresh(new_vacancy)
        return new_vacancy
    else:
        # Update operation
        vacancies = db.query(JobVacancies).filter(JobVacancies.id == id).first()
        if vacancies is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vacancies not found")
        job_data_dict = job_data.dict(exclude_unset=True)
        for key, value in job_data_dict.items():
            setattr(vacancies, key, value)
        
        db.commit()
        db.refresh(vacancies)
        return vacancies


def save_home_trending_news(db: Session, data: HomeTrendingNewsSchema, id: int, user_id: int):

    if  id == 0:
        # Add operation
        data_dict = data.dict()
        data_dict["created_on"] = datetime.utcnow()
        data_dict["created_by"] = user_id
        new_data = HomeTrendingNews(**data_dict)
        db.add(new_data)
        db.commit()
        db.refresh(new_data)
        return new_data
    else:
        # Update operation
        news = db.query(HomeTrendingNews).filter(HomeTrendingNews.id == id).first()
        if news is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="news not found")
        data_dict = data.dict(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(news, key, value)
        
        db.commit()
        db.refresh(news)
        return news


def delete_job_vacancies(db: Session, vacancy_id: int,deleted_by: int):
    existing_vacancies = db.query(JobVacancies).filter(JobVacancies.id == vacancy_id).first()

    if existing_vacancies is None:
        raise HTTPException(status_code=404, detail="Job Vacancies not found")

    existing_vacancies.is_deleted = 'yes'
    existing_vacancies.deleted_by = deleted_by
    existing_vacancies.deleted_on = datetime.utcnow()
   
    db.commit()

    return {
        "message": "Job Vacancies marked as deleted successfully",

    }
    
    
#----------------------------------------------------------------------------------------

        # Job       Application 
#---------------------------------------------------------------------------------------



def get_all_job_application(db: Session):
    return db.query(JobApplication).all()



def save_job_application(db: Session, job_application_data: JobApplicationSchema):

    
        # Add operation
        job_application_dict = job_application_data.dict()
       
        job_application = JobApplication(**job_application_dict)
        db.add(job_application)
        db.commit()
        db.refresh(job_application)
        return job_application



#------------------------------------------------------------------------
    #Miracle  Features

#------------------------------------------------------------------------




def get_all_miracle_features(db: Session):
    return db.query(MiracleFeatures).all()



def save_miracle_features(db: Session, miracle_features_data: MiracleFeaturesSchema):

    
        # Add operation
        miracle_features_dict = miracle_features_data.dict()
       
        miracle_features = MiracleFeatures(**miracle_features_dict)
        db.add(miracle_features)
        db.commit()
        db.refresh(miracle_features)
        return miracle_features