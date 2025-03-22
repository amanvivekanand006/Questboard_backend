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