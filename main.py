 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware 

from caerp_auth import authentication
from caerp_router import get,site_manager,admin,menu,customer,product

from caerp_router import test
from caerp_db.database import caerp_base, caerp_engine
from fastapi.staticfiles import StaticFiles



caerp_base.metadata.create_all(bind=caerp_engine)

app = FastAPI(
    debug=True,
    title="Main Application API",
    description="""
        Welcome to the Main Application API! Here, you can find documentation for various endpoints related to different modules.

        ## Documentation Links:
        - [Get Module](/get/docs): Documentation for endpoints related to the Get module.
        - [Admin Module](/admin/docs): Documentation for endpoints related to the Admin module.
        - [Menu Module](/menu/docs): Documentation for endpoints related to the Menu module.
        - [Site Manager Module](/sitemanager/docs): Documentation for endpoints related to the Site Manager module.
        - [Customer Module](/customer/docs): Documentation for endpoints related to the customer module.
        - [Product Module](/product/docs): Documentation for endpoints related to the product module.
    """
)
app_get=FastAPI()
app_admin=FastAPI(debug=True)
app_site_manager=FastAPI(debug=True)
app_menu=FastAPI()
app_customer=FastAPI(debug=True)
app_product=FastAPI(debug=True)
app_test=FastAPI()




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key="da30300a84b6fa144a20702bd15acac18ff3954aa67e72b485d59df5e27fb5d3")

try:
    caerp_engine.connect()
    print("Database connection established.")
except Exception as e:
    print(f"Error connecting to the database: {e}")


# instance of the APIRouter class.

app.include_router(authentication.router)
app.include_router(test.router)


app.include_router(product.router)

# for app_tables
app_get.include_router(authentication.router)
app_get.include_router(get.router)

# for 
app_admin.include_router(authentication.router)
app_admin.include_router(admin.router)

# for app_site_pages
app_site_manager.include_router(authentication.router)
app_site_manager.include_router(site_manager.router)

# for menus
app_menu.include_router(authentication.router)
app_menu.include_router(menu.router)

# for customer_tables
app_customer.include_router(authentication.router)
app_customer.include_router(customer.router)

app_product.include_router(authentication.router)
app_product.include_router(product.router)

app_test.include_router(authentication.router)
app_test.include_router(test.router)








app.mount("/get", app_get, name="get")
app.mount("/admin", app_admin, name="admin")
app.mount("/sitemanager", app_site_manager, name="sitemanager")
app.mount("/menu", app_menu, name="menu")
app.mount("/customer", app_customer, name="customer")
app.mount("/product", app_product, name="product")
app.mount("/test", app_test, name="test")





app_site_manager.mount("/save_director", StaticFiles(directory="uploads/our_directors"), name="uploads")

app_site_manager.mount("/save_team", StaticFiles(directory="uploads/our_teams"), name="teams")

app_site_manager.mount("/save_trending_news", StaticFiles(directory="uploads/trending_news"), name="news")
app_site_manager.mount("/save_image_gallery", StaticFiles(directory="uploads/image_gallery"), name="gallery")
app_admin.mount("/add/admin_users", StaticFiles(directory="uploads/admin_profile"), name="gallery")
app_product.mount("/save_product_module", StaticFiles(directory="uploads/product_module_images"), name="product")
app_product.mount("/save_product_master", StaticFiles(directory="uploads/product_master_videos"), name="product")
app_product.mount("/save_product_master", StaticFiles(directory="uploads/product_master_images"), name="product")

app_product.mount("/save_product_additional_videos", StaticFiles(directory="uploads/product_master_additional_videos"), name="product")
app_site_manager.mount("/save_prime_customer",StaticFiles(directory="uploads/prime_customers"), name="customer")


app_customer.mount("/save_customer_company_profile",StaticFiles(directory="uploads/company_logo"), name="customer")
app_customer.mount("/image/add_customer_profile_image",StaticFiles(directory="uploads/customer_profile_photo"), name="customer")




















