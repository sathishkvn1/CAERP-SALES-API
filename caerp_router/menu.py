from fastapi import APIRouter, Depends,HTTPException,status
from typing import List
from caerp_db.models import AdminSubMenuPermission, ClientMainMenu
from caerp_auth.authentication import authenticate_user
from caerp_schemas import AdminMainMenuCreate, AdminMainMenuDeleteSchema, AdminSubMenuCreate, AdminSubMenuDeleteSchema, ClientMenu, ClientMenuBase, ClientMenuResponse, PublicMainMenuCreate, PublicSubMenuCreate, PublicSubSubMenuCreate, SiteLegalAboutUsBaseResponse

from sqlalchemy.orm import Session
from caerp_db.database import get_db
from caerp_db import db_menu
import jwt
from datetime import datetime, timedelta
from caerp_auth.oauth2 import get_current_user,oauth2_scheme,SECRET_KEY, ALGORITHM
from caerp_auth import oauth2
from sqlalchemy import text
from UserDefinedConstants.user_defined_constants import DeletedStatus


from jose import JWTError, jwt
from fastapi import Path
from starlette.requests import Request

router = APIRouter(
    prefix="/menu",
    tags=["MENU"]
)





@router.get('/admin_menu/get_main_menus')
def get_main_menu_permission_is_granted(
    request: Request,
    token: str = Depends(oauth2.oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    if not request.session.get("user_id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID missing in session")

    role_id = request.session.get("role_id")
    menu_data = db_menu.get_menu_data_by_role_with_sub_menu(db, role_id)
    if not menu_data:
        raise HTTPException(status_code=404, detail="Menu data not found")
    

    response_menu = []
    for menu_item in menu_data:
        if menu_item.main_menu_permission_is_granted  == "yes":
            response_menu.append({
                "main_menu_id": menu_item.main_menu_id,
                "main_menu": menu_item.main_menu,
                "main_menu_has_sub_menu": menu_item.main_menu_has_sub_menu,
                "main_menu_display_order": menu_item.main_menu_display_order,
                "main_menu_page_link": menu_item.main_menu_page_link,
                "main_menu_permission_id": menu_item.main_menu_permission_id,
                "main_menu_permission_role_id": menu_item.main_menu_permission_role_id,
                "main_menu_permission_is_granted": menu_item.main_menu_permission_is_granted,
            })
    
    return {"menu": response_menu}


#--------------------------------------------------------------------------------------------------------------

@router.get('/admin_menu/get_all_menu')
def get_main_menu_data(
    request: Request,
    token: str = Depends(oauth2.oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    if not request.session.get("user_id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID missing in session")
    
    role_id = request.session.get("role_id")
    
    menu_data = db_menu.get_menu_data_by_role(db, role_id)
    if not menu_data:
        raise HTTPException(status_code=404, detail="Menu data not found")
    
    response_menu = []
    for menu_item in menu_data:
        if menu_item.main_menu_has_sub_menu == "yes":
            # Fetch sub-menu permissions
            sub_menu_permissions = db_menu.get_sub_menu_permissions(db, menu_item.main_menu_id,role_id)
            print("Sub-menu permissions for main menu", menu_item.main_menu_id, ":", sub_menu_permissions)
        else:
            sub_menu_permissions = []  # No sub-menu permissions for this menu item
        
        response_menu.append({
            "main_menu_id": menu_item.main_menu_id,
            "main_menu": menu_item.main_menu,
            "main_menu_has_sub_menu": menu_item.main_menu_has_sub_menu,
            "main_menu_display_order": menu_item.main_menu_display_order,
            "main_menu_page_link": menu_item.main_menu_page_link,
            "main_menu_permission_id":menu_item.main_menu_permission_id,
            "main_menu_permission_role_id":menu_item.main_menu_permission_role_id,
            "main_menu_permission_is_granted":menu_item.main_menu_permission_is_granted,
            "sub_menu": [
                {
                    "sub_menu_id": sub_menu.sub_menu_id,
                    "sub_menu": sub_menu.sub_menu,
                    "sub_menu_has_sub_menu": sub_menu.sub_menu_has_sub_menu,
                    "sub_menu_display_order": sub_menu.sub_menu_display_order,
                    "sub_menu_page_link": sub_menu.sub_menu_page_link,
                    "sub_menu_permission_id": sub_menu.sub_menu_permission_id,
                    "sub_menu_permission_role_id": sub_menu.sub_menu_permission_role_id,
                    "sub_menu_permission_is_granted": sub_menu.sub_menu_permission_is_granted
                    
                }
                for sub_menu in sub_menu_permissions
            ]
        })
    
    return {"menu": response_menu}


#--------------------------------------------------------------------------------------------------------------


@router.post('/admin_menu/add/admin_main_menu', response_model=AdminMainMenuCreate)
def create_admin_main_menu(
        request: AdminMainMenuCreate,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    
    
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    new_user = db_menu.create_admin_main_menu(db, request, user_id)
    
    return new_user


 #--------------------------------------------------------------------------------------------------------------   




@router.post("/admin_menu/update/admin_main_menu/{id}", response_model=AdminMainMenuCreate)
def update_user_role(id: int,
                     role_input: AdminMainMenuCreate,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"] 
    return db_menu.update_admin_main_menu(db, id, role_input, modified_by=user_id)


#--------------------------------------------------------------------------------------------------------------   



@router.delete("/admin_menu/delete/admin_main_menu/{id}", response_model=AdminMainMenuDeleteSchema)
def delete_admin_main_menu(id: int,
                     role_input: AdminMainMenuDeleteSchema,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"] 
    return db_menu.delete_admin_main_menu(db, id, role_input, deleted_by=user_id)


#--------------------------------------------------------------------------------------------------------------   


@router.post('/admin_menu/add/admin_sub_menu/{main_menu_id}', response_model=AdminSubMenuCreate)
def create_admin_sub_menu(
        request: AdminSubMenuCreate,
        main_menu_id: int = Path(..., title="Main Menu ID"),
        token: str = Depends(oauth2.oauth2_scheme),
        db: Session = Depends(get_db)
):
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"] 
    new_user = db_menu.create_admin_sub_menu(db, main_menu_id, request, user_id)
    return new_user

#--------------------------------------------------------------------------------------------------------------   



@router.post('/admin_menu/update/admin_sub_menu/{main_menu_id}/{id}', response_model=AdminSubMenuCreate)
def create_admin_sub_menu(
        id: int,
        request: AdminSubMenuCreate,
        main_menu_id: int = Path(..., title="Main Menu ID"),
        token: str = Depends(oauth2.oauth2_scheme),
        db: Session = Depends(get_db)
):
    
    auth_info = authenticate_user(token) 
    user_id = auth_info["user_id"]
    new_user = db_menu.update_admin_sub_menu(id,db, main_menu_id, request, user_id)
    return new_user

#--------------------------------------------------------------------------------------------------------------   


@router.delete("/admin_menu/delete/admin_sub_menu/{id}", response_model=AdminSubMenuDeleteSchema)
def delete_user_role(
                     request: Request,
                     id: int,
                     role_input: AdminSubMenuDeleteSchema,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    if not request.session.get("user_id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID missing in session")
    
    user_id = request.session.get("user_id")
    return db_menu.delete_admin_sub_menu(db, id, role_input, deleted_by=user_id)


#--------------------------------------------------------------------------------------------------------------   


@router.get('/admin_menu/get_all_menu_with_role_and_permission')
def get_main_menu_data(
    request: Request,
    token: str = Depends(oauth2.oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    if not request.session.get("user_id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID missing in session")
    
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    role_id = auth_info["role_id"]
    

    menu_data = db_menu.get_menu_data_by_role_and_permission(db, role_id, "yes")
    
    if not menu_data:
        raise HTTPException(status_code=404, detail="Menu data not found")
    
    response_menu = []
    for menu_item in menu_data:
        print("Main Menu ID:", menu_item.main_menu_id)
        print("role ID:", role_id)
        if menu_item.main_menu_has_sub_menu == "yes":
            # Fetch sub-menu permissions
            sub_menu_permissions = get_sub_menu_by_role_and_permission(db, menu_item.main_menu_id, role_id)
            print("Sub-menu permissions for main menu", menu_item.main_menu_id, ":", sub_menu_permissions)
        else:
            sub_menu_permissions = []  # No sub-menu permissions for this menu item
        
        response_menu.append({
            "main_menu_id": menu_item.main_menu_id,
            "main_menu": menu_item.main_menu,
            "main_menu_has_sub_menu": menu_item.main_menu_has_sub_menu,
            "main_menu_display_order": menu_item.main_menu_display_order,
            "main_menu_page_link": menu_item.main_menu_page_link,
            "main_menu_permission_id": menu_item.main_menu_permission_id,
            "main_menu_permission_role_id": menu_item.main_menu_permission_role_id,
            "main_menu_permission_is_granted": menu_item.main_menu_permission_is_granted,
            "sub_menu": [
                {
                    "sub_menu_id": sub_menu.sub_menu_id,
                    "sub_menu": sub_menu.sub_menu,
                    "sub_menu_has_sub_menu": sub_menu.sub_menu_has_sub_menu,
                    "sub_menu_display_order": sub_menu.sub_menu_display_order,
                    "sub_menu_page_link": sub_menu.sub_menu_page_link,
                    "sub_menu_permission_id": sub_menu.sub_menu_permission_id,
                    "sub_menu_permission_role_id": sub_menu.sub_menu_permission_role_id,
                    "sub_menu_permission_is_granted": sub_menu.sub_menu_permission_is_granted
                }
                for sub_menu in sub_menu_permissions
            ]
        })
    
    return {"menu": response_menu}



def get_sub_menu_by_role_and_permission(db: Session, main_menu_id: int, role_id: int):
    sql_query = text(
    "SELECT * FROM app_view_admin_sub_menu_permission "
    "WHERE main_menu_id = :main_menu_id "
    "AND sub_menu_permission_role_id = :role_id "
    "AND sub_menu_permission_is_granted = 'yes'"
)

    print("SQL Query:", sql_query, " with parameters: main_menu_id =", main_menu_id, "and role_id =", role_id)
    try:
        result = db.execute(sql_query, {"main_menu_id": main_menu_id, "role_id": role_id}).fetchall()
        print("Query Result:", result)  
        return result
    except Exception as e:
        print("Error executing query:", e)  
        raise
    

#--------------------------------------------------------------------------------------------------------------   

@router.post('/client_menu/save_client_menu/{id}', response_model=ClientMenuBase)
def save_client_menu(
        id: int = 0,  # Default to 0 for add operation
        menu_data: ClientMenuBase = Depends(),
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
):
    # Check authorization
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]

    try:
        menu = db_menu.save_client_menu(db, menu_data, id, user_id)
        return menu  # Return the menu data as response
    except Exception as e:
        error_detail = [{
            "loc": ["server"],
            "msg": "Internal server error",
            "type": "internal_server_error"
        }]
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

#--------------------------------------------------------------------------------------------------------------      

@router.delete("/client_menu/delete/client_menu/{id}")
def delete_client_menu(
                     
                     id: int,
                     db: Session = Depends(get_db),
                     token: str = Depends(oauth2.oauth2_scheme)):
    
    
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    auth_info = authenticate_user(token)
    user_id = auth_info["user_id"]
    
    return db_menu.delete_client_menu(db, id, deleted_by=user_id)
   
#--------------------------------------------------------------------------------------------------------------      

@router.get("/client_menu/get_client_menu_by_id/{id}", response_model=ClientMenuResponse)
def get_client_menu_by_id(id: int,
                        db: Session = Depends(get_db)):
    
    detail = db_menu.get_client_menu_by_id(db, id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Not found with ID {id}")
    return {"menu": [detail]}

#--------------------------------------------------------------------------------------------------------------      
@router.get("/client_menu/get_all_client_menu/" , response_model=List[ClientMenu])
async def get_all_trending_news(deleted_status: DeletedStatus = DeletedStatus.NOT_DELETED,
                              db: Session = Depends(get_db),
                             ):
    return get_all_trending_news(db, deleted_status)



def get_all_trending_news(db: Session, deleted_status: DeletedStatus):
    if deleted_status == DeletedStatus.DELETED:
        return db.query(ClientMainMenu).filter(ClientMainMenu.is_deleted == 'yes').all()
    elif deleted_status == DeletedStatus.NOT_DELETED:
        return db.query(ClientMainMenu).filter(ClientMainMenu.is_deleted == 'no').all()
    elif deleted_status == DeletedStatus.ALL:
        return db.query(ClientMainMenu).all()
    else:
       
        raise ValueError("Invalid deleted_status")
		    
#--------------------------------------------------------------------------------------------------------------      
@router.post('/public_menu/add/public_main_menu', response_model=PublicMainMenuCreate)
def create_public_main_menu(
        request: Request,
        public_main_menu_create: PublicMainMenuCreate,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2.oauth2_scheme)
 ):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    if not request.session.get("user_id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID missing in session")
    
    user_id = request.session.get("user_id")
    
    new_user = db_menu.create_public_main_menu(db, public_main_menu_create, user_id)
    
    return new_user

#--------------------------------------------------------------------------------------------------------------      
# check from here
@router.get('/public_menu/get_all_menu')
def get_public_main_menu_data(
    request: Request,
    # token: str = Depends(oauth2.oauth2_scheme),
    db: Session = Depends(get_db)
 ):
    # if not token:
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    # if not request.session.get("user_id"):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID missing in session")
    
    
    menu_data   = db_menu.get_public_menu_data(db) 
    
    if not menu_data:
        raise HTTPException(status_code=404, detail="Menu data not found")
    
    response_menu = []
    for menu_item in menu_data:
        sub_menu_data = []  # Initialize sub_menu_data here
        if menu_item.has_sub_menu == "yes":
            sub_menu_data = db_menu.get_public_sub_menu_data(db, menu_item.id)
        
        response_menu.append({
            "main_menu_id": menu_item.id,
            "main_menu": menu_item.menu,
            "main_menu_has_sub_menu": menu_item.has_sub_menu,
            "main_menu_display_order": menu_item.display_order,
            "main_menu_page_link": menu_item.page_link,
            "sub_menu": []
        })
        
        for sub_menu in sub_menu_data:
            sub_sub_menu_data = []  # Initialize sub_sub_menu_data here
            if sub_menu.has_sub_menu == "yes":
                sub_sub_menu_data = db_menu.get_public_sub_sub_menu_data(db, sub_menu.id)
            
            response_menu[-1]["sub_menu"].append({
                "sub_menu_id": sub_menu.id,
                "sub_menu": sub_menu.sub_menu,
                "sub_menu_has_sub_menu": sub_menu.has_sub_menu,
                "sub_menu_display_order": sub_menu.display_order,
                "sub_menu_page_link": sub_menu.page_link,
                "sub_sub_menu": [
                    {
                        "sub_sub_menu_id": sub_sub_menu.id,
                        "sub_menu_id": sub_sub_menu.sub_menu_id,
                        "sub_sub_menu": sub_sub_menu.sub_sub_menu,
                        "display_order": sub_sub_menu.display_order,
                        "page_link": sub_sub_menu.page_link
                    }
                    for sub_sub_menu in sub_sub_menu_data
                ]
            })

    return {"menu": response_menu}
#--------------------------------------------------------------------------------------------------------------      

@router.post('/public_menu/add/public_sub_menu/{main_menu_id}', response_model=PublicSubMenuCreate)
def create_public_sub_menu(
        request: Request,
        input: PublicSubMenuCreate,
        main_menu_id: int = Path(..., title="Main Menu ID"),
        token: str = Depends(oauth2.oauth2_scheme),
        db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    if not request.session.get("user_id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID missing in session")
    if main_menu_id == 2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sub-menu cannot be inserted for main_menu_id=2")
    user_id = request.session.get("user_id")

    new_user = db_menu.create_public_sub_menu(db, main_menu_id, input, user_id)
    return new_user

#--------------------------------------------------------------------------------------------------------------      

@router.post('/public_menu/add/public_sub_sub_menu/{sub_menu_id}', response_model=PublicSubSubMenuCreate)
def create_public_sub_sub_menu(
        request: Request,
        input: PublicSubSubMenuCreate,
        sub_menu_id: int = Path(..., title="Sub Menu ID"),
        token: str = Depends(oauth2.oauth2_scheme),
        db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")

    if not request.session.get("user_id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID missing in session")
    if sub_menu_id == 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="sub_sub-menu cannot be inserted for sub_menu_id=1")
    
    # STATUS_CODE_SUB_MENU_NOT_ALLOWED = 601
    # if sub_menu_id == 1:
    #     raise HTTPException(status_code=STATUS_CODE_SUB_MENU_NOT_ALLOWED, detail="Sub-menu cannot be inserted for main_menu_id=2")
    user_id = request.session.get("user_id")

    new_user = db_menu.create_public_sub_sub_menu(db, sub_menu_id, input, user_id)
    return new_user
#--------------------------------------------------------------------------------------------------------------      