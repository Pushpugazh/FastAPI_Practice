from http.client import HTTPException

from fastapi import FastAPI, HTTPException
from schema import UserSchema
from database import db

from utils import serialize_doc

app = FastAPI()

users_collection = db["users"]


@app.get("/home")
def home():
    return {
        "message" : "The API is working!..."
    }


@app.post("/sign-up")
def register(user: UserSchema):
    user_data = user.model_dump()

    user_info = users_collection.find_one({"userName": user.userName})

    if user_info:
        return {
            "message": "Username already exists"
        }

    users_collection.insert_one(user_data)
    return {
        "message": "User sign up successful"
    }



@app.get("/get-all-users")
def user_list():
    users = list(users_collection.find())
    return [serialize_doc(user) for user in users]


@app.post("/log-in")
def log_in(user: UserSchema):
    user_doc = users_collection.find_one({"userName": user.userName})
    pass_match = {
        0 : "Invalid Credentials",
        1 : "Login Successful"
    }

    if not user_doc:
        raise HTTPException(status_code=404, detail=f"user {user.userName} not found")

    match = 1 if user_doc['password'] == user.password else 0

    return {
        "message": pass_match[match],
        "userName": user.userName if match else None
    }


@app.delete("/delete-users")
def delete_users(userName: str):
    if userName.lower() == "all":
        users_collection.delete_many({})
        message = "All Users deleted Successfully"
    else:
        users_collection.delete_one({"userName": userName})
        message = f"User : {userName} deleted Successfully"
    return {
        "message": message
    }

