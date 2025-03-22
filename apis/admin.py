from . import *


client = MongoClient(mongo_uri)
db = client["questboard"]
admins_collection = db["admins"]

def generate_admin_id():
    id = f"AID{random.randint(10000000,99999999)}"
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

@api_router.post("/create_admin", operation_id="creating_admin_for_application" , tags=["Admin"])
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


@api_router.get("/get_admin", operation_id="get_admins" ,tags=["Admin"])
async def get_admin(admin_id : str):
    Admin = admins_collection.find_one({"admin_id": admin_id})
    if not Admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    Admin.pop("_id", None)
    return Admin

@api_router.put("/update_admin", operation_id="updating_admins", tags=["Admin"])
async def update_admin(admin_id: str, admin : createadmin):
    updated_admin = admin.dict()
    result = admins_collection.update_one({"admin_id":admin_id},{"$set":updated_admin})
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    updated_admin["admin_id"] = admin_id
    return updated_admin

@api_router.delete("/delete_admin", operation_id="deleting_admins" ,tags=["Admin"])
async def delete_admin(admin_id:str):
    result= admins_collection.delete_one({"admin_id":admin_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"message":"admin deleted successfully"}

# @api_router.get("/fetch_users")
# async def fetch_users():
#     users = list(user_collection.find())
#     for user in users:
#         user.pop("_id")
#     return users
