from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import os

# Initialize FastAPI application
app = FastAPI()

# 1. ALLOW FRONTEND TO CONNECT (CORS Settings)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. CONNECT TO MONGODB DATABASE
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://pingtosani_db_user:LoUPLWvwNi2wNSQO@sanidb.nq0r9f4.mongodb.net")
client = MongoClient(MONGO_URI)
db = client["my_database"]
collection = db["users"]

# 3. DEFINE THE DATA STRUCTURE
class UserSchema(BaseModel):
    name: str
    age: int
    sex: str

# 4. HOME ROUTE
@app.get("/")
def home():
    return {"status": "online", "message": "Python backend is running successfully!"}

# 5. DIAGNOSTIC ROUTE TO CHECK MONGODB LINK
@app.get("/test-db")
def test_db():
    try:
        client.admin.command('ping')
        return {"status": "success", "database_connected": True}
    except Exception as e:
        return {"status": "error", "database_connected": False, "details": str(e)}

# 6. SUBMIT FORM DATA ROUTE (The missing link!)
@app.post("/submit")
def save_user(user: UserSchema):
    try:
        user_data = user.dict()
        result = collection.insert_one(user_data)
        return {
            "status": "success", 
            "message": f"Successfully saved {user.name} to the database!", 
            "id": str(result.inserted_id)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
