from . import *


client = MongoClient(mongo_uri)
db = client["questboard"]
user_collection = db.usercollection

def generate_user_id():
    id = f"UID{random.randint(10000000,99999999)}"
    return id

class user_registration(BaseModel):
    username: str
    email: EmailStr
    profile_pic: str
    xp : int = Field(default = 0)
    coins : int
    level : int
    badges : List[str] = []
    following : List[str] = []
    followers : List[str] = []


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

@api_router.post("/Following_user",operation_id="following user", tags=["Users"])
def send_follow_request(user_id:str=Query(...,), following_id:str=Query(...,)):
    check_user_id = user_collection.find_one({"user_id":user_id})
    check_following_id = user_collection.find_one({"user_id":following_id})
    check_if_follower = user_collection.find_one({"following": {"$in": [following_id]}})

    if not check_user_id:
        raise HTTPException(status_code=404, detail=f"User Not Found!")
    if not check_following_id:
        raise HTTPException(status_code=404, detail=f"following User Not Found!")
    if check_user_id == check_following_id:
        raise HTTPException(status_code=404, detail=f"User Cannot follow its own account!")
    if check_if_follower:
        raise HTTPException(status_code=404, detail=f"you already follow {following_id}!")
    
    document1 = user_collection.find_one_and_update({"user_id":user_id},{"$push":{"following":following_id}})
    document2 = user_collection.find_one_and_update({"user_id":following_id},{"$push":{"followers":user_id}})
    
    if document1:
       return {"message": f"User {user_id} now follows {following_id}"}
    # if document2:
    #     return{"message" : f"{user_id} Started following you!"}


@api_router.post("/Unfollowing_user",operation_id="unfollowing user", tags=["Users"])
def unfollowing_user(user_id:str=Query(...,), unfollowing_id:str=Query(...,)):
    check_user_id = user_collection.find_one({"user_id":user_id})
    check_unfollowing_id = user_collection.find_one({"user_id":unfollowing_id})
    check_if_follower = user_collection.find_one({"following": {"$in": [unfollowing_id]}})


    if not check_user_id:
        raise HTTPException(status_code=404, detail=f"User Not Found!")
    if not check_unfollowing_id:
        raise HTTPException(status_code=404, detail=f"Unfollowing User Not Found!")
    if check_user_id == check_unfollowing_id:
        raise HTTPException(status_code=404, detail=f"User Cannot Unfollow its own account!")
    if not check_if_follower:
        raise HTTPException(status_code=404, detail=f"you dont follow this User!")

    document1 = user_collection.find_one_and_update({"user_id":user_id},{"$pull":{"following":unfollowing_id}})
    document2 = user_collection.find_one_and_update({"user_id":unfollowing_id},{"$pull":{"followers":user_id}})

    if document1:
       return {"message": f"User {user_id} now Unfollows {unfollowing_id}"}
    # if document2:
    #     return{"message" : f"{user_id} Stoped following you!"}

@api_router.get("/get_user_followers_list", operation_id="getting_all_user_followers_list", tags=["Users"])
def get_user_followers(user_id:str=Query(...,)):
    check_user_id = user_collection.find_one({"user_id":user_id})
    
    if not check_user_id:
        raise HTTPException(status_code=404, detail=f"User Not Found")
    else:
        document = user_collection.find_one({"user_id":user_id})
        return {
             "followers": document.get("followers", [])
        }
             
@api_router.get("/get_user_following_list", operation_id="getting_all_user_following_list", tags=["Users"])
def get_user_followings(user_id:str=Query(...,)):
    check_user_id = user_collection.find_one({"user_id":user_id})
    
    if not check_user_id:
        raise HTTPException(status_code=404, detail=f"User Not Found")
    else:
        document = user_collection.find_one({"user_id":user_id})
        return {
             "followers": document.get("following", [])
        }
             
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

