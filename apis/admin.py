from . import *


client = MongoClient(mongo_uri)
db = client["questboard"]
admins_collection = db["admins"]
user_collection = db.usercollection

class adminbase(BaseModel):
    name : str
    email : str
    phone_number : int
    is_admin : bool
    

class createadmin(adminbase):
    pass

class admin(adminbase):
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

@api_router.post("/create_admin")
async def create_admin(admin: createadmin):
    admin_dict = admin.dict() 
    admin_dict["admin_id"] = str(uuid.uuid4())

    result = admins_collection.insert_one(admin_dict)
    if result.inserted_id:
       admin_dict.pop("_id", None)
       return admin_dict
    raise HTTPException(status_code=500, detail="Failed to create admin")


@api_router.get("/get_admin")
async def get_admin(admin_id : str):
    Admin = admins_collection.find_one({"admin_id": admin_id})
    if not Admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    Admin.pop("_id", None)
    return Admin

@api_router.put("/update_admin")
async def update_admin(admin_id: str, admin : createadmin):
    updated_admin = admin.dict()
    result = admins_collection.update_one({"admin_id":admin_id},{"$set":updated_admin})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    updated_admin["admin_id"] = admin_id
    return updated_admin

@api_router.delete("/delete_admin")
async def delete_admin(admin_id:str):
    result= admins_collection.delete_one({"admin_id":admin_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"message":"admin deleted successfully"}
    
