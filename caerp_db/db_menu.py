from fastapi import HTTPException,status
from caerp_db.models import AdminMainMenu, AdminMainMenuPermission, AdminSubMenu,AdminSubMenuPermission, ClientMainMenu, PublicMainMenu, PublicSubMenu, PublicSubSubMenu, SiteLegalAboutUs
from caerp_schemas import AdminMainMenuCreate, AdminMainMenuDeleteSchema, AdminSubMenuCreate, AdminSubMenuDeleteSchema, ClientMenuBase, PublicSubMenuCreate, PublicSubSubMenuCreate
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


def create_admin_main_menu(db: Session, request: AdminMainMenuCreate, created_by: int):
    new_menu = AdminMainMenu(
        main_menu=request.main_menu,
        main_menu_has_sub_menu=request.main_menu_has_sub_menu,
        main_menu_display_order=request.main_menu_display_order,
        main_menu_page_link=request.main_menu_page_link,
        created_by=created_by  
    )
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu
    






def update_admin_main_menu(db: Session, id: int, role_input: AdminMainMenuCreate, modified_by: int):
    update_admin_main_menu = db.query(AdminMainMenu).filter(AdminMainMenu.main_menu_id == id).first()

    if update_admin_main_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    for field, value in role_input.dict(exclude_unset=True).items():
        setattr(update_admin_main_menu, field, value)

    # Set modified_by and modified_on outside the loop
    update_admin_main_menu.modified_by = modified_by
    update_admin_main_menu.modified_on = datetime.utcnow()

    db.commit()
    db.refresh(update_admin_main_menu)

    return update_admin_main_menu




 
def delete_admin_main_menu(db: Session, id: int, role_input: AdminMainMenuDeleteSchema, deleted_by: int):
    deleted_admin_main_menu = db.query(AdminMainMenu).filter(AdminMainMenu.main_menu_id == id).first()
    if deleted_admin_main_menu is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    deleted_admin_main_menu.is_deleted = 'yes'
    deleted_admin_main_menu.deleted_by = deleted_by
    deleted_admin_main_menu.deleted_on = datetime.utcnow()
    db.commit()
    return {
        "message": "Menu item marked as deleted successfully",
        "deleted_by": deleted_by,
        "deleted_on": deleted_admin_main_menu.deleted_on
    }
   




def create_admin_sub_menu(db: Session, main_menu_id: int, request: AdminSubMenuCreate, created_by: int):
    new_sub_menu = AdminSubMenu(
        main_menu_id=main_menu_id,  
        sub_menu=request.sub_menu,
        sub_menu_has_sub_menu=request.sub_menu_has_sub_menu,
        sub_menu_display_order=request.sub_menu_display_order,
        sub_menu_page_link=request.sub_menu_page_link,
        created_by=created_by  
    )
    db.add(new_sub_menu)
    db.commit()
    db.refresh(new_sub_menu)
    return new_sub_menu






def update_admin_sub_menu(id: int, db: Session, main_menu_id: int, role_input: AdminSubMenuCreate, modified_by: int):
    update_admin_sub_menu = db.query(AdminSubMenu).filter(AdminSubMenu.sub_menu_id == id).first()
    print(update_admin_sub_menu)

    if update_admin_sub_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    for field, value in role_input.dict(exclude_unset=True).items():
        setattr(update_admin_sub_menu, field, value)

    update_admin_sub_menu.modified_by = modified_by
    update_admin_sub_menu.main_menu_id = main_menu_id
    update_admin_sub_menu.modified_on = datetime.utcnow()
    
    db.commit()
    db.refresh(update_admin_sub_menu)

    return update_admin_sub_menu




    
def delete_admin_sub_menu(db: Session, id: int, role_input: AdminSubMenuDeleteSchema, deleted_by: int):
    deleted_admin_sub_menu = db.query(AdminSubMenu).filter(AdminSubMenu.sub_menu_id == id).first()
    if deleted_admin_sub_menu is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    deleted_admin_sub_menu.is_deleted = 'yes'
    deleted_admin_sub_menu.deleted_by = deleted_by
    deleted_admin_sub_menu.deleted_on = datetime.utcnow()
    db.commit()
    return {
        "message": "Deleted successfully",
        "deleted_by": deleted_by,
        "deleted_on": deleted_admin_sub_menu.deleted_on
    }
    
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


    

def delete_client_menu(db: Session, id: int, deleted_by: int):
    result = db.query(ClientMainMenu).filter(ClientMainMenu.id == id).first()

    if result is None:
        raise HTTPException(status_code=404, detail="Director not found")

    result.is_deleted = 'yes'
    result.deleted_by = deleted_by
    result.deleted_on = datetime.utcnow()

    db.commit()

    return {
        "message": "Deleted successfully",
    }

    

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





