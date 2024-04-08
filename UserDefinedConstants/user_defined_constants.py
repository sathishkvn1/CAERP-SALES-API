from enum import Enum

class DeletedStatus(str, Enum):
    ALL = "all"
    DELETED = "yes"
    NOT_DELETED = "no"
    
    
class ActiveStatus(str,Enum):
    ALL         = 'all'
    ACTIVE      = 'yes'
    NOT_ACTIVE  ='no'

class ParameterConstant(str,Enum):
    STATE       ='state_id'
    TALUK       ='taluk_id'
    DISTRICT    = 'district_id'
    COUNTRY     = 'country_id'
    POST_OFFICE = 'post_office_id'
    TYPE        = 'customer_type_id' 
    
class BooleanFlag(str, Enum):
    yes = "yes"
    no = "no"
    
class ActionType(str, Enum):
    DELETE = 'DELETE'
    UNDELETE = 'UNDELETE'
    

    
