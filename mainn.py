from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import os

app = FastAPI()

# 1. FIX CORS: Allows your frontend website to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Connect to MongoDB (Replace with your actual string or environment variable)
MONGO_URI = os.getenv("MONGO_URI", "your_mongodb_connection_string_here")
client = MongoClient(MONGO_URI)
db = client["my_database"]
collection = db["users"]

# 3. Define what the data should look like
class UserSchema(BaseModel):
    name: str
    age: int
    sex: str

# 4. Create the API Route that handles the form submission
@app.post("/submit")
def save_user(user: UserSchema):
    # Convert data to a dictionary format MongoDB expects
    user_data = user.dict()
    
    # Insert into the database
    result = collection.insert_one(user_data)
    
    # Send a success message back to the frontend
    return {"status": "success", "message": "User saved!", "id": str(result.inserted_id)}
