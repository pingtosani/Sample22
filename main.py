from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import os

# Initialize FastAPI application
app = FastAPI()

# 1. ALLOW FRONTEND TO CONNECT (CORS Settings)
# This allows your Vercel frontend website to communicate with this backend securely.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you can replace "*" with your actual Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. CONNECT TO MONGODB DATABASE
# Render will pull your actual database string safely from the Environment Variables.
# If it can't find one, it will look for the fallback string provided below.
MONGO_URI = os.getenv("MONGO_URI", "your_mongodb_connection_string_here")
client = MongoClient(MONGO_URI)
db = client["my_database"]
collection = db["users"]

# 3. DEFINE THE DATA STRUCTURE
# This tells Python exactly what data properties to expect from the form.
class UserSchema(BaseModel):
    name: str
    age: int
    sex: str

# 4. HOME ROUTE
# Added a home route so you can easily check if your server is online in a web browser.
@app.get("/")
def home():
    return {"status": "online", "message": "Python backend is running successfully!"}

# 5. SUBMIT FORM DATA ROUTE
# This receives the data payload from the frontend and pushes it directly to MongoDB.
@app.post("/submit")
def save_user(user: UserSchema):
    try:
        # Convert incoming data into standard Python dictionary format
        user_data = user.dict()
        
        # Insert the document into your MongoDB collection
        result = collection.insert_one(user_data)
        
        # Send a clean success response back to the user's browser
        return {
            "status": "success", 
            "message": f"Successfully saved {user.name} to the database!", 
            "id": str(result.inserted_id)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
