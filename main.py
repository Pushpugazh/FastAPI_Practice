from http.client import HTTPException

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from schema import UserSchema
from database import db
from utils import serialize_doc, hash_password, verify_password, create_access_token, get_current_user

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

    if users_collection.find_one({"userName": user.userName}):
        raise HTTPException(status_code=400, detail="Username already exists")

    user_data["password"] = hash_password(user.password)
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

    if not user_doc:
        raise HTTPException(status_code=404, detail="user not found")

    if not verify_password(user.password, user_doc["password"]):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    token = create_access_token(user.model_dump(), 30)
    return {
        "message": "User Login successful",
        "token" : token
    }


@app.delete("/delete-users")
def delete_users(
        userName: str,
        current_user: dict = Depends(get_current_user)
    ):
    if userName.lower() == "all":
        users_collection.delete_many({})
        message = "All Users deleted Successfully"
    else:
        users_collection.delete_one({"userName": userName})
        message = f"User : {userName} deleted Successfully by {current_user}"
    return {
        "message": message
    }

