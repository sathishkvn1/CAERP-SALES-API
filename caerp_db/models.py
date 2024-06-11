
# from sqlalchemy import Date
from sqlalchemy import Date
from sqlalchemy import Column, Integer, String ,Float,Text, DECIMAL
from sqlalchemy.dialects.mysql import CHAR
from caerp_db.database import caerp_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from datetime import date, datetime 
from sqlalchemy import Column, DateTime, func
from sqlalchemy import Enum



class CountryDB(caerp_base):
    __tablename__ = "app_countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_name_english        = Column(String(500), nullable=False)
    country_name_arabic         = Column(String(500, collation='utf8mb3_general_ci'), nullable=True)
    iso2_code                   = Column(String(2), nullable=True)
    iso3_code                   = Column(String(3), nullable=True)
    isd_code                    = Column(String(10), nullable=True)
    states                      =relationship("StateDB",back_populates="country")

class StateDB(caerp_base):
    __tablename__ = "app_states"
    id                          = Column(Integer, primary_key=True, autoincrement=True)
    country_id                  = Column(Integer, ForeignKey('app_countries.id'), nullable=False)
    state_name                  = Column(String(50), nullable=False)
    country                     = relationship("CountryDB", back_populates="states")
    districts                   = relationship("DistrictDB",back_populates="states")
    # post_offices = relationship("PostOfficeView", back_populates="state_name")


class DistrictDB(caerp_base):
    __tablename__ = "app_districts"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    state_id        = Column(Integer, ForeignKey('app_states.id'), nullable=False)
    district_name   = Column(String(50), nullable=False)
    states          = relationship("StateDB", back_populates="districts")
    # post_offices = relationship("PostOfficeView", back_populates="district_name")


class CityDB(caerp_base):
    __tablename__ = "app_cities"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    country_id      = Column(Integer, ForeignKey('app_countries.id'), nullable=False)
    state_id        = Column(Integer, ForeignKey('app_states.id'), nullable=False)
    city_name       = Column(String(50), nullable=False)
    
class TalukDB(caerp_base):
    __tablename__ = "app_taluks"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    district_id     = Column(Integer, nullable=False)
    state_id        = Column(Integer, nullable=False)
    taluk_name      = Column(String(50), nullable=False)
    # post_offices = relationship("PostOfficeView", back_populates="taluk_name")

    
class CurrencyDB(caerp_base):
    __tablename__ = "app_currencies"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    short_name      = Column(String(3), nullable=False)
    long_name       = Column(String(100), nullable=False)
    currency_symbol = Column(String(10), nullable=True)


    
class NationalityDB(caerp_base):
    __tablename__ = "app_nationality"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    nationality = Column(String(100), nullable=False)
    
class PostOfficeTypeDB(caerp_base):
    __tablename__ = "app_post_office_type"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    office_type = Column(String(50), nullable=False)
    
    
class PostalDeliveryStatusDB(caerp_base):
    __tablename__ = "app_postal_delivery_status"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    delivery_status = Column(String(50), nullable=False)

    
class PostalCircleDB(caerp_base):
    __tablename__ = "app_postal_circle"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    circle_name = Column(String(50), nullable=False)
    regions     = relationship("PostalRegionDB", back_populates="circle")
    divisions   = relationship("PostalDivisionDB", back_populates="circle", cascade="all, delete-orphan")
   

    
    
class PostalRegionDB(caerp_base):
    __tablename__ = "app_postal_region"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    circle_id       = Column(Integer, ForeignKey('app_postal_circle.id'), nullable=False)
    region_name     = Column(String(50), nullable=False)
    circle          = relationship("PostalCircleDB", back_populates="regions")
    divisions       = relationship("PostalDivisionDB", back_populates="region", cascade="all, delete-orphan")
  



class PostalDivisionDB(caerp_base):
    __tablename__ = "app_postal_division"
    id               = Column(Integer, primary_key=True, autoincrement=True)
    circle_id        = Column(Integer, ForeignKey('app_postal_circle.id'), nullable=False)
    region_id        = Column(Integer, ForeignKey('app_postal_region.id'), nullable=False)
    division_name    = Column(String(50), nullable=False)


    circle = relationship("PostalCircleDB", back_populates="divisions")
    region = relationship("PostalRegionDB", back_populates="divisions")
   



class PostOfficeView(caerp_base):
    __tablename__ = "app_view_post_offices"
    id                  = Column(Integer, primary_key=True)
    post_office_name    = Column(String(length=255))
    pin_code            = Column(String(length=10))
    post_office_type_id = Column(Integer)
    office_type         = Column(String(length=255))
    postal_delivery_status_id = Column(Integer)
    delivery_status     = Column(String(length=255))
    postal_division_id  = Column(Integer)
    division_name       = Column(String(length=255))  # Specify length for VARCHAR column
    postal_region_id    = Column(Integer)
    region_name         = Column(String(length=255))
    postal_circle_id    = Column(Integer)
    circle_name         = Column(String(length=255))
    taluk_id            = Column(Integer)
    taluk_name          = Column(String(length=255))
    district_id         = Column(Integer)
    district_name       = Column(String(length=255))
    state_id            = Column(Integer)
    state_name          = Column(String(length=255))
    country_id          =Column(Integer)
    country_name_english = Column(String(length=255))
    contact_number       = Column(String(length=20)) 
    latitude             = Column(String(length=15)) 
    longitude            = Column(String(length=15)) 
    
    
class AboutUsDB(caerp_base):
    __tablename__ = "app_site_about_us"
    id                      = Column(Integer, primary_key=True, index=True)
    about_us                = Column(Text, nullable=False)
    sub_head_description    = Column(Text)
    our_mission             = Column(Text)
    our_vision              = Column(Text)
    our_target              = Column(Text)
    footer_description      = Column(Text)
    


class Gender(caerp_base):
    __tablename__ = "app_gender"
    
    id          = Column(Integer, primary_key=True, autoincrement=True)
    gender      = Column(String(20), nullable=False)

class UserRole(caerp_base):
    __tablename__ = "app_user_role"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    role        = Column(String(50), nullable=False)
    created_by  = Column(Integer, nullable=False, default=0)
    created_on  = Column(DateTime, nullable=False, default=func.now())
    modified_by = Column(Integer, default=None)
    modified_on = Column(DateTime, default=None)
    is_deleted  = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by  = Column(Integer, default=None)
    deleted_on  = Column(DateTime, default=None)

class Designation(caerp_base):
    __tablename__ = "app_designation"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    designation     = Column(String(50), nullable=False)
    created_by      = Column(Integer, nullable=False, default=0)
    created_on      = Column(DateTime, nullable=False, default=func.now())
    modified_by     = Column(Integer, default=None)
    modified_on     = Column(DateTime, default=None)
    is_deleted      = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by      = Column(Integer, default=None)
    deleted_on      = Column(DateTime, default=None)
    


class AdminUser(caerp_base):
    __tablename__ = "app_admin_users"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    first_name      = Column(String(50), nullable=False)
    last_name       = Column(String(50), default=None)
    gender_id       = Column(Integer, nullable=False)
    user_name       = Column(String(50), nullable=False, unique=True)
    password        = Column(String(200), nullable=False)
    role_id         = Column(Integer, nullable=False)
    designation_id  = Column(Integer,  nullable=False)
    address_line_1  = Column(String(100), default=None)
    address_line_2  = Column(String(100), default=None)
    address_line_3  = Column(String(100), default=None)
    address_line_4  = Column(String(100), default=None)
    pin_code        = Column(String(100), nullable=False)
    city_id         = Column(Integer,  nullable=False)
    taluk_id        = Column(Integer,  nullable=False)
    district_id     = Column(Integer,  nullable=False)
    state_id        = Column(Integer,  nullable=False)
    country_id      = Column(Integer,  nullable=False)
    mobile_number   = Column(String(20), default=None)
    whatsapp_number = Column(String(20), default=None)
    email_id        = Column(String(100), default=None)
    is_active       = Column(Enum('yes', 'no'), nullable=False, default='yes')
    created_by      = Column(Integer, nullable=False, default=0)
    created_on      = Column(DateTime, nullable=False, default=func.now())
    modified_by     = Column(Integer, default=None)
    modified_on     = Column(DateTime, default=None)
    is_deleted      = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by      = Column(Integer, default=None)
    deleted_on      = Column(DateTime, default=None)

    

class AdminLog(caerp_base):
    __tablename__ = "app_admin_log"

    id                  = Column(Integer, primary_key=True, index=True)
    user_id             = Column(Integer, default=None)
    logged_in_on        = Column(DateTime, nullable=False, default=datetime.utcnow)
    logged_out_on       = Column(DateTime, default=None)
    logged_in_ip        = Column(String(500), default=None)
    referrer            = Column(String(500), default=None)
    city                = Column(String(500, collation='utf8mb4_unicode_ci'), default=None)  
    region              = Column(String(500, collation='utf8mb4_unicode_ci'), default=None) 
    country             = Column(String(500, collation='utf8mb4_unicode_ci'), default=None) 
    browser_type        = Column(String(500), default=None)
    browser_family      = Column(String(500), default=None)
    browser_version     = Column(String(500), default=None)
    operating_system    = Column(String(500), default=None)
    os_family           = Column(String(500), default=None)
    os_version          = Column(String(500), default=None)
    
    
class CustomerLog(caerp_base):
    __tablename__ = "customer_log"

    id              = Column(Integer, primary_key=True, index=True)
    user_id         = Column(Integer, default=None)
    logged_in_on    = Column(DateTime, nullable=False, default=datetime.utcnow)
    logged_out_on   = Column(DateTime, default=None)
    logged_in_ip    = Column(String(500), default=None)
    referrer        = Column(String(500), default=None)
    city            = Column(String(500, collation='utf8mb4_unicode_ci'), default=None)  
    region          = Column(String(500, collation='utf8mb4_unicode_ci'), default=None) 
    country         = Column(String(500, collation='utf8mb4_unicode_ci'), default=None) 
    browser_type    = Column(String(500), default=None)
    browser_family  = Column(String(500), default=None)
    browser_version = Column(String(500), default=None)
    operating_system     = Column(String(500), default=None)
    os_family       = Column(String(500), default=None)
    os_version      = Column(String(500), default=None)

    
class AdminMainMenuPermission(caerp_base):
    __tablename__ = 'app_view_admin_main_menu_permission'

    main_menu_id                         = Column(Integer, primary_key=True)
    main_menu                            = Column(String(length=255))
    main_menu_has_sub_menu               = Column(String(length=10))
    main_menu_display_order              = Column(Integer)
    main_menu_page_link                  = Column(String(length=255))
    main_menu_permission_id             = Column(Integer)
    main_menu_permission_role_id        = Column(Integer)
    main_menu_permission_is_granted     = Column(String(length=10))
        


class AdminSubMenuPermission(caerp_base):
    __tablename__ = 'app_view_admin_sub_menu_permission'

    main_menu_id                    = Column(Integer, primary_key=True)
    sub_menu_id                     = Column(Integer)
    sub_menu                        = Column(String(length=255))  # Specify length for VARCHAR column
    sub_menu_has_sub_menu           = Column(String(length=10))  # Adjust length as needed
    sub_menu_display_order          = Column(Integer)
    sub_menu_page_link              = Column(String(length=255))  # Adjust length as needed
    sub_menu_permission_id          = Column(Integer)
    sub_menu_permission_role_id     = Column(Integer)
    sub_menu_permission_is_granted  = Column(String(length=10)) 
    
class AdminMainMenu(caerp_base):
    __tablename__ = 'app_admin_main_menu'

    main_menu_id                = Column(Integer, primary_key=True, autoincrement=True)
    main_menu                   = Column(String(200))
    main_menu_has_sub_menu      = Column(Enum('yes', 'no'), nullable=False, default='no')
    main_menu_display_order     = Column(Integer, nullable=False)
    main_menu_page_link         = Column(String(500), default=None)
    created_by                  = Column(Integer, nullable=False)
    created_on                  = Column(DateTime, nullable=False, default=func.now())
    modified_by                 = Column(Integer)
    modified_on                 = Column(DateTime)
    is_deleted                  = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by                  = Column(Integer, default=None)
    deleted_on                  = Column(DateTime, default=None)
    
class AdminSubMenu(caerp_base):
    __tablename__ = "app_admin_sub_menu"

    sub_menu_id                 = Column(Integer, primary_key=True, autoincrement=True)
    main_menu_id                = Column(Integer, nullable=False)
    sub_menu                    = Column(String(200))
    sub_menu_has_sub_menu       = Column(Enum('yes', 'no'), nullable=False, default='no')
    sub_menu_display_order      = Column(Integer, nullable=False)
    sub_menu_page_link          = Column(String(500), default=None)
    created_by                  = Column(Integer, nullable=False)
    created_on                  = Column(DateTime, nullable=False, default=func.now())
    modified_by                 = Column(Integer)
    modified_on                 = Column(DateTime)
    is_deleted                  = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by                  = Column(Integer)
    deleted_on                  = Column(DateTime)
    
    
class Test(caerp_base):
    __tablename__ = 'test'

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, index=True)
    
    
class OurTeam(caerp_base):
    __tablename__ = "app_site_our_team"
   
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    full_name           = Column(String(100), nullable=False)
    designation_id      = Column(Integer)
    qualification_id    = Column(Integer)
    description         = Column(Text)
    experience          = Column(String(1000))
    created_by          = Column(Integer, nullable=False)
    created_on          = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_by         = Column(Integer)
    modified_on         = Column(DateTime)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer)
    deleted_on          = Column(DateTime)
    
    
class OurDirectorDB(caerp_base):
    __tablename__ = 'app_site_our_directors'

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    full_name           = Column(String(100), nullable=False)
    designation_id      = Column(Integer)
    qualification_id    = Column(Integer)
    description         = Column(Text)
    experience          = Column(String(1000))
    created_by          = Column(Integer, nullable=False)
    created_on          = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_by         = Column(Integer)
    modified_on         = Column(DateTime)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer)
    deleted_on          = Column(DateTime)
    
    
class FaqCategoryDB(caerp_base):
    __tablename__ = 'app_site_faq_category'
    
    id               = Column(Integer, primary_key=True, autoincrement=True)
    faq_category     = Column(String(500), nullable=False)
    created_by       = Column(Integer, nullable=False)
    created_on       = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_by      = Column(Integer)
    modified_on      = Column(DateTime)
    is_deleted       = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by       = Column(Integer)
    deleted_on       = Column(DateTime)
    
    

    
class FaqDB(caerp_base):
    __tablename__ = "app_site_faq"
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    faq                 = Column(String(1000), nullable=False)
    faq_answer          = Column(Text)
    faq_category_id     = Column(Integer,  nullable=False)
    created_by          = Column(Integer, nullable=False)
    created_on          = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_by         = Column(Integer)
    modified_on         = Column(DateTime)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer)
    deleted_on          = Column(DateTime)

class TrendingNews(caerp_base):
    __tablename__ = 'app_site_trending_news'
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    title               = Column(String(1000), nullable=False)
    details             = Column(Text)
    created_by          = Column(Integer, nullable=False)
    created_on          = Column(DateTime, nullable=False, default=func.now())
    modified_by         = Column(Integer)
    modified_on         = Column(DateTime)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer)
    deleted_on          = Column(DateTime)
    

    
    
class SocialMediaURL(caerp_base):
    __tablename__ = 'app_site_social_media_url'
    
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    social_media        = Column(String(100), nullable=False)
    social_media_url    = Column(String(200))
    faicon              = Column(String(50))
    created_by          = Column(Integer, nullable=False)
    created_on          = Column(DateTime, nullable=False, default=func.now())
    modified_by         = Column(Integer)
    modified_on         = Column(DateTime)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer)
    deleted_on          = Column(DateTime)

class ContactDetailsDB(caerp_base):
    __tablename__ = 'app_site_contact_details'
    id                        = Column(Integer, primary_key=True, autoincrement=True)
    contact_us                = Column(String(100), nullable=False)
    map_iframe                = Column(Text)
    email_id                 = Column(String(50))
    address                  = Column(Text)
    office_phone             = Column(Text)
    customer_care_no         = Column(String(500))
    telephone                = Column(String(500))
    mobile_no                = Column(String(500))
    whatsapp_no              = Column(String(50))
    contact_side_description = Column(String(500))
    contact_main_description = Column(Text)
    client_site_address_text = Column(String(255))
    site_url                 = Column(String(255))
    modified_by              = Column(Integer)
    modified_on              = Column(DateTime)


class PrivacyPolicyDB(caerp_base):
    __tablename__ = 'app_site_privacy_policy'
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    privacy_policy      = Column(Text, nullable=False)
    modified_by         = Column(Integer, default=None)
    modified_on         = Column(DateTime, default=None)
    
class TermsAndConditionDB(caerp_base):
    __tablename__ = 'app_site_terms_and_condition'
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    terms_and_condition = Column(Text, nullable=False)
    modified_by         = Column(Integer, default=None)
    modified_on         = Column(DateTime, default=None)
    
    
class ImageGalleryDB(caerp_base):
    __tablename__ = 'app_site_image_gallery'
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    title               = Column(String(500), nullable=False)
    description         = Column(Text)
    created_by          = Column(Integer, nullable=False)
    created_on          = Column(DateTime, nullable=False, default=func.now())
    modified_by         = Column(Integer)
    modified_on         = Column(DateTime)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer)
    deleted_on          = Column(DateTime)
    
    
class GeneralContactDetailsDB(caerp_base):
    __tablename__ = 'app_site_general_contact_details'

    id                      = Column(Integer, primary_key=True, autoincrement=True)
    general_contact_details = Column(Text, nullable=False)
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    
    
class CompanyMaster(caerp_base):
    __tablename__ = 'acc_company_master'

    company_id                  = Column(Integer, primary_key=True, autoincrement=True)
    company_name                = Column(String(100), nullable=False)
    state_id                    = Column(Integer, nullable=False)
    country_id                  = Column(Integer, nullable=False)
    base_currency_id            = Column(Integer, nullable=False)
    suffix_symbol_to_amount     = Column(Enum('yes', 'no'), default='no')
    show_amount_in_millions     = Column(Enum('yes', 'no'), default='no')
    book_begin_date             = Column(Date,nullable=False)
    created_by                  = Column(Integer, nullable=False)
    created_on                  = Column(DateTime, nullable=False)
    modified_by                 = Column(Integer)
    modified_on                 = Column(DateTime)
    is_deleted                  = Column(Enum('yes', 'no'), default='no')
    deleted_by                  = Column(Integer)
    deleted_on                  = Column(DateTime)


class Master(caerp_base):
    __tablename__ = 'Master'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    voucher_id      = Column(Integer,nullable=False)


class Detail1(caerp_base):
    __tablename__ = 'Detail1'

    id          = Column(Integer, primary_key=True, autoincrement=True)
    voucher_id  = Column(Integer,nullable=False)


class Detail2(caerp_base):
    __tablename__ = 'Detail2'

    id              = Column(Integer, primary_key=True, autoincrement=True)
    voucher_id      = Column(Integer,nullable=False)
    
class Voucher(caerp_base):
    __tablename__ = 'VoucherCounter'

    id          = Column(Integer, primary_key=True, autoincrement=True)
    voucher_id  = Column(Integer)
    
    

    
class ClientMainMenu(caerp_base):
    __tablename__ = 'app_client_main_menu'
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    menu                = Column(String(200))
    has_sub_menu        = Column(Enum('yes', 'no'), default='no')
    display_order       = Column(Integer, nullable=False)
    page_link           = Column(String(500), default=None)
    created_by          = Column(Integer, nullable=False)
    created_on          = Column(DateTime, nullable=False, server_default='CURRENT_TIMESTAMP')
    modified_by         = Column(Integer, default=None)
    modified_on         = Column(DateTime, default=None)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer, default=None)
    deleted_on          = Column(DateTime, default=None)
    
    
class SiteLegalAboutUs(caerp_base):
    __tablename__ = 'app_site_legal_about_us'

    id                              = Column(Integer, primary_key=True, autoincrement=True)
    nature_of_business              = Column(String(100), nullable=False)
    legal_status_of_the_firm        = Column(String(100), default=None)
    gst_in                          = Column(String(100), default=None)
    pan_number                      = Column(String(100), default=None)
    trade_mark                      = Column(String(100), default=None)
    startup_reg_number              = Column(String(100), default=None)
    total_number_of_employees       = Column(String(100), default=None)
    annual_turn_over                = Column(String(100), default=None)
    cin                             = Column(String(50), default=None)
    tan_number                      = Column(String(100), default=None)
    iso_number                      = Column(String(100), default=None)
    startup_mission_number          = Column(String(100), default=None)
    year_of_establishment           = Column(String(100), default=None)
    import_export_code              = Column(String(100), default=None)
    msme                            = Column(String(100), default=None)
    esic                            = Column(String(100), default=None)
    epf                             = Column(String(100), default=None)
    updated_by                      = Column(Integer, default=None)
    updated_on                      = Column(DateTime, default=None)
    
class PublicMainMenu(caerp_base):
    __tablename__ = 'app_main_menu'

    id                          = Column(Integer, primary_key=True, autoincrement=True)
    menu                        = Column(String(200))
    has_sub_menu                = Column(Enum('yes', 'no'), nullable=False, default='no')
    display_order               = Column(Integer, nullable=False)
    page_link                   = Column(String(500), default=None)
    created_by                  = Column(Integer, nullable=False)
    created_on                  = Column(DateTime, nullable=False, default=func.now())
    modified_by                 = Column(Integer)
    modified_on                 = Column(DateTime)
    is_deleted                  = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by                  = Column(Integer, default=None)
    deleted_on                  = Column(DateTime, default=None)

    
class PublicSubMenu(caerp_base):
    __tablename__ = "app_sub_menu"

    id                      = Column(Integer, primary_key=True, autoincrement=True)
    main_menu_id            = Column(Integer, nullable=False)
    sub_menu                = Column(String(200))
    has_sub_menu            = Column(Enum('yes', 'no'), nullable=False, default='no')
    display_order           = Column(Integer, nullable=False)
    page_link               = Column(String(500), default=None)
    created_by              = Column(Integer, nullable=False)
    created_on              = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer)
    modified_on             = Column(DateTime)
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer)
    deleted_on              = Column(DateTime)
    
 
class PublicSubSubMenu(caerp_base):
    __tablename__ = "app_sub_sub_menu"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    sub_menu_id         = Column(Integer, nullable=False)
    sub_sub_menu        = Column(String(200))
    display_order       = Column(Integer, nullable=False)
    page_link           = Column(String(500), default=None)
    created_by          = Column(Integer, nullable=False)
    created_on          = Column(DateTime, nullable=False, default=func.now())
    modified_by         = Column(Integer)
    modified_on         = Column(DateTime)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer)
    deleted_on          = Column(DateTime)
    

class CustomerRegister(caerp_base):
    __tablename__ = "customer_register"

    id                          = Column(Integer, primary_key=True, autoincrement=True)
    first_name                  = Column(String(100), nullable=False)
    last_name                   = Column(String(100), nullable=False)
    gender_id                   = Column(Integer, nullable=False)
    mobile_number               = Column(String(100), nullable=False)
    is_mobile_number_verified   = Column(Enum('yes', 'no'), nullable=False, default='no')
    email_id                    = Column(String(100), default=None)
    is_email_id_verified        = Column(Enum('yes', 'no'), nullable=False, default='no')
    pin_code                    = Column(Integer, nullable=False)
    post_office_id              = Column(Integer, nullable=False)
    taluk_id                    = Column(Integer, nullable=False)
    district_id                 = Column(Integer, nullable=False)
    state_id                    = Column(Integer, nullable=False)
    country_id                  = Column(Integer, nullable=False)
    password                    = Column(String(100), nullable=False)
    customer_type_id            = Column(Integer, nullable=False,default=1)
    created_on                  = Column(DateTime, nullable=False, default=func.now())
    expiring_on                 = Column(DateTime, nullable=False, default=func.now()) 
    is_deleted                  = Column(Enum('yes', 'no'), nullable=False, default='no')
    is_active                   = Column(Enum('yes', 'no'), nullable=False, default='yes')       



    
    
class CustomerCompanyProfile(caerp_base):
    __tablename__ = "customer_company_profile"
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    customer_id         = Column(Integer, nullable=False)
    company_name        = Column(String(250), nullable=False)
    pin_code            = Column(String(20), nullable=False)
    city_id             = Column(Integer, nullable=False)
    post_office_id      = Column(Integer, nullable=False)
    taluk_id            = Column(Integer, nullable=False)
    district_id         = Column(Integer, nullable=False)
    state_id            = Column(Integer, nullable=False)
    country_id          = Column(Integer, nullable=False)
    address_line_1      = Column(String(250), nullable=False)
    address_line_2      = Column(String(250), default=None)
    address_line_3      = Column(String(250), default=None)
    address_line_4      = Column(String(250), default=None)
    pan_number          = Column(String(100), default=None)
    pan_card_type_id    = Column(Integer, default=None)
    gst_number          = Column(String(100), default=None)
    company_description = Column(Text, default=None)
    about_company       = Column(Text, default=None)
    company_mobile      = Column(String(100), nullable=False)
    company_email_id    = Column(String(100), nullable=False)
    company_web_site    = Column(String, default=None)
    

    
class CustomerNews(caerp_base):
    __tablename__ = 'customer_news'

    id          = Column(Integer, primary_key=True, autoincrement=True)
    title       = Column(String(500), nullable=False)
    details     = Column(Text, nullable=False)
    is_active   = Column(Enum('yes', 'no'), nullable=False, default='yes')
    created_by  = Column(Integer, nullable=False)
    created_on  = Column(DateTime, nullable=False, default=func.now())
    modified_by = Column(Integer)
    modified_on = Column(DateTime)
    is_deleted  = Column(Enum('yes', 'no'), nullable=False, default='no')  
    deleted_by  = Column(Integer, default=None)
    deleted_on  = Column(DateTime, default=None)


    
class CustomerSalesQuery(caerp_base):
    __tablename__ = "customer_sales_queries"

    id                      = Column(Integer, primary_key=True, index=True)
    query_date              = Column(Date, nullable=False)
    contact_person_name     = Column(String(100), nullable=False)
    company_name            = Column(String(250), default=None)
    email_id                = Column(String(100), default=None)
    mobile_number           = Column(String(100), nullable=False)
    pin_code                = Column(Integer, default=None)
    city_id                 = Column(Integer, nullable=False)
    post_office_id          = Column(Integer, nullable=False)
    taluk_id                = Column(Integer, nullable=False)
    district_id             = Column(Integer, nullable=False)
    state_id                = Column(Integer, nullable=False)
    country_id              = Column(Integer, nullable=False)
    is_read                 = Column(Enum('yes', 'no'), default='no')
    read_by                 = Column(Integer, default=None)
    read_on                 = Column(DateTime, default=None)
    is_replied              = Column(Enum('yes', 'no'), default=None)
    replied_by              = Column(Integer, default=None)
    
    
class InstallmentMaster(caerp_base):
    __tablename__ = "installment_master"
    
    id                      = Column(Integer, primary_key=True, index=True)
    number_of_installments  = Column(Integer, nullable=False)
    is_active               = Column(Enum('yes', 'no'), default='no')
    active_from_date        = Column(Date, default=None)
    created_by              = Column(Integer, nullable=False)
    created_on              = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer, nullable=False)
    modified_on             = Column(DateTime, nullable=False, default=func.now())
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer, nullable=True)  # Allow NULL values for deleted_by
    deleted_on              = Column(DateTime, nullable=True)  # Allow NULL values for deleted_on


    
class ProductMaster(caerp_base):
    __tablename__= "product_master"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    product_code        = Column(String(100), default=None)
    product_name        = Column(String(100), default=None)
    category_id         = Column(Integer, default=None)
    product_description_main = Column(Text, default=None)
    product_description_sub = Column(Text, default=None)
    has_module          = Column(Enum('yes', 'no'), nullable=False, default='no')
    created_by          = Column(Integer, default=None)
    created_on          = Column(DateTime, nullable=False, default=func.now())
    modified_by         = Column(Integer, default=None)
    modified_on         = Column(DateTime, default=None)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer, default=None)
    deleted_on          = Column(DateTime, default=None)

class ProductCategory(caerp_base):
    __tablename__ = "product_category"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    category_name       = Column(String(100), default=None)
    created_by          = Column(Integer, default=None)
    created_on          = Column(DateTime, nullable=False, default=func.now())
    modified_by         = Column(Integer, default=None)
    modified_on         = Column(DateTime, default=None)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer, default=None)
    deleted_on          = Column(DateTime, default=None)

class ProductModule(caerp_base):
    __tablename__ = "product_module"
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    product_master_id   = Column(Integer, nullable=False)
    module_name         = Column(String(100), nullable=False)
    module_description  = Column(String(5000), nullable=False)
    display_order       = Column(Integer, nullable=False,default=1)
    created_by          = Column(Integer, default=None)
    created_on          = Column(DateTime, nullable=False, default=func.now())
    modified_by         = Column(Integer, default=None)
    modified_on         = Column(DateTime, default=None)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    is_deleted_directly = Column(Enum('yes', 'no'), nullable=False, default='no')
    is_deleted_with_master = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer, default=None)
    deleted_on          = Column(DateTime, default=None)


class ProductVideo(caerp_base):
    __tablename__   =   "product_videos"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    product_master_id	= Column(Integer, nullable=False)
    video_title	         = Column(String(100), nullable=False)
    video_description  = Column(String(5000), nullable=False)
    created_by          = Column(Integer, default=None)
    created_on          = Column(DateTime, nullable=False, default=func.now())
    modified_by         = Column(Integer, default=None)
    modified_on         = Column(DateTime, default=None)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer, default=None)
    deleted_on          = Column(DateTime, default=None)
    
    
class InstallmentDetails(caerp_base):
    __tablename__ = "installment_details"

    id                      = Column(Integer, primary_key=True, index=True, autoincrement=True)
    installment_master_id   = Column(Integer,  nullable=False)
    installment_name        = Column(String(200), default=None)
    payment_rate            = Column(DECIMAL(10, 2), nullable=False)
    due_date                = Column(Date, nullable=False)
    created_by              = Column(Integer, nullable=False)
    created_on              = Column(DateTime, nullable=False, default=datetime.utcnow)
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer, default=None)
    deleted_on              = Column(DateTime, default=None)


class CustomerInstallmentMaster(caerp_base):
    __tablename__ = "customer_installment_master"

    id                      = Column(Integer, primary_key=True, index=True)
    customer_id             = Column(Integer,  nullable=False)
    installment_master_id   = Column(Integer,  nullable=False)
    total_amount_to_be_paid = Column(Float, nullable=False)


class CustomerInstallmentDetails(caerp_base):
    __tablename__ = "customer_installment_details"

    id                              = Column(Integer, primary_key=True, index=True)
    customer_installment_master_id  = Column(Integer,  nullable=False)
    installment_details_id          = Column(Integer,  nullable=False)
    due_amount                      = Column(Float, nullable=False)
    due_date                        = Column(Date, default=None)
    is_paid                         = Column(Enum('yes', 'no'), nullable=False, default='no')
    paid_date                       = Column(Date, default=None)
    paid_amount                     = Column(Float, default=None)
    payment_mode_id                 = Column(Integer, default=None)
    transaction_id                  = Column(Integer,  default=None)
    
class PanCard(caerp_base):
    __tablename__   =   "app_pan_card_types"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    pan_card_type_code	= Column(String(1), nullable=False)
    pan_card_type	    = Column(String(100), nullable=False)

class Qualification(caerp_base):
    __tablename__   =   "app_qualification"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    qualification	    = Column(String(50), nullable=False)

class ConstitutionTypes(caerp_base):
    __tablename__   =   "app_constitution_types"

    id                   = Column(Integer, primary_key=True, autoincrement=True)
    constitution_type	 = Column(String(50), nullable=False)

class Profession(caerp_base):
    __tablename__  =  "app_profession"
    
    id                   = Column(Integer, primary_key=True, autoincrement=True)
    profession_name 	 = Column(String(100), nullable=False)
    profession_code      = Column(String(100), nullable=False)



    
class HomeBanner(caerp_base):
    __tablename__  =  "app_site_home_banner"
    
    id                   = Column(Integer, primary_key=True, autoincrement=True)
    description          = Column(Text, nullable=False)
 


class HomeMiracleAutomation(caerp_base):
    __tablename__  =  "app_site_home_miracle_of_automation"
    
    id                   = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text, nullable=False)
   


class HomeTrendingNews(caerp_base):
    __tablename__  =  "app_site_home_trending_news"
    
    id                   = Column(Integer, primary_key=True, autoincrement=True)
    description         = Column(Text, nullable=False)
    created_by          = Column(Integer, default=None)
    created_on          = Column(DateTime, nullable=False, default=func.now())
    modified_by         = Column(Integer, default=None)
    modified_on         = Column(DateTime, default=None)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer, default=None)
    deleted_on          = Column(DateTime, default=None)




    
class PrimeCustomer(caerp_base):
    __tablename__  =  "app_site_prime_customers"
    
    id                   = Column(Integer, primary_key=True, autoincrement=True)
    customer_name       = Column(String(100), nullable=False)
    description         = Column(Text, nullable=False)
    website             = Column(String(255), nullable=False)
    created_by          = Column(Integer, default=None)
    created_on          = Column(DateTime, nullable=False, default=func.now())
    modified_by         = Column(Integer, default=None)
    modified_on         = Column(DateTime, default=None)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer, default=None)
    deleted_on          = Column(DateTime, default=None)




class JobVacancies(caerp_base):
    __tablename__  =  "app_site_job_vacancies"
    
    id                   = Column(Integer, primary_key=True, autoincrement=True)
    title 				 = Column(String(255), nullable=False)	
    description 		 = Column(String(2000), nullable=False)		
    skills 				 = Column(String(2000), nullable=False)
    qualifications 		 = Column(String(2000), nullable=False)	
    experience 			 = Column(String(2000), nullable=False)	
    certifications       = Column(String(2000), nullable=False)			
    announcement_date 	 = Column(Date, default=None)
    closing_date	     = Column(Date, default=None)
    created_by          = Column(Integer, default=None)
    created_on          = Column(DateTime, nullable=False, default=func.now())
    modified_by         = Column(Integer, default=None)
    modified_on         = Column(DateTime, default=None)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer, default=None)
    deleted_on          = Column(DateTime, default=None)
    
    
class JobApplication(caerp_base):
    __tablename__ = "app_site_job_applications"

    id              = Column(Integer, primary_key=True, index=True)
    applied_date    = Column(Date, nullable=False, default=datetime.utcnow)		
    full_name 		= Column(String(255), nullable=False)
    email_id 		= Column(String(255), nullable=False)	
    subject  		= Column(String(255), default=None)
    mobile_number	= Column(String(20), default=None)
    experience 		= Column(String(2000), default=None)
    message         = Column(String(2000), default=None)

class MiracleFeatures(caerp_base):
    __tablename__ = "app_site_miracle_features"

    id                  = Column(Integer, primary_key=True, index=True)
    fa_icon 		    = Column(String(255), nullable=False)
    title 			    = Column(String(255), nullable=False)
    description         = Column(Text, nullable=False)	
    created_by          = Column(Integer, default=None)
    created_on          = Column(DateTime, nullable=False, default=func.now())
    modified_by         = Column(Integer, default=None)
    modified_on         = Column(DateTime, default=None)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer, default=None)
    deleted_on          = Column(DateTime, default=None)
    
#--------------------------------------------------------------------------------------------------------------#--------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------


class EmailCredentials(caerp_base):
    __tablename__ = "app_email_api_settings"

    id                      = Column(Integer, primary_key=True, index=True)
    SMTP_auth               = Column(Enum('true', 'false'), nullable=False, default='true')
    SMTP_sequre             = Column(Enum('ssl', 'tls'), nullable=False, default='tls')
    SMTP_host               = Column(String(100), nullable=False)
    SMTP_port               = Column(String(5), nullable=False)
    username                = Column(String(100), nullable=False)
    password                = Column(Text, nullable=False)
    email_error_report      = Column(Integer, nullable=False)
    IMAP_host               = Column(String(100), default=None)
    IMAP_port               = Column(String(5), default=None)
    IMAP_username           = Column(String(100), default=None)
    IMAP_mail_box           = Column(String(10), default=None)
    IMAP_path               = Column(String(30), default=None)
    IMAP_server_encoding    = Column(String(15), default=None)
    IMAP_attachement_dir    = Column(String(20), default=None)
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)



class OtpGeneration(caerp_base):
    __tablename__ = "app_site_otp"

    id              = Column(Integer, primary_key=True, index=True)    
    otp             = Column(String(50), nullable=False)
    otp_expire_on   = Column(DateTime, nullable=False)
    created_by          = Column(Integer, default=None)
    created_on          = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by          = Column(Integer, default=None)
    deleted_on          = Column(DateTime, default=None)

class MobileCredentials(caerp_base):
    __tablename__ = "app_sms_api_settings"

    id                      = Column(Integer, primary_key=True, index=True)  
    api_url                  = Column(String(500), nullable=False)
    port                    = Column(String(6), nullable=False)
    sender                  = Column(String(6), nullable=False)
    username                = Column(String(250), nullable=False)
    password                = Column(Text, nullable=False)
    entity_id               = Column(String(250), nullable=False)
    delivery_report_status  = Column(Integer, default=None)
    is_active               = Column(Enum('yes', 'no'), nullable=False, default='yes')
    modified_on             = Column(DateTime, default=None)
    modified_by             = Column(Integer, default=None)

class SmsTemplates(caerp_base):
     __tablename__ = "app_site_sms_templates"

     id                      = Column(Integer, primary_key=True, index=True) 
     sms_category            = Column(Enum('TRANSACTIONAL', 'PROMOTIONAL'), nullable=False, default=None)
     sms_type                = Column(String(100), nullable=False)
     message_template        = Column(String(500), nullable=False)
     template_id             = Column(String(100), nullable=False)
     created_by              = Column(Integer, default=None)
     created_on              = Column(DateTime, nullable=False, default=func.now())
     modified_on             = Column(DateTime, default=None)
     modified_by             = Column(Integer, default=None)
     is_active               = Column(Enum('yes', 'no'), nullable=False, default='yes')
     
     
class CustomerPasswordReset(caerp_base):
    __tablename__ = 'customer_password_reset_requests'

    id                      = Column(Integer, primary_key=True, index=True)
    customer_id             = Column(Integer, nullable=False)
    request_token           = Column(String(500), nullable=False)
    request_timestamp       = Column(DateTime, nullable=False, default=func.now())



class PriceListProductMaster(caerp_base):
    __tablename__ = 'price_list_product_master'

    id                      = Column(Integer, primary_key=True, index=True)
    product_master_id       = Column(Integer, nullable=False)
    price                   = Column(Float, nullable=False, default=0)
    igst_rate                = Column(Float, nullable=False,default=0.0)
    cgst_rate               = Column(Float, nullable=False, default=0.0)
    sgst_rate               = Column(Float, nullable=False)
    cess_rate               = Column(Float, nullable=False)
    discount_percentage     = Column(Float, nullable=False)
    discount_amount         = Column(Float, nullable=False)
    effective_from_date     = Column(Date, nullable=False)
    effective_to_date       = Column(Date, default=None)
    created_by              = Column(Integer, default=None)
    created_on              = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    is_deleted_directly     = Column(Enum('yes', 'no'), nullable=False, default='no')
    is_deleted_with_master  = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer, default=None)
    deleted_on              = Column(DateTime, default=None)

class PriceListProductMasterView(caerp_base):
    __tablename__ = 'view_price_list_product_master'

    product_master_id       = Column(Integer,  nullable=False)
    price_list_product_master_id       = Column(Integer, primary_key=True, index=True)
    product_code            = Column(String, nullable=False)
    category_id             = Column(Integer, nullable=False)
    category_name           = Column(String, nullable=False)
    product_name            = Column(String, nullable=False)
    product_description_main= Column(String, nullable=False)
    product_description_sub = Column(String, nullable=False)
    has_module              = Column(Enum('yes', 'no'), nullable=False, default='no')
    price                   = Column(Float, nullable=False)
    igst_rate                = Column(Float, nullable=False)
    cgst_rate               = Column(Float, nullable=False)
    sgst_rate               = Column(Float, nullable=False)
    cess_rate               = Column(Float, nullable=False)
    discount_percentage     = Column(Float, nullable=False)
    discount_amount         = Column(Float, nullable=False)
    effective_from_date     = Column(DateTime, nullable=False, default=func.now())
    effective_to_date       = Column(DateTime, default=None)
    created_by              = Column(Integer, default=None)
    created_on              = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    is_deleted_directly     = Column(Enum('yes', 'no'), nullable=False, default='no')
    is_deleted_with_master  = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer, default=None)
    deleted_on              = Column(DateTime, default=None)

 
 
class PriceListProductModule(caerp_base):
    __tablename__ = 'price_list_product_module'

    id                      = Column(Integer, primary_key=True, index=True)
    price_list_product_master_id   = Column(Integer, nullable=False)
    module_id                      = Column(Integer, nullable=False)
    module_price                   = Column(Float, nullable=False)
    igst_rate                = Column(Float, nullable=False)
    cgst_rate               = Column(Float, nullable=False)
    sgst_rate               = Column(Float, nullable=False)
    cess_rate               = Column(Float, nullable=False)
    discount_percentage     = Column(Float, nullable=False)
    discount_amount         = Column(Float, nullable=False)
    effective_from_date     = Column(Date, nullable=False)
    effective_to_date       = Column(Date, default=None)
    created_by              = Column(Integer, default=None)
    created_on              = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    is_deleted_directly     = Column(Enum('yes', 'no'), nullable=False, default='no')
    is_deleted_with_master  = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer, default=None)
    deleted_on              = Column(DateTime, default=None)


class PriceListProductModuleView(caerp_base):
    __tablename__ = 'view_price_list_product_module'

    price_list_product_module_id   = Column(Integer, primary_key=True, index=True)
    price_list_product_master_id   = Column(Integer, nullable=False)
    product_master_id              = Column(Integer, nullable=False)
    module_name                    = Column(String, nullable=False)
    module_id                      = Column(Integer, nullable=False)
    product_code                   = Column(String, nullable=False)
    product_name                   = Column(String, nullable=False)
    module_description             = Column(String, nullable=False)
    module_price                   = Column(Float, nullable=False)
    module_igst_rate                = Column(Float, nullable=False)
    module_cgst_rate               = Column(Float, nullable=False)
    module_sgst_rate               = Column(Float, nullable=False)
    module_cess_rate               = Column(Float, nullable=False)
    module_discount_percentage     = Column(Float, nullable=False)
    module_discount_amount         = Column(Float, nullable=False)
    module_effective_from_date     = Column(Date, nullable=False)
    module_effective_to_date       = Column(Date, default=None)
    master_price                   = Column(Float, nullable=False)
    master_igst_rate                = Column(Float, nullable=False)
    master_cgst_rate               = Column(Float, nullable=False)
    master_sgst_rate               = Column(Float, nullable=False)
    master_cess_rate               = Column(Float, nullable=False)
    master_discount_percentage     = Column(Float, nullable=False)
    master_discount_amount         = Column(Float, nullable=False)
    master_effective_from_date     = Column(Date, nullable=False)
    master_effective_to_date       = Column(Date, default=None)
    created_by              = Column(Integer, default=None)
    created_on              = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    is_deleted_directly     = Column(Enum('yes', 'no'), nullable=False, default='no')
    is_deleted_with_master  = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer, default=None)
    deleted_on              = Column(DateTime, default=None)


class ProductRating(caerp_base):
    __tablename__ = 'product_rating'

    id              = Column(Integer, primary_key=True, index=True)
    product_master_id = Column(Integer, nullable=False)
    user_id           = Column(Integer, nullable=False)
    rating            = Column(Float, nullable=False)
    comment           = Column(String, nullable=False)
    created_on        = Column(DateTime, nullable=False,default=func.now())

class ProductMasterPrice(caerp_base):
    __tablename__ = 'product_master_price'

    id                      = Column(Integer, primary_key=True, index=True)
    product_master_id       = Column(Integer, nullable=False)
    price                   = Column(Float, nullable=False) 
    gst_rate                = Column(Float, nullable=False) 
    cess_rate               = Column(Float, nullable=False)  
    effective_from_date     = Column(Date, nullable=False)
    effective_to_date       = Column(Date, default=None)
    created_by              = Column(Integer, nullable=False)
    created_on              = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer, default=None)
    deleted_on              = Column(DateTime, default=None)



class ViewProductMasterPrice(caerp_base):
    __tablename__ = 'view_product_master_price'

    product_master_id       = Column(Integer, nullable=False)
    product_master_price_id = Column(Integer, primary_key=True, index=True)
    category_id     = Column(Integer, nullable=False)
    product_code    = Column(String, nullable=False)
    product_name    = Column(String, nullable=False)
    product_description_main = Column(String, nullable=False)
    product_description_sub = Column(String, nullable=False)
    has_module         = Column(Enum('yes', 'no'), nullable=False, default='no')
    created_by       = Column(Integer, nullable=False)
    created_on              = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer, default=None)
    deleted_on              = Column(DateTime, default=None)
    price                   = Column(Float, nullable=False) 
    gst_rate                = Column(Float, nullable=False) 
    cess_rate               = Column(Float, nullable=False)  
    effective_from_date     = Column(Date, nullable=False)
    effective_to_date       = Column(Date, default=None)
    price_is_deleted        = Column(Enum('yes', 'no'), nullable=False, default='no')





class ProductModulePrice(caerp_base):
    __tablename__ = 'product_module_price'

    id                      = Column(Integer, primary_key=True, index=True)
    product_master_price_id       = Column(Integer, nullable=False)
    module_id       = Column(Integer, nullable=False)
    module_price                   = Column(Float, nullable=False) 
    gst_rate                = Column(Float, nullable=False) 
    cess_rate               = Column(Float, nullable=False)  
    effective_from_date     = Column(Date, nullable=False)
    effective_to_date       = Column(Date, default=None)
    created_by              = Column(Integer, nullable=False)
    created_on              = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer, default=None)
    deleted_on              = Column(DateTime, default=None)



class ViewProductModulePrice(caerp_base):
    __tablename__ = 'view_product_module_price'

    product_module_id       = Column(Integer, nullable=False)
    product_master_id       = Column(Integer, nullable=False)
    product_master_price_id = Column(Integer, nullable=False)
    product_module_price_id = Column(Integer, primary_key=True, index=True)
    
    module_name         = Column(String, nullable=False)
    module_description  = Column(String, nullable=False)
    display_order       = Column(Integer, nullable=False)
    created_by       = Column(Integer, nullable=False)
    created_on              = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer, default=None)
    deleted_on              = Column(DateTime, default=None)
    module_price                   = Column(Float, nullable=False) 
    gst_rate                = Column(Float, nullable=False) 
    cess_rate               = Column(Float, nullable=False)  
    effective_from_date     = Column(Date, nullable=False)
    effective_to_date       = Column(Date, default=None)


class OfferCategory(caerp_base):
    __tablename__ ='offer_category'

    id              = Column(Integer, primary_key=True, index=True)
    offer_category  = Column(String, nullable=False)

class OfferMaster(caerp_base):
    __tablename__ = "offer_master"

    id                  = Column(Integer, primary_key=True, index=True)
    offer_category_id   = Column(Integer, nullable=False)
    offer_name          = Column(String, nullable=False)
    offer_percentage    = Column(Float, default=0.0)
    offer_amount        = Column(Float, default=0.0)
    effective_from_date = Column(Date, nullable=False)
    effective_to_date   = Column(Date, default=None)
    created_by          = Column(Integer, nullable=False)
    created_on              = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer, default=None)
    deleted_on              = Column(DateTime, default=None)

class OfferDetails(caerp_base):
    __tablename__ = 'offer_details'

    id                  = Column(Integer, primary_key=True, index=True)
    offer_master_id     = Column(Integer, nullable=False)
    product_master_id   = Column(Integer, nullable=False)
    created_by          = Column(Integer, nullable=False)
    created_on              = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer, default=None)
    deleted_on              = Column(DateTime, default=None)

class OfferDetailsView(caerp_base):
    __tablename__ = 'view_offer_details'

    offer_details_id             = Column(Integer, primary_key=True, index=True) 
    offer_master_id              = Column(Integer, nullable=False)
    offer_category_id            = Column(Integer, nullable=False)
    offer_category               = Column(String, nullable=False)
    offer_name                   = Column(String, nullable=False)
    offer_percentage             = Column(Float, default=0.0)
    offer_amount                 = Column(Float, default=0.0)
    product_master_id            = Column(Integer, nullable=False)
    product_name                 = Column(String, nullable=False)
    product_code                 = Column(String, default=None)
    effective_from_date          = Column(Date, nullable=False)
    effective_to_date            = Column(Date, default=None)
    offer_details_created_by                   = Column(Integer, nullable=False)
    offer_details_created_on                   = Column(DateTime, nullable=False, default=func.now())
    offer_details_modified_by                  = Column(Integer, default=None)
    offer_details_modified_on                  = Column(DateTime, default=None)
    offer_details_is_deleted                   = Column(Enum('yes', 'no'), nullable=False, default='no')
    offer_details_deleted_by                   = Column(Integer, default=None)
    offer_details_deleted_on                   = Column(DateTime, default=None)


class CartDetails(caerp_base):
    __tablename__ = 'cart_details'

    id                  = Column(Integer, primary_key=True, index=True)
    product_master_id   = Column(Integer, nullable=False)
    customer_id         = Column(Integer, nullable=False)
    saved_for_later     = Column(Enum('yes', 'no'), nullable=False, default='no') 
    is_deleted          = Column(Enum('yes', 'no'), nullable=False, default='no')                     

class CouponMaster(caerp_base):
    __tablename__ = 'coupon_master'

    id                  = Column(Integer, primary_key=True, index=True)
    coupon_name         = Column(String(50), nullable=False)
    coupon_code         = Column(String(50), nullable=False)
    coupon_percentage   = Column(Float, default=0.0)
    coupon_amount       = Column(Float, default=0.0)
    effective_from_date = Column(Date, nullable=False)
    effective_to_date   = Column(Date, default=None)
    created_by          = Column(Integer, nullable=False)
    created_on              = Column(DateTime, nullable=False, default=func.now())
    modified_by             = Column(Integer, default=None)
    modified_on             = Column(DateTime, default=None)
    is_deleted              = Column(Enum('yes', 'no'), nullable=False, default='no')
    deleted_by              = Column(Integer, default=None)
    deleted_on              = Column(DateTime, default=None)

class PracticingAs(caerp_base):
    __tablename__ = 'app_practicing_as'

    id                  = Column(Integer, primary_key=True, index=True)
    practicing_type         = Column(String(50), nullable=False)
    display_number         = Column(Integer, nullable=False)

class AreaOfPracticing(caerp_base):
    __tablename__ = 'app_area_of_practicing'

    id                  = Column(Integer, primary_key=True, index=True)
    practicing_type     = Column(String(50), nullable=False)
    display_number      = Column(Integer, nullable=False)

class ProfessionalQualification(caerp_base):
    __tablename__ ='app_professional_qualification'

    id              = Column(Integer, primary_key=True, index=True)
    qualification   = Column(String(50), nullable=False)
    display_number  = Column(Integer, nullable=False)


class CustomerAreaOfPracticing(caerp_base):
    __tablename__ = 'customer_area_of_practicing'

    id              = Column(Integer, primary_key=True, index=True)
    customer_id     = Column(Integer, nullable=False)
    area_of_practicing_id = Column(Integer, nullable=False)
    other           = Column(String, default=None)
    created_on      = Column(DateTime, nullable=False)
    modified_on     = Column(DateTime, default=None)
    is_deleted      = Column(Enum('yes', 'no'), nullable=False, default='no')


class CustomerPracticingAs(caerp_base):
    __tablename__ = 'customer_practicing_as'

    id              = Column(Integer, primary_key=True, index=True)
    customer_id     = Column(Integer, nullable=False)
    practicing_type_id = Column(Integer, nullable=False)
    other           = Column(String, default=None)
    created_on      = Column(DateTime, nullable=False)
    modified_on     = Column(DateTime, default=None)
    is_deleted      = Column(Enum('yes', 'no'), nullable=False, default='no')

class CustomerProfessionalQualification(caerp_base):
    __tablename__ = 'customer_professional_qualification'

    id              = Column(Integer, primary_key=True, index=True)
    customer_id     = Column(Integer, nullable=False)
    profession_type_id = Column(Integer, nullable=False)
    membership_number	= Column(Integer, nullable=False)
    enrollment_date     = Column(Date, default=None)
    created_on      = Column(DateTime, nullable=False)
    modified_on     = Column(DateTime, default=None)
    is_deleted      = Column(Enum('yes', 'no'), nullable=False, default='no')

