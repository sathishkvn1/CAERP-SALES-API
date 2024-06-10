
from enum import Enum
from pydantic import BaseModel,Field
from typing import List,Optional, Union,Dict
from datetime import date, datetime
from UserDefinedConstants.user_defined_constants import BooleanFlag




class CountryCreate(BaseModel):
    id: int
    country_name_english: str
    country_name_arabic: Optional[str]
    iso2_code: Optional[str]
    iso3_code: Optional[str]
    isd_code: Optional[str]

    class Config:
        orm_mode  : True

class CountryDetail(BaseModel):
    id: int
    country_name_english: str
    country_name_arabic: Optional[str]
    iso2_code: Optional[str]
    iso3_code: Optional[str]
    isd_code: Optional[str]

    class Config:
        orm_mode  : True
        
        

        
class StateDetail(BaseModel):
    id: int
    country_id: int
    state_name: str

    class Config:
        orm_mode  : True
 
#  get  the states based on country       
class StatesByCountry(BaseModel):
    country_id: int
    states: List[StateDetail]

    class Config:
        orm_mode = True

  


class DistrictDetail(BaseModel):
    id: int
    district_name: str

    class Config:
        orm_mode = True

class DistrictDetailByState(BaseModel):
    state_id: int
    districts: List[DistrictDetail]

    class Config:
        orm_mode = True
        
class DistrictResponse(BaseModel):
    district: DistrictDetail


# class CityDetail(BaseModel):
#     id: int
#     country_id: int
#     state_id: int
#     city_name: str

#     class Config:
#         orm_mode = True
        
class CityDetail(BaseModel):
    id: int
    city_name: str

    class Config:
        orm_mode = True
        
class CityResponse(BaseModel):
    country_id: int
    state_id: int
    cities: List[CityDetail]
        

 
class TalukDetail(BaseModel):
    id: int
    district_id: int
    taluk_name: str

class TalukResponse(BaseModel):
    state_id: int
    taluks: List[TalukDetail]

class TalukResponseByDistrict(BaseModel):
    district_id: int
    taluks: List[Dict[str, str]]   
       

class CurrencyDetail(BaseModel):
    id: int
    short_name: str
    long_name: str
    currency_symbol: Optional[str]

    class Config:
        orm_mode = True
        
class NationalityDetail(BaseModel):
    id: int
    nationality :str

    class Config:
        orm_mode = True
        
class PostOfficeTypeDetail(BaseModel):
    id: int
    office_type: str

    class Config:
        orm_mode = True

class PostalDeliveryStatusDetail(BaseModel):
    id: int
    delivery_status: str

    class Config:
        orm_mode = True
        
class PostalCircleDetail(BaseModel):
    id: int
    circle_name: str

    class Config:
        orm_mode = True

class PostalRegionDetail(BaseModel):
    id: int
    circle_id: int
    region_name: str

    class Config:
        orm_mode = True

class PostalDivisionDetail(BaseModel):
    id: int
    circle_id: int
    region_id: int
    division_name: str



class PostOfficeDetail(BaseModel):
    id: int
    post_office_name: str
    pin_code: str
    post_office_type_id: int
    office_type: str
    postal_delivery_status_id: int
    delivery_status: str
    postal_division_id: int
    division_name: str
    postal_region_id: int
    region_name: str
    postal_circle_id: int
    circle_name: str
    taluk_id: int
    taluk_name: str
    district_id: int
    district_name: str
    state_id: int
    state_name: str
    contact_number: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    
    class Config:
        orm_mode = True
        
class PincodeDetails(BaseModel):
    pincode: str

    taluk: Dict[str, Union[int, str]]
    division:Dict[str,Union[int,str]]
    region:Dict[str,Union[int,str]]
    postalcircle:Dict[str,Union[int,str]]
    district:Dict[str,Union[int,str]]
    state:Dict[str,Union[int,str]]
    country:Dict[str,Union[int,str]]
    post_offices: List[Dict[str, Union[int, str]]]


class PostOfficeListResponse(BaseModel):
    pincode_details: List[PincodeDetails]

    class Config:
        orm_mode = True


    

class AboutUsSchema(BaseModel):
    id: int
    about_us: str
    sub_head_description: Optional[str]
    our_mission: Optional[str]
    our_vision: Optional[str]
    our_target: Optional[str]
    footer_description: Optional[str]

    class Config:
        orm_mode = True

class AboutUsResponse(BaseModel):
    aboutus: List[AboutUsSchema]
    



    

class GenderSchema(BaseModel):
    id: int
    gender: str

    class Config:
        orm_mode = True

class GenderSchemaResponse(BaseModel):
    gender: List[GenderSchema]
    

class UserRoleSchema(BaseModel):
    id: int
    role: str

    class Config:
        orm_mode = True

class UserRoleListResponse(BaseModel):
    roles: List[UserRoleSchema]
    

class UserRoleInputSchema(BaseModel):
    role: str

    
class UserRoleUpdateSchema(BaseModel):
    role: Optional[str] = None


class UserRoleDeleteSchema(BaseModel):
    role: Optional[str] = None
    deleted_by: Optional[int] = None
    deleted_on: Optional[datetime] = None
    
class UserRoleListResponses(BaseModel):
    id: int
    role: str

    class Config:
        orm_mode = True
        
class DesignationSchema(BaseModel):
    id: int
    designation: str
    
    class Config:
        orm_mode = True
    
class DesignationListResponse(BaseModel):
    designations: List[DesignationSchema]


class DesignationListResponses(BaseModel):
    id: int
    designation: str

    class Config:
        orm_mode = True
        
        
class DesignationInputSchema(BaseModel):
    designation: str
    

class User(BaseModel):
    id: int
    username: str
        
class DesignationUpdateSchema(BaseModel):
    designation: Optional[str] = None



class DesignationDeleteSchema(BaseModel):
    designation: Optional[str] = None
    deleted_by: Optional[int] = None
    deleted_on: Optional[datetime] = None
    

# class AdminUserCreateSchema(BaseModel):
#     first_name: str
#     last_name: str
#     gender_id: int
#     user_name: str
#     password: str
#     role_id: int
#     designation_id: int
#     address_line_1: Optional[str] = None
#     address_line_2: Optional[str] = None
#     address_line_3: Optional[str] = None
#     address_line_4: Optional[str] = None
#     pin_code: str
#     city_id:int
#     taluk_id:int
#     district_id:int
#     state_id:int
#     country_id:int
#     mobile_number: Optional[str] = None
#     whatsapp_number: Optional[str] = None
#     email_id: Optional[str] = None

class AdminUserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    gender_id: int
    user_name: str
    password: str
    role_id: int
    designation_id: int
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    address_line_3: Optional[str] = None
    address_line_4: Optional[str] = None
    pin_code: str
    city_id:int
    taluk_id:int
    district_id:int
    state_id:int
    country_id:int
    mobile_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    email_id: Optional[str] = None
    

   
# class AdminUserUpdateSchema(BaseModel):
#     first_name: str
#     last_name: str
#     gender_id: int
#     user_name: str
#     role_id: int
#     designation_id: int
#     address: Optional[str] = None
#     mobile_number: Optional[str] = None
#     whatsapp_number: Optional[str] = None
#     email_id: Optional[str] = None
    
class AdminUserUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    gender_id: int
    user_name: str
    role_id: int
    designation_id: int
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    address_line_3: Optional[str] = None
    address_line_4: Optional[str] = None
    pin_code: str
    city_id:int
    taluk_id:int
    district_id:int
    state_id:int
    country_id:int
    mobile_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    email_id: Optional[str] = None
    

class AdminUserChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str
    
class UserImageUpdateSchema(BaseModel):
    image_file: bytes

class AdminUserDeleteSchema(BaseModel):
    message: str
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]
    

    
class AdminUserListResponse(BaseModel):
    users: List[AdminUserCreateSchema]
    
class UserLoginSchema(BaseModel):
    user_name: str
    password: str

class UserLoginResponseSchema(BaseModel):
    message: str
    user_id: int
    token: str  

class ProtectedResourceResponse(BaseModel):
    message: str
    user_id: int
    
class AboutUsUpdateSchema(BaseModel):
    about_us: Optional[str] = None


class SubContentUpdateSchema(BaseModel):

    sub_head_description: Optional[str]
    our_mission: Optional[str]
    our_vision: Optional[str]
    our_target: Optional[str]
    footer_description: Optional[str]
    
    
class AdminMainMenuCreate(BaseModel):
    main_menu: str
    main_menu_has_sub_menu: str
    main_menu_display_order: int
    main_menu_page_link: str

    class Config:
        orm_mode = True
        
        
class  AdminMainMenuDeleteSchema(BaseModel):
    message: str
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]

    
class AdminSubMenuCreate(BaseModel):
    # main_menu_id: int
    sub_menu: str
    sub_menu_has_sub_menu: str = 'no'
    sub_menu_display_order: int
    sub_menu_page_link: Optional[str]
    
    

class AdminSubMenuDeleteSchema(BaseModel):
    message: str
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]
    
class TestSchema(BaseModel):
    id: int
    name: str
    

class OurTeamSchema(BaseModel):
    full_name: str
    designation_id: Optional[int] = None
    qualification_id: Optional[int] = None
    description: Optional[str] = None
    experience: Optional[str] = None
    
class OurTeamSchemaforDelete(BaseModel):
    id: Optional[int]
    full_name: str
    designation_id: Optional[int]
    qualification_id: Optional[int]
    description: Optional[str]
    experience: Optional[str]
    created_by: int
    created_on: datetime
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    is_deleted: str
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]

    class Config:
        orm_mode = True
        
        
    
class OurTeamSchemaResponse(BaseModel):
    team: List[OurTeamSchemaforDelete]

class OurDirectorSchema(BaseModel):
    full_name: str
    designation_id: Optional[int] = None
    qualification_id: Optional[int] = None
    description: Optional[str] = None
    experience: Optional[str] = None
    
    
class OurDirectorSchemaforDelete(BaseModel):
    id: Optional[int]
    full_name: str
    designation_id: Optional[int]
    qualification_id: Optional[int]
    description: Optional[str]
    experience: Optional[str]
    created_by: int
    created_on: datetime
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    is_deleted: str
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]

    class Config:
        orm_mode = True
    
    
class OurDirectorResponse(BaseModel):
    director: List[OurDirectorSchemaforDelete]
    
    
class FaqCategory(BaseModel):
    faq_category: str
    
    

class FaqSchema(BaseModel):
    faq: str
    faq_answer: Optional[str] = None
    faq_category_id: int
    
    
class FaqCategorySchemaForDelete(BaseModel):
    id: int
    faq_category: str
    created_by: int
    created_on: datetime
    modified_by: Optional[int] = None
    modified_on: Optional[datetime] = None
    is_deleted: str
    deleted_by: Optional[int] = None
    deleted_on: Optional[datetime] = None
    
class FaqCategoryResponse(BaseModel):
    faq: List[FaqCategorySchemaForDelete]

class FaqSchemaForDelete(BaseModel):
    id: int
    faq: str
    faq_answer: Optional[str] = None
    faq_category_id: int
    created_by: int
    created_on: datetime
    modified_by: Optional[int] = None
    modified_on: Optional[datetime] = None
    is_deleted: str = 'no'
    deleted_by: Optional[int] = None
    deleted_on: Optional[datetime] = None
    
    
class FaqResponse(BaseModel):
    faq: List[FaqSchemaForDelete]

    
class TrendingNewsSchema(BaseModel):
    title: str
    details: Optional[str] = None
    class Config:
        orm_mode = True
        



    

class SocialMediaURLSchema(BaseModel):
    social_media: str
    social_media_url: Optional[str]
    faicon: Optional[str]

    class Config:
        orm_mode = True

class SocialMediaSchema(BaseModel):
    id: int
    social_media: str
    social_media_url: Optional[str]
    faicon: Optional[str]
    created_by: int
    created_on: datetime
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    is_deleted: str
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]

    class Config:
        orm_mode = True
        
class SocialMediaResponse(BaseModel):
    social_media: List[SocialMediaSchema]
  
class ContactDetailsSchema(BaseModel):
    contact_us: str
    map_iframe: Optional[str] = None
    email_id: Optional[str] = None
    address: Optional[str] = None
    office_phone: Optional[str] = None
    customer_care_no: Optional[str] = None
    telephone: Optional[str] = None
    mobile_no: Optional[str] = None
    whatsapp_no: Optional[str] = None
    contact_side_description: Optional[str] = None
    contact_main_description: Optional[str] = None
    client_site_address_text: Optional[str] = None
    site_url: Optional[str] = None  
    class Config:
        orm_mode = True


class ContactDetailResponse(BaseModel):
    contact: List[ContactDetailsSchema]
    

class PrivacyPolicySchema(BaseModel):
    privacy_policy: str

    class Config:
        orm_mode = True
        
class PrivacyPolicyResponse(BaseModel):
    privacy_policy: List[PrivacyPolicySchema]
    
    

class TermsAndConditionSchema(BaseModel):
    terms_and_condition: str

    class Config:
        orm_mode = True
        
class TermsAndConditionResponse(BaseModel):
    terms_and_condition: List[TermsAndConditionSchema]
    
class ImageGallerySchema(BaseModel):
    title: str
    description: Optional[str] = None

    class Config:
        orm_mode = True
        
class GeneralContactDetailsSchema(BaseModel):
    general_contact_details: str
    class Config:
        orm_mode = True
        
class GeneralContactDetailsResponse(BaseModel):
    contact_details: List[GeneralContactDetailsSchema]
    
    
    
class CompanyMasterBase(BaseModel):
    company_name: str
    state_id: int
    country_id: int
    base_currency_id: int
    suffix_symbol_to_amount: str = 'no'
    show_amount_in_millions: str = 'no'
    book_begin_date: date
    created_by: int
    is_deleted: str = 'no'

class UserRoleForDelete(BaseModel):
    id: int
    role: str
    created_by: int
    created_on: datetime
    modified_by: Optional[int] = None
    modified_on: Optional[datetime] = None
    is_deleted: str = 'no'
    deleted_by: Optional[int] = None
    deleted_on: Optional[datetime] = None
    


class AdminUserBaseForDelete(BaseModel):
    id: int
    first_name: str
    last_name: str
    gender_id: int
    user_name: str
    role_id: int
    designation_id: int
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    address_line_3: Optional[str] = None
    address_line_4: Optional[str] = None
    pin_code: str
    city_id:int
    taluk_id:int
    district_id:int
    state_id:int
    country_id:int
    mobile_number: Optional[str] = None
    whatsapp_number: Optional[str] = None
    email_id: Optional[str] = None
    created_by: int
    created_on: datetime
    modified_by: Optional[int] = None
    modified_on: Optional[datetime] = None
    is_deleted: str = 'no'
    deleted_by: Optional[int] = None
    deleted_on: Optional[datetime] = None
    
	


class DesignationSchemaForDelete(BaseModel):
    id: int
    designation:str
    created_by: int
    created_on: datetime
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    is_deleted: str
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]

    class Config:
        orm_mode = True
        
        
class LoginRequest(BaseModel):
    username: str
    password: str
    user_type: str
    
class ImageGallerySchemaForGet(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_by: int
    created_on: datetime
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    is_deleted: str
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]


class ImageGalleryResponse(BaseModel):
    gallery: List[ImageGallerySchemaForGet]  
    
class TrendingNewsSchemaForDeletedStatus(BaseModel):
    id: int
    title: str
    details: Optional[str]
    created_by: int
    created_on: datetime
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    is_deleted: str
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]

    class Config:
        orm_mode = True
        
        
class TrendingNewsResponse(BaseModel):
    news: List[TrendingNewsSchemaForDeletedStatus]  
    
    
    
class ClientMenuBase(BaseModel):
    menu: str
    has_sub_menu: str
    display_order: int
    page_link: str

    class Config:
        orm_mode = True
        
            
class ClientMenu(BaseModel):
    id: int
    menu: str
    has_sub_menu: str
    display_order: int
    page_link: Optional[str] = None
    created_by: int
    created_on: datetime
    modified_by: Optional[int] = None
    modified_on: Optional[datetime] = None
    is_deleted: str
    deleted_by: Optional[int] = None
    deleted_on: Optional[datetime] = None

    class Config:
        orm_mode = True

        
class ClientMenuResponse(BaseModel):
    menu: List[ClientMenu]  

class SiteLegalAboutUsBase(BaseModel):
    nature_of_business: str
    legal_status_of_the_firm: Optional[str] = None
    gst_in: Optional[str] = None
    pan_number: Optional[str] = None
    trade_mark: Optional[str] = None
    startup_reg_number: Optional[str] = None
    total_number_of_employees: Optional[str] = None
    annual_turn_over: Optional[str] = None
    cin: Optional[str] = None
    tan_number: Optional[str] = None
    iso_number: Optional[str] = None
    startup_mission_number: Optional[str] = None
    year_of_establishment: Optional[str] = None
    import_export_code: Optional[str] = None
    msme: Optional[str] = None
    esic: Optional[str] = None
    epf: Optional[str] = None
    
    
class SiteLegalAboutUsBaseResponse(BaseModel):
    legalaboutus: List[SiteLegalAboutUsBase]
    

class PublicMainMenuCreate(BaseModel):
    menu: str
    has_sub_menu: str
    display_order: int
    page_link: str

    class Config:
        orm_mode = True
        
class PublicSubMenuCreate(BaseModel):
    main_menu_id: int
    sub_menu: str
    has_sub_menu: str = 'no'
    display_order: int
    page_link: Optional[str]

class PublicSubSubMenuCreate(BaseModel):
    sub_menu_id: int
    sub_sub_menu: str
    display_order: int
    page_link: Optional[str]
    

    
    
class CustomerRegisterBase(BaseModel):
    
    first_name: str
    last_name: Optional[str] = None 
    gender_id: Optional[int] = None
    mobile_number: Optional[str] = None
    pin_code: Optional[int] = None
    post_office_id: Optional[int] = None
    taluk_id: Optional[int] = None
    district_id: Optional[int] = None
    state_id: Optional[int] = None
    country_id: Optional[int] = None
    email_id: Optional[str] = None
    password: str

class CustomerRegisterBaseForUpdate(BaseModel):
    
    first_name: str
    last_name: Optional[str] = None 
    gender_id: Optional[int] = None
    mobile_number: Optional[str] = None
    pin_code: Optional[int] = None
    post_office_id: Optional[int] = None
    taluk_id: Optional[int] = None
    district_id: Optional[int] = None
    state_id: Optional[int] = None
    country_id: Optional[int] = None
    customer_type_id: Optional[int] = None
    email_id: Optional[str] = None

    


class CustomerRegisterSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    gender_id: int
    mobile_number: str
    is_mobile_number_verified: str = 'no'
    email_id: Optional[str] = None
    is_email_id_verified: str = 'no'
    pin_code: int
    post_office_id: int
    taluk_id: int
    district_id: int
    state_id: int
    country_id: int
    password: str
    customer_type_id: int
    created_on: Optional[datetime] = None
    expiring_on: Optional[datetime] = None
    is_deleted: str = 'no'
    is_active: str = 'yes'
   

class CustomerRegisterListSchema(BaseModel):
    
    customers: List[CustomerRegisterSchema]
    
class CustomerCompanyProfileSchema(BaseModel):
    
    company_name: str
    pin_code: str
    city_id: int
    post_office_id: int
    taluk_id: int
    district_id: int
    state_id: int
    country_id: int
    address_line_1: str
    address_line_2: Optional[str] = None
    address_line_3: Optional[str] = None
    address_line_4: Optional[str] = None
    pan_number: Optional[str] = None
    pan_card_type_id: Optional[int] = None
    gst_number: Optional[str] = None
    company_description: Optional[str] = None
    about_company: Optional[str] = None
    company_mobile: str
    company_email_id: str
    company_web_site: Optional[str] = None
    
    
class CustomerCompanyProfileSchemaResponse(BaseModel):
    customer: List[CustomerCompanyProfileSchema]
    
    

class CompanyProfileSchemaForGet(BaseModel):
    id: int
    customer_id: int
    company_name: str
    pin_code: str
    city_id: int
    post_office_id: int
    taluk_id: int
    district_id: int
    state_id: int
    country_id: int
    address_line_1: str
    address_line_2: Optional[str]
    address_line_3: Optional[str]
    address_line_4: Optional[str]
    pan_number: Optional[str]
    pan_card_type_id: Optional[int]
    gst_number: Optional[str]
    company_description: Optional[str]
    about_company: Optional[str]
    company_mobile: str
    company_email_id: str
    company_web_site: Optional[str]

class CustomerNewsBase(BaseModel):
    title: str
    details: str
   

# class ImageGallerySchemaForGet(BaseModel):
#     id: int
#     title: str
#     description: Optional[str]
#     created_by: int
#     created_on: datetime
#     modified_by: Optional[int]
#     modified_on: Optional[datetime]
#     is_deleted: str
#     deleted_by: Optional[int]
#     deleted_on: Optional[datetime]
    
class CustomerNewsBaseForGet(BaseModel):
    id: int
    title: str
    details: str
    is_active: str 
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    created_by: int
    created_on: datetime
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]
    
    
class CustomerNewsResponse(BaseModel):
    news: List[CustomerNewsBaseForGet]  
    
    
class CustomerLoginRequest(BaseModel):
    email: str
    password: str
    
class ClientUserChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str
    
class FAQBase(BaseModel):
    faq: str
    faq_answer: str

class FAQCategoryID(BaseModel):
    faq_category_id: int
    
    
class CustomerSalesQueryBase(BaseModel):
    query_date: datetime 
    contact_person_name: str
    company_name: Optional[str] = None
    email_id: Optional[str] = None
    mobile_number: Optional[int] = None
    pin_code: Optional[int] = None
    city_id: int
    post_office_id: int
    taluk_id: int
    district_id: int
    state_id: int
    country_id: int
    
    class Config:
        orm_mode = True
    
class CustomerSalesQueryForGet(BaseModel):
    query_date: date
    contact_person_name: str
    company_name: Optional[str] = None
    email_id: Optional[str] = None
    mobile_number: Optional[int] = None
    pin_code: Optional[int] = None
    city_id: int
    post_office_id: int
    taluk_id: int
    district_id: int
    state_id: int
    country_id: int
    is_read: str = 'no'
    read_by: Optional[int] = None
    read_on: Optional[datetime] = None
    is_replied: Optional[str] = None
    replied_by: Optional[int] = None

    class Config:
        orm_mode = True
        
        
class InstallmentMasterBase(BaseModel):
    product_id: int
    number_of_installments: int
    is_active: BooleanFlag = 'no'
    active_from_date: Optional[date] = None
    
    
class InstallmentMasterForGet(BaseModel):
    id:int
    number_of_installments: int
    is_active: BooleanFlag = 'no'
    active_from_date: Optional[date] = None
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    created_by: int
    is_deleted: str
    created_on: datetime
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]
     
        
        
        
        # //////////////////////////////////////////////
        
class  ProductMasterSchema(BaseModel):
    product_code     : Optional[str]
    product_name     : Optional[str]
    category_id      : Optional[int]
    product_description_main : Optional[str]
    product_description_sub  :Optional[str]
    has_module       : Optional[str]
    

  
class  ProductMasterSchemaResponse(BaseModel):
    id               : int
    product_code     : Optional[str]
    product_name     : Optional[str]
    category_id      : Optional[int]
    product_description_main : Optional[str]
    product_description_sub  :Optional[str]
    has_module : Optional[str]
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    created_by: int
    is_deleted: str
    created_on: datetime
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]
     


 
# class  ProductCategorySchema(BaseModel):
    
#     category_name     : Optional[str]
#     created_on        : Optional[datetime]
    
class  ProductCategorySchema(BaseModel):
    
    category_name     : Optional[str]
    


 
class  ProductCategorySchemaResponse(BaseModel):
    id               : int
    category_name     : Optional[str]
    created_on        : Optional[datetime]
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    created_by: int
    is_deleted: str
    created_on: datetime
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]
    
class ProductModuleSchema(BaseModel):

    product_master_id   : int
    module_name         : str
    module_description  : str
    display_order       : int
    

class ProductModuleSchemaResponse(BaseModel):

    id                  : int 
    product_master_id   : int
    module_name         : str
    module_description  : str
    display_order       : int
    modified_by         : Optional[int]
    modified_on         : Optional[datetime]
    created_by          : int
    is_deleted          : str
    is_deleted_directly : str
    is_deleted_with_master: str
    created_on          : datetime
    deleted_by          : Optional[int]
    deleted_on          : Optional[datetime]



class ProductVideoSchema(BaseModel):

    product_master_id: int
    video_title: Optional[str] = None
    video_description: Optional[str] = None


class ProductVideoSchemaResponse(BaseModel):

    id: int
    product_master_id: int
    video_title: str
    video_description: Optional[str] = None
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    created_by: int
    is_deleted: str
    created_on: datetime
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]



class InstallmentDetailsBase(BaseModel):
    installment_master_id: int
    installment_name: str
    payment_rate: float 
    due_date: date
    



    
    
class CustomerInstallmentMasterBase(BaseModel):
    customer_id: int
    installment_master_id: int
    total_amount_to_be_paid: float


class CustomerInstallmentDetailsBase(BaseModel):
    customer_installment_master_id: int
    installment_details_id: int
    due_amount: float
    due_date: Optional[date]
    is_paid: BooleanFlag
    paid_date: Optional[date]
    paid_amount: Optional[float] = None
    payment_mode_id: Optional[int]
    transaction_id: Optional[int]
    
    
class CustomerInstallmentDetailsForGet(BaseModel):
    id:int
    customer_installment_master_id: int
    installment_details_id: int
    due_amount: float
    due_date: Optional[date]
    is_paid: BooleanFlag
    paid_date: Optional[date]
    paid_amount: Optional[float] = None
    payment_mode_id: Optional[int]
    transaction_id: Optional[int]
    

    
class MobileVerificationStatus(BaseModel):
    mobile: str
    message: Optional[str] = None

class EmailVerificationStatus(BaseModel):
    email_id: str
    message: Optional[str] = None
    
class AdminUserActiveInactiveSchema(BaseModel):
     id:int
     is_active: BooleanFlag = 'yes'
     
     
# class InstallmentCreate(BaseModel):
#     number_of_installments: int
#     is_active: BooleanFlag 
#     active_from_date: Optional[date] = None
#     installment_name: str
#     payment_rate: float
#     due_date: date
   

#     class Config:
#         orm_mode = True

class InstallmentDetail(BaseModel):
    installment_name: str
    payment_rate: float
    due_date: date

class InstallmentCreate(BaseModel):
    number_of_installments: int
    is_active: str
    active_from_date: Optional[date] = None
    installment_details: List[InstallmentDetail]

    class Config:
        orm_mode = True
        
class InstallmentDetails(BaseModel):
    installment_master_id: int
    installment_name: str
    payment_rate: float
    due_date: date

    class Config:
        orm_mode = True
        
class InstallmentMasterCreate(BaseModel):
    number_of_installments: int
    is_active: bool
    active_from_date: date
    created_by: int
    
class InstallmentMasterCreateForGet(BaseModel):
    number_of_installments: int
    is_active: bool
    active_from_date: date
    created_by: int

class InstallmentDetailsCreate(BaseModel):
    installment_master_id: int
    installment_name: str
    payment_rate: float
    due_date: date
    created_by: int
    
class InstallmentEdit(BaseModel):
    is_active: Optional[BooleanFlag] = None
    active_from_date: Optional[date] = None
    installment_name: Optional[str] = None
    payment_rate: Optional[float] = None
    due_date: Optional[date] = None

    class Config:
        orm_mode = True
        
class InstallmentDetailsForGet(BaseModel):
    id:int
    installment_master_id: int
    installment_name: str
    payment_rate: float 
    due_date: date
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    created_by: int
    created_on: datetime
    is_deleted: str
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]
    
#///
class PancardSchemaResponse(BaseModel):
    id :int
    pan_card_type_code : str
    pan_card_type : str
    
class QualificationSchemaResponse(BaseModel):
    id:int
    qualification : str
    
class QualificationSchemaForUpdate(BaseModel):

    qualification : str



class ConstitutionTypeSchemaResponse(BaseModel):
    id:int
    constitution_type   : str
    
class ConstitutionTypeForUpdate(BaseModel):

    constitution_type   : str


class ProfessionSchemaResponse(BaseModel):
    id:int
    profession_name : str 
    profession_code : str
    
class ProfessionSchemaForUpdate(BaseModel):

    profession_name : str 
    profession_code : str


class HomeBannerSchema(BaseModel):

    description : str

class HomeMiracleAutomationSchema(BaseModel):

    description : str

class HomeTrendingNewsSchema(BaseModel):
     
     description : str

class PrimeCustomerSchema(BaseModel):

    customer_name : str
    description  : str
    website      : str

# class JobVacancieSchema(BaseModel):

#     title 				 : str
#     description 		 : str	
#     skills 				: str
#     qualifications 		: str
#     experience 			: str
#     certifications       : str		
#     announcement_date 	 : datetime
#     closing_date        : datetime

class JobVacancieSchema(BaseModel):

    title 				 : str
    description 		 : str	
    skills 				: str
    qualifications 		: str
    experience 			: str
    certifications       : str
    announcement_date : Optional[date] = None		
  
    closing_date        : Optional[date] = None	
    

    
  

# class AdminLogSchema(BaseModel):
#     id: int
#     user_id: int
#     logged_in_on: datetime
#     logged_out_on: Optional[datetime]
#     logged_in_ip: Optional[str]
#     referrer: Optional[str]
#     browser_type: Optional[str]
#     browser_family: Optional[str]
#     browser_version: Optional[str]
#     operating_system: Optional[str]
#     os_family: Optional[str]
#     os_version: Optional[str]

#     class Config:
#         orm_mode = True
#         from_orm = True
#         from_attributes = True
        
class AdminLogSchema(BaseModel):
    id: int
    user_id: int
    user_name: str  # Combined field of first_name and last_name
    logged_in_on: datetime
    logged_out_on: Optional[datetime]
    logged_in_ip: Optional[str]
    referrer: Optional[str]
    city: Optional[str]
    region: Optional[str]
    country: Optional[str]
    browser_type: Optional[str]
    browser_family: Optional[str]
    browser_version: Optional[str]
    operating_system: Optional[str]
    os_family: Optional[str]
    os_version: Optional[str]

    class Config:
        orm_mode = True
        
# class CustomerLogSchema(BaseModel):
#     id: int
#     user_id: int
#     logged_in_on: datetime
#     logged_out_on: Optional[datetime]
#     logged_in_ip: Optional[str]
#     referrer: Optional[str]
#     browser_type: Optional[str]
#     browser_family: Optional[str]
#     browser_version: Optional[str]
#     operating_system: Optional[str]
#     os_family: Optional[str]
#     os_version: Optional[str]

#     class Config:
#         orm_mode = True
#         from_orm = True
#         from_attributes = True


class CustomerLogSchema(BaseModel):
    id: int
    user_id: int
    user_name: str  # Combined field of first_name and last_name
    logged_in_on: datetime
    logged_out_on: Optional[datetime]
    logged_in_ip: Optional[str]
    referrer: Optional[str]
    city: Optional[str]
    region: Optional[str]
    country: Optional[str]
    browser_type: Optional[str]
    browser_family: Optional[str]
    browser_version: Optional[str]
    operating_system: Optional[str]
    os_family: Optional[str]
    os_version: Optional[str]

    class Config:
        orm_mode = True

        
        
class InstallmentFilter(BaseModel):
    is_active: BooleanFlag
    is_deleted: BooleanFlag
    
    
#/////////////


class HomeBannerSchemaResponse(BaseModel):

    id          : int
    description : str


class HomeMiracleAutomationSchemaResponse(BaseModel):

    id          : int
    description : str

class HomeTrendingNewsSchemaResponse(BaseModel):
     
    id          : int
    description : str
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    created_by: int
    created_on: datetime
    is_deleted: str
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]

class PrimeCustomerSchemaResponse(BaseModel):

    id            : int
    customer_name : str
    description  : str
    website      : str
    modified_by: Optional[int]
    modified_on: Optional[datetime]
    created_by: int
    created_on: datetime
    is_deleted: str
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]

class JobVacancieSchemaResponse(BaseModel):

    id                  :int
    title 				 : str
    description 		 : str	
    skills 				: str
    qualifications 		: str
    experience 			: str
    certifications       : str		
    announcement_date 	 : datetime
    closing_date        : datetime
    modified_by         : Optional[int]
    modified_on: Optional[datetime]
    created_by: int
    created_on: datetime
    is_deleted: str
    deleted_by: Optional[int]
    deleted_on: Optional[datetime]



class JobApplicationSchema(BaseModel):
    applied_date        : Optional[date] = None	
    full_name           : str
    email_id            : str
    subject             : str
    mobile_number       : str
    experience          : str
    message             : str


class JobApplicationSchemaResponse(BaseModel):

    id                  : int
    applied_date        : datetime
    full_name           : str
    email_id            : str
    subject             : str
    mobile_number       : str
    experience          : str
    message             : str

class MiracleFeaturesSchema(BaseModel):
    fa_icon 	: str	
    title 		: str	
    description : str


    
class MiracleFeaturesSchemaResponse(BaseModel):
    id         : int    
    fa_icon 	: str	
    title 		: str	
    description : str
    created_by  : int       
    created_on  : datetime  
    modified_by : Optional[int]        
    modified_on : Optional[datetime]        
    is_deleted  : bool       
    deleted_by  : Optional[int]       
    deleted_on  : Optional[datetime] 


class CAPTCHARequest(BaseModel):
    answer: int
    
#--------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
class EmailCredentialsSchema(BaseModel):
    SMTPHost: str
    SMTPPort: int
    SMTPAuth: bool
    UserName: str
    Password: Optional[str] = None


class Email(BaseModel):
    messageTo: str
    messageToUserName: str = ""
    messageBody: str
    subject: str
    messageType: str = "NO_REPLY"
    
    
    
class GetCustomerPasswordResetSchema(BaseModel):
    id			    :int
    customer_id 	:int
    request_token 	: str
    request_timestamp :Optional[datetime]

class CustomerPasswordResetSchema(BaseModel):
    email_id : str

class PriceListProductMaster(BaseModel):
    
    product_master_id     : Optional[int]
    price                 : float=0
    igst_rate                : float=0.0
    cgst_rate               : Optional[float] = 0.0
    sgst_rate               : Optional[float] = 0.0
    cess_rate               : Optional[float] = 0.0
    discount_percentage     : Optional[float] = 0.0
    discount_amount         : Optional[float] =0.0
    effective_from_date     : Optional[date] 
    effective_to_date       : Optional[date] = None
    
    
class PriceListProductMasterResponse(BaseModel):
    id                    :int
    product_master_id     : int
    price                 : float
    igst_rate                : float
    cgst_rate               : float
    sgst_rate               : float
    cess_rate               : float
    discount_percentage     : float
    discount_amount         : float
    effective_from_date     : Optional[date]
    effective_to_date       : Optional[date]
    created_by              : Optional[int]
    created_on              : Optional[datetime]
    modified_by             : Optional[int]
    modified_on             : Optional[datetime]
    is_deleted              : str
    is_deleted_directly     : str
    is_deleted_with_master  : str
    deleted_by              : Optional[int]
    deleted_on              : Optional[datetime]


class PriceListProductMasterView(BaseModel):
   
    product_master_id        :  int
    price_list_product_master_id   : int   
    product_code             :  str
    category_id              :  int
    category_name            :  str
    product_name             :  str
    product_description_main :  str
    product_description_sub  :  str
    has_module               :  str
    price                    :  float 
    igst_rate                 :    float
    cgst_rate                :    float
    sgst_rate                :    float
    cess_rate                :    float
    discount_percentage      :    float
    discount_amount          :    float
    effective_from_date      :  Optional[date] 
    effective_to_date        :  Optional[date]
    created_by               :  Optional[int]
    created_on               :  Optional[datetime]
    modified_by              :  Optional[int]
    modified_on              :  Optional[datetime]
    is_deleted               :  str
    is_deleted_directly      :   str
    is_deleted_with_master   :   str
    deleted_by               : Optional[int]
    deleted_on               : Optional[datetime]


class PriceListProductModule(BaseModel):
    
    price_list_product_master_id   :int
    module_id                      : int
    module_price                   : float=0
    igst_rate                : float=0
    cgst_rate               : float=0
    sgst_rate               : float=0
    cess_rate               : float=0
    discount_percentage     : float=0
    discount_amount         : float=0
    effective_from_date     : Optional[date]
    effective_to_date       : Optional[date]
    

class PriceListProductModuleResponse(PriceListProductModule):
    created_by              : int
    created_on              : datetime
    modified_by             : Optional[int]
    modified_on             : Optional[datetime]
    is_deleted              : str
    is_deleted_directly     : str
    is_deleted_with_master  : str
    deleted_by              : Optional[int]
    deleted_on              : Optional[datetime]



class PriceListProductModuleView(BaseModel):
    price_list_product_module_id   : int
    price_list_product_master_id   : int
    product_master_id              : int
    module_name                    : str
    module_id                      : int
    product_code                   : str
    product_name                   : str
    module_description             : str
    module_price                   : float
    module_igst_rate                : float
    module_cgst_rate               : float
    module_sgst_rate               : float
    module_cess_rate               : float
    module_discount_percentage     : float
    module_discount_amount         : float
    module_effective_from_date     : Optional[date]
    module_effective_to_date       : Optional[date]
    master_price                   : float
    master_igst_rate                : float
    master_cgst_rate               : float
    master_sgst_rate               : float
    master_cess_rate               : float
    master_discount_percentage     : float
    master_discount_amount         : float
    master_effective_from_date     : Optional[date]
    master_effective_to_date       :  Optional[date]
    created_by              : int
    created_on              : Optional[datetime]
    modified_by             : Optional[int]
    modified_on             : Optional[datetime]
    is_deleted              : str
    is_deleted_directly     : str
    is_deleted_with_master  : str
    deleted_by              : Optional[int]
    deleted_on              : Optional[datetime]



class ProductRating(BaseModel):    
    
    product_master_id : int  
    rating            : float
    comment           : Optional[str]=None


class ProductMasterPriceSchema(BaseModel):

    # id                      : int
    product_master_id       : int
    price                   : float
    gst_rate                : float 
    cess_rate               : float  
    effective_from_date     : date
    effective_to_date       : Optional[str]= None


class ProductModulePriceSchema(BaseModel):

    # id                      : int
    product_master_price_id   : int
    module_id                 :int
    module_price            : float
    gst_rate                : float 
    cess_rate               : float  
    effective_from_date     : date
    effective_to_date       : Optional[str]= None

   
class  OfferCategoryResponse(BaseModel):

    id              : int
    offer_category  : str

class OfferMasterSchema(BaseModel):

    id                 : Optional[int] = None
    offer_category_id   : int
    offer_name          : str
    offer_percentage    : Optional[float]= None
    offer_amount        : Optional[float]= None
    effective_from_date : date
    effective_to_date   : Optional[date] =None
   

class OfferDetailsSchema(BaseModel):

    offer_master_id     : int
    product_master_id   : int

class SaveOfferDetailsRequest(BaseModel):

    master: list[OfferMasterSchema]
    details: Optional[list[OfferDetailsSchema]]=None 

class CartDetailsSchema(BaseModel):

    
    product_master_id : int
    customer_id       : int
    saved_for_later   : Optional[BooleanFlag] ='no'

class CouponSchema(BaseModel):

    coupon_name : str
    coupon_code : str
    coupon_percentage: Optional[float]= None
    coupon_amount : Optional[float]= None
    effective_from_date : date
    effective_to_date   : Optional[date]



class CustomerPracticingAsSchema(BaseModel):
    # customer_id     : int
    practicing_type_id : int
    other               : Optional[str] = None      

class CustomerAreaOfPracticingSchema(BaseModel):
    # customer_id     : int
    area_of_practicing_id : int
    other               : Optional[str] = None

class CustomerQualificationSchema(BaseModel):
    # customer_id     :int   
    profession_type_id : int
    membership_number	: int
    enrollment_date     :date
    # practicing_as: Optional[List[CustomerPracticingAsSchema]]
    # area_of_practicing :Optional[List[CustomerAreaOfPracticingSchema]] 

class CompleteCustomerQualificationSchema(BaseModel):
    # customer_id     :int
    qualifications: Optional[List[CustomerQualificationSchema]] =None
    practicing_as: Optional[List[CustomerPracticingAsSchema]] =None
    area_of_practicing:Optional[ List[CustomerAreaOfPracticingSchema]] = None