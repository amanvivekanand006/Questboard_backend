from . import *

client = MongoClient(mongo_uri)
db = client["questboard"]
admins_collection = db["admins"]

class admin(BaseModel):
    name : str
    email : str
    phone_number : int
    is_admin : bool
    admin_id : int
