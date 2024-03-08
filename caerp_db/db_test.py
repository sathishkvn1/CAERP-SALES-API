from fastapi import HTTPException
from carp_db.models import AdminMainMenuPermission, AdminSubMenuPermission

from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import and_
from datetime import datetime




def get_menu_data_by_role_and_permission(db: Session, role_id: int, main_menu_permission: str):
    return db.query(AdminMainMenuPermission).filter(
        and_(
            AdminMainMenuPermission.main_menu_permission_role_id == role_id,
            AdminMainMenuPermission.main_menu_permission_is_granted  == main_menu_permission
        )
    ).all()



