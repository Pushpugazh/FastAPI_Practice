from pydantic import BaseModel, Field
from typing import Optional, Literal


class UserSchema(BaseModel):
    userName : str = Field(..., description="Enter your user name")
    password : str = Field(..., description="Enter your password")
    dateOfBirth : Optional[str] = Field(None, description="Enter your data of birth")
    gender : Literal["male", "female"] = Field(None, description="Enter your gender")