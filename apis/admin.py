from . import *

class admin(BaseModel):
    name : str
    email : str
    phone_number : int
    is_admin : bool
    admin_id : int
