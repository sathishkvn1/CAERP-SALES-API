from fastapi import HTTPException,status
from UserDefinedConstants.user_defined_constants import ActionType
from caerp_db.models import AdminMainMenu, AdminMainMenuPermission, AdminSubMenu,AdminSubMenuPermission, ClientMainMenu, PublicMainMenu, PublicSubMenu, PublicSubSubMenu, SiteLegalAboutUs
from caerp_schemas import AdminMainMenuCreate, AdminMainMenuDeleteSchema, AdminSubMenuCreate, AdminSubMenuDeleteSchema, ClientMenuBase, PublicMainMenuCreate, PublicSubMenuCreate, PublicSubSubMenuCreate
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import and_
from datetime import datetime



def get_menu_data_by_role(db: Session, role_id: int):
    return db.query(AdminMainMenuPermission).filter_by(main_menu_permission_role_id=role_id).all()

def get_menu_data_by_role_with_sub_menu(db: Session, role_id: int):
    return db.query(AdminMainMenuPermission).filter(
        and_(
            AdminMainMenuPermission.main_menu_permission_role_id == role_id,
            AdminMainMenuPermission.main_menu_permission_is_granted  == "yes"
        )
    ).all()
    



def get_sub_menu_permissions(db: Session, main_menu_id: int, role_id: int):
    sql_query = text(
        "SELECT * FROM app_view_admin_sub_menu_permission WHERE main_menu_id = :main_menu_id AND sub_menu_permission_role_id = :role_id"
    )
    return db.execute(sql_query, {"main_menu_id": main_menu_id, "role_id": role_id}).fetchall()




def save_admin_main_menu(db: Session, request: AdminMainMenuCreate, id: int, user_id: int):

    if id == 0:
        # Add operation
        menu_data_dict = request.dict()
        menu_data_dict["created_on"] = datetime.utcnow()
        menu_data_dict["created_by"] = user_id
        new_menu_category = AdminMainMenu(**menu_data_dict)
        db.add(new_menu_category)
        db.commit()
        db.refresh(new_menu_category)
        return new_menu_category
    
    else:
        # Update operation
        menu_to_update = db.query(AdminMainMenu).filter(AdminMainMenu.main_menu_id == id).first()
        if menu_to_update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
        
        menu_data_dict = request.dict(exclude_unset=True)
        for key, value in menu_data_dict.items():
            setattr(menu_to_update, key, value)
        menu_to_update.modified_by = user_id
        menu_to_update.modified_on = datetime.utcnow()
        
        db.commit()
        db.refresh(menu_to_update)
        return menu_to_update


 


def delete_admin_main_menu(db: Session, id: int, action: ActionType, user_id: int):
    menu_item = db.query(AdminMainMenu).filter(AdminMainMenu.main_menu_id == id).first()
    if menu_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    if action == ActionType.DELETE:
        if menu_item.is_deleted == 'yes':
            raise HTTPException(status_code=400, detail="Menu item already deleted")
        
        menu_item.is_deleted = 'yes'
        menu_item.deleted_by = user_id
        menu_item.deleted_on = datetime.utcnow()
    elif action == ActionType.UNDELETE:
        if menu_item.is_deleted == 'no':
            raise HTTPException(status_code=400, detail="Menu item not deleted")
        
        menu_item.is_deleted = 'no'

    
    db.commit()
    return {"success": True, "message": f"Menu item {action.value.lower()} successfully"}




def save_admin_sub_menu(db: Session, main_menu_id: int, request: AdminSubMenuCreate, user_id: int, id: int = 0):
    print("main_menu_id:", main_menu_id)
    print("request:", request)
    print("user_id:", user_id)
    print("id:", id)
    
    if id == 0:
        # Add operation
        new_sub_menu = AdminSubMenu(
            main_menu_id=main_menu_id,  
            sub_menu=request.sub_menu,
            sub_menu_has_sub_menu=request.sub_menu_has_sub_menu,
            sub_menu_display_order=request.sub_menu_display_order,
            sub_menu_page_link=request.sub_menu_page_link,
            created_by=user_id  
        )
        db.add(new_sub_menu)
        db.commit()
        db.refresh(new_sub_menu)
        return new_sub_menu
    else:
        # Update operation
        existing_menu = db.query(AdminSubMenu).filter(AdminSubMenu.sub_menu_id == id).first()
        print("existing_menu:", existing_menu)

        if existing_menu is None:
            raise HTTPException(status_code=404, detail="Menu not found")

        for field, value in request.dict(exclude_unset=True).items():
            setattr(existing_menu, field, value)

        existing_menu.modified_by = user_id
        existing_menu.main_menu_id = main_menu_id
        existing_menu.modified_on = datetime.utcnow()
        
        db.commit()
        db.refresh(existing_menu)

        return existing_menu

    



def delete_admin_sub_menu(db: Session, id: int, action: ActionType, user_id: int) -> tuple:
    menu_item = db.query(AdminSubMenu).filter(AdminSubMenu.sub_menu_id == id).first()
    if menu_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    
    if action == ActionType.DELETE:
        if menu_item.is_deleted == 'yes':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Menu item already deleted")
        
        menu_item.is_deleted = 'yes'
        menu_item.deleted_by = user_id
        menu_item.deleted_on = datetime.utcnow()
        db.commit()
        return (True, "Menu item deleted successfully")
    
    elif action == ActionType.UNDELETE:
        if menu_item.is_deleted == 'no':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Menu item not deleted")
        
        menu_item.is_deleted = 'no'
        db.commit()
        return (True, "Menu item undeleted successfully")

    
# test

def get_menu_data_by_role_and_permission(db: Session, role_id: int, main_menu_permission: str):
    return db.query(AdminMainMenuPermission).filter(
        and_(
            AdminMainMenuPermission.main_menu_permission_role_id == role_id,
            AdminMainMenuPermission.main_menu_permission_is_granted  == main_menu_permission
        )
    ).all()

  
def save_client_menu(db: Session, menu_data: ClientMenuBase, id: int, user_id: int):

    if id == 0:
        # Add operation
        client_menu_dict = menu_data.dict()
        client_menu_dict["created_by"] = user_id
        client_menu_dict["created_on"] = datetime.utcnow()
        new_menu = ClientMainMenu(**client_menu_dict)
        db.add(new_menu)
        db.commit()
        db.refresh(new_menu)
        return new_menu
    else:
        # Update operation
        menu = db.query(ClientMainMenu).filter(ClientMainMenu.id == id).first()
        if menu is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
        client_menu_dict = menu_data.dict(exclude_unset=True)
        for key, value in client_menu_dict.items():
            setattr(menu, key, value)
        menu.modified_by = user_id
        menu.modified_on = datetime.utcnow()
        db.commit()
        db.refresh(menu)
        return menu


    

# def delete_client_menu(db: Session, id: int, deleted_by: int):
#     result = db.query(ClientMainMenu).filter(ClientMainMenu.id == id).first()

#     if result is None:
#         raise HTTPException(status_code=404, detail="Director not found")

#     result.is_deleted = 'yes'
#     result.deleted_by = deleted_by
#     result.deleted_on = datetime.utcnow()

#     db.commit()

#     return {
#         "message": "Deleted successfully",
#     }

def delete_client_menu(db: Session, id: int, action: ActionType, deleted_by: int) -> tuple:
    result = db.query(ClientMainMenu).filter(ClientMainMenu.id == id).first()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Director not found")

    if action == ActionType.DELETE:
        result.is_deleted = 'yes'
        result.deleted_by = deleted_by
        result.deleted_on = datetime.utcnow()
        db.commit()
        return (True, "Deleted successfully")
    elif action == ActionType.UNDELETE:
      
        result.is_deleted = 'no'
      
        db.commit()
        return (True, "Undeleted successfully")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported action")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid action")
    

def get_client_menu_by_id(db: Session, id: int):
    return db.query(ClientMainMenu).filter(ClientMainMenu.id == id).first()  


def get_public_menu_data(db: Session):
    return db.query(PublicMainMenu).all()


def get_public_sub_menu_data(db: Session, main_menu_id: int):
    sql_query = text(
        "SELECT * FROM app_sub_menu WHERE main_menu_id = :main_menu_id "
    )
    return db.execute(sql_query, {"main_menu_id": main_menu_id}).fetchall()


def get_public_sub_sub_menu_data(db: Session, sub_menu_id: int):
    return db.query(PublicSubSubMenu).filter_by(sub_menu_id=sub_menu_id).all()  



def create_public_sub_menu(db: Session, main_menu_id: int, request: PublicSubMenuCreate, created_by: int):
    new_sub_menu = PublicSubMenu(
        main_menu_id=main_menu_id,  
        sub_menu=request.sub_menu,
        has_sub_menu=request.has_sub_menu,
        display_order=request.display_order,
        page_link=request.page_link,
        created_by=created_by  
    )
    db.add(new_sub_menu)
    db.commit()
    db.refresh(new_sub_menu)
    return new_sub_menu
   
    

def create_public_sub_sub_menu(db: Session, sub_menu_id: int, request: PublicSubSubMenuCreate, created_by: int):
    new_sub_sub_menu = PublicSubSubMenu(
        sub_menu_id=sub_menu_id,  
        sub_sub_menu=request.sub_sub_menu,
        display_order=request.display_order,
        page_link=request.page_link,
        created_by=created_by  
    )
    db.add(new_sub_sub_menu)
    db.commit()
    db.refresh(new_sub_sub_menu)
    return new_sub_sub_menu



def create_public_main_menu(db: Session, request: PublicMainMenuCreate, created_by: int):
    new_menu = PublicMainMenu(
        menu=request.menu,
        has_sub_menu=request.has_sub_menu,
        display_order=request.display_order,
        page_link=request.page_link,
        created_by=created_by  
    )
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu




