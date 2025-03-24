from . import *


client = MongoClient(mongo_uri)
db = client["questboard"]
admins_collection = db["admins"]
user_collection = db.usercollection

def generate_admin_id():
    id = f"AID{random.randint(10000000,99999999)}"
    return id
def generate_user_id():
    id = f"UID{random.randint(10000000,99999999)}"
    return id

class adminbase(BaseModel):
    name : str
    email : str
    phone_number : int
    is_admin : bool
    

class createadmin(adminbase):
    pass

class admin(adminbase):
    admin_id : str = Field(default_factory=generate_admin_id)

class user_registration(BaseModel):
    username: str
    email: EmailStr
    profile_pic: str
    xp : int = Field(default = 0)
    coins : int
    level : int
    badges : List[str] = []



@api_router.post("/user_registration", operation_id="creating_user_account", tags=["Admin and Users"])
def create_user(userschema: user_registration):
    response = userschema.dict()
    generated_user_id = generate_user_id()
    response.update({
        "user_id": generated_user_id
    })
    
    # Check if user exists with email
    existing_user = user_collection.find_one({"email": response['email']})
    
    if existing_user:
        # Convert existing user document to dictionary
        complete_user_details = dict(existing_user)
        complete_user_details['_id'] = str(complete_user_details['_id'])
        
        # Return both minimal and complete user details
        return {
            "message": "User already exists",
            "user_details": {
                "user_id": existing_user["user_id"]
            },
            "complete_user_details": complete_user_details
        }
    else:
        result = user_collection.insert_one(response)
        inserted_id = str(result.inserted_id)
        return {
            "message": "User created successfully",
            "user_id": generated_user_id
        }
@api_router.post("/create_admin", operation_id="creating_admin_for_application" , tags=["Admin and Users"])
async def create_admin(admin: createadmin):
    admin_dict = admin.dict() 
    generated_admin_id = generate_admin_id()
    admin_dict.update({
        "admin_id" : generated_admin_id
    })

    result = admins_collection.insert_one(admin_dict)
    if result.inserted_id:
       admin_dict.pop("_id", None)
       return admin_dict
    raise HTTPException(status_code=500, detail="Failed to create admin")


@api_router.get("/get_admin", operation_id="get_admins" ,tags=["Admin and Users"])
async def get_admin(admin_id : str):
    Admin = admins_collection.find_one({"admin_id": admin_id})
    if not Admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    Admin.pop("_id", None)
    return Admin

@api_router.put("/update_admin", operation_id="updating_admins", tags=["Admin and Users"])
async def update_admin(admin_id: str, admin : createadmin):
    updated_admin = admin.dict()
    result = admins_collection.update_one({"admin_id":admin_id},{"$set":updated_admin})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    updated_admin["admin_id"] = admin_id
    return updated_admin

@api_router.delete("/delete_admin", operation_id="deleting_admins" ,tags=["Admin and Users"])
async def delete_admin(admin_id:str):
    result= admins_collection.delete_one({"admin_id":admin_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"message":"admin deleted successfully"}

@api_router.get("/fetch_users")
async def fetch_users():
    users = list(user_collection.find())
    for user in users:
        user.pop("_id")
    return users


@api_router.get("/user_details")
async def fetch_user(user_id: str):
    User = user_collection.find_one({"user_id":user_id})
    if not User:
        raise HTTPException(status_code=404, detail="User not found")
    else:
       User.pop("_id", None)
    
       return User