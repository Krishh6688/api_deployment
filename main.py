from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
# with the help of client we can access database and collections
db = client["mktrainings"]
gk_data = db["mk_collection"]

# create object of FastAPI
app = FastAPI()

# for data validataion purpose use pydantic model class
class gkdata(BaseModel):
    name: str
    phone: int
    city: str
    course: str
    
@app.post("/gktrainings/insert")    
async def gk_data_insert_helper(data:gkdata):
    result  = await gk_data.insert_one(data.model_dump())
    return str(result.inserted_id)

    
def gk_helper(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

@app.get("/gktrainings/get_all_data")
async def get_gk_all_data():
    items = []
    cursor = gk_data.find({})
    async for document in cursor:
        items.append(gk_helper(document))
    return items

@app.get("/gktrainings/show_data")
async def show_gk_all_data():
    items = []
    cursor = gk_data.find({})
    async for document in cursor:
        items.append(gk_helper(document))
    return items


@app.get("/gktrainings/showcollections")
async def get_all_collections():
    collection_names = await db.list_collection_names()
    return {"collections": collection_names}

from bson import ObjectId

@app.get("/gktrainings/getdata/{id}")
async def get_gk_data_id(id: str):
    document = await gk_data.find_one({"_id": ObjectId(id)})
    
    if not document:
        return {"message": "Record not found"}
    
    return gk_helper(document)


@app.get("/gktrainings/getname/{name}")
async def get_gk_data_name(name: str):
    document = await gk_data.find_one({"name": name})
    
    if not document:
        return {"message": "Record not found"}
    
    return gk_helper(document)