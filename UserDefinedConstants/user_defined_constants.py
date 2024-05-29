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
    
class ProductConstatnt(str,Enum):
    PRODUCTID       ='product_id'
    PRODUCTCODE     = 'product_code'
    
 

class RecordActionType(str,Enum):
     UPDATE_ONLY        = 'UPDATE_ONLY'
     INSERT_ONLY        = 'INSERT_ONLY'
     UPDATE_AND_INSERT  = 'UPDATE_AND_INSERT'
     DELETE             = 'DELETE'
     UNDELETE           = 'UNDELETE'

class Operator(str,Enum):
    EQUAL_TO    = 'EQUAL_TO'
    # NOT_EQUAL_TO = 'NOT_EQUAL_TO'
    GREATER_THAN = 'GREATER_THAN'
    LESS_THAN  = 'LESS_THAN'

class ApplyTo(str,Enum):
    ALL         =   'ALL'
    SELECTED    =   'SELECTED'


class Status(str,Enum):
    CURRENT     = "CURRENT"
    UPCOMMING   = "UPCOMMING"
    EXPIRED     = "EXPIRED"