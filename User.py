from pydantic import BaseModel, Field, EmailStr
from Hasher import get_password_hash
from sql_connector import connect

class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "Securing FastAPI applications with JWT.",
                "content": "In this tutorial, you'll learn how to secure your application by enabling authentication using JWT. We'll be using PyJWT to sign, encode and decode JWT tokens...."
            }
        }


class UserSignUp(BaseModel):
    Name: str = Field(...)
    Phone: str = Field(...)
    Password: str = Field(...)
    Role: int 

    class Config:
        schema_extra = {
            "example": {
                "Name": "Joe Doe",
                "Phone": "89090692828",
                "Password": "941941",
                "Role":1
            }
        }

class UserLoginSchema(BaseModel):
    Phone: str = Field(...)
    Password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "Phone": "89090692828",
                "Password": "941941"
            }
        }

def Push_User_to_DB(user: UserSignUp):
    wowtoDB = connect()
    mycursor = wowtoDB.cursor()
    mycursor.execute(
        f"INSERT INTO User (Name, Phone, Password, Role) VALUES ('{str(user.Name)}', '{str(user.Phone)}', '{str(get_password_hash(user.Password))}',{int(user.Role)})")
    wowtoDB.commit()


def User_credentials_check_DB(data):
    wowtoDB = connect()
    mycursor = wowtoDB.cursor()
    mycursor.execute(f"SELECT * FROM User WHERE phone = '{str(data.Phone)}' AND Password = '{str(get_password_hash(data.Password))}'")
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        return True
    return False

def User_check_DB(data):
    wowtoDB = connect()
    mycursor = wowtoDB.cursor()
    mycursor.execute(f"SELECT * FROM User WHERE phone = '{str(data.Phone)}'")
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        return True
    return False