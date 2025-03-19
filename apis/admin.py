from . import *

client = MongoClient(mongo_uri)
db = client["questboard"]
admins_collection = db["admins"]
user_collection = db.usercollection

class admin(BaseModel):
    name : str
    email : str
    phone_number : int
    is_admin : bool
    admin_id : int

class user_registration(BaseModel):
    user_id : str
    username: str
    email: EmailStr
    profile_pic: str
    xp : int = Field(default = 0)
    coins : int
    level : int
    badges : List[str] = []

@api_router.post("/user_registration", operation_id="creating_user_account")
def create_user(userschema: user_registration):
    response = userschema.dict()
    result = user_collection.insert_one(response)  # result is an InsertOneResult
    user_id = str(result.inserted_id)  # Convert the inserted_id to a string
    return {"message": "User created successfully", "user_id": user_id}



