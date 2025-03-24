from . import *

client = MongoClient(mongo_uri)
db = client["questboard"]
quest_collection = db.Quest_collection


class Quest_schema(BaseModel):
    title : str
    description : str
    coins : int
    xp : int 
    creation_date : datetime = datetime.now()
    boost_score : int = Field(default=0)

def get_ups(quest):
    return quest["Ups"]

def generate_quest_id():
    id = f"QUID{random.randint(10000000,99999999)}"
    return id

@api_router.post("/create_quests", operation_id="posting_quests_from user", tags=["Quests"])
def posting_quest(questschema:Quest_schema,created_by :str=Query(...,), status: str = Query(...,enum= ["Open","Accepted","Completed"])):
    quest_id = generate_quest_id()
    document = questschema.dict()
    document.update({
        "quest_id": quest_id,
        "status" : status,
        "created_by" : created_by
    })

    response = quest_collection.insert_one(document)
    inserted_id = str(response.inserted_id)
    inserted_document = quest_collection.find_one({"_id": response.inserted_id})
    return {
        "quest_id": quest_id,
        "title": inserted_document["title"],
        "description": inserted_document["description"],
        "coins" : inserted_document["coins"],
        "xp" : inserted_document["xp"],
        "creation_date": inserted_document["creation_date"],
        "boost_score" : inserted_document["boost_score"],
        "status" : inserted_document["status"],
        "created_by" : inserted_document["created_by"],
    }


@api_router.post("/likes_quest")
async def quest_action(quest_id:str, user_id:str, action: str):
    if action not in ["up","down"]:
       raise HTTPException(status_code=400, detail="Action must be 'up' or 'down'")
    Quest = quest_collection.find_one({'quest_id':quest_id})
    if not Quest:
        raise HTTPException(status_code=400,detail="NO Quest")
    if "Ups" not in Quest:
        quest_collection.update_one(
            {"quest_id": quest_id},
            {"$set": {"Ups": 0, "liked_by": []}}
        )
        # Refresh quest after initialization
        Quest = quest_collection.find_one({"quest_id": quest_id})

    if action == "up":
        if "liked_by" in Quest and user_id in Quest["liked_by"]:
            raise HTTPException(status_code=400, detail="You have already upped this quest")
        
        update_data = {
            "$inc": {"Ups": 1},  # Increment Ups by 1
            "$addToSet": {"liked_by": user_id},  # Add user_id to liked_by array
            "$set": {"last_updated": datetime.utcnow()}
        }
        message = "Quest upped successfully"       
    # Handle the "down" action (unlike)
    elif action == "down":
        if "Ups" not in Quest or Quest["Ups"] == 0:
            raise HTTPException(status_code=400, detail="This quest has no ups to remove")
        if "liked_by" not in Quest or user_id not in Quest["liked_by"]:
            raise HTTPException(status_code=400, detail="You haven't upped this quest yet")
        
        update_data = {
            "$inc": {"Ups": -1},  # Decrement Ups by 1
            "$pull": {"liked_by": user_id},  # Remove user_id from liked_by array
            "$set": {"last_updated": datetime.utcnow()}
        }
        message = "Quest un-upped successfully"

    # Perform the update
    result = quest_collection.update_one(
        {"quest_id": quest_id},
        update_data
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update quest")

    # Fetch updated quest details
    updated_quest = quest_collection.find_one({"quest_id": quest_id})
    updated_quest.pop("_id")

    return {
        "message": message,
        "quest_id": quest_id,
        "Ups": updated_quest["Ups"],
        "liked_by": updated_quest.get("liked_by", [])
    }

@api_router.get("/fetch_trendingquests")
async def trending_quests():
    trending = list(quest_collection.find())
    for Quest in trending:
       Quest.pop("_id")
       if "Ups" not in Quest:
            Quest["Ups"] = 0
           
    trending.sort(key=get_ups, reverse=True)

    return {
        "message": "Trending quests fetched successfully",
        "trending_quests": trending
    }



