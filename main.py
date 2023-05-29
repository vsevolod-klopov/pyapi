from fastapi import FastAPI, Body, Depends, Request, HTTPException
from sql_connector import connect
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from Hasher import *
from User import UserLoginSchema, UserSignUp, Push_User_to_DB ,User_check_DB,User_credentials_check_DB
import car
from auth_bearer import JWTBearer
from auth_handler import signJWT , GetIdJWT
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)



def check_user_login(data):
    return User_credentials_check_DB(data)

def check_user_Reg(data):
    return User_check_DB(data)


@app.get("/")
async def read_items():
    html_content = """
    <html>
        <head>
            <title>WOWTO</title>
        </head>
        <body>
            <h1>Привет ты попапл на api сервер wowto.</h1>
            <a href="docs">api docs</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/db-status")
async def root():
    wowtoDB = connect()
    return {"message": f"{wowtoDB.is_connected()}"}


@app.get("/currentuser", dependencies=[Depends(JWTBearer())], tags=["get"])
async def current_user(request: Request):
    token = request.headers['authorization'].split(' ')[1]
    id = GetIdJWT(token)
    return {"id": f"{str(id)}"}

@app.get("/user/{id}", dependencies=[Depends(JWTBearer())], tags=["get"])
async def root(id):
    wowtoDB = connect()
    if wowtoDB.is_connected() == False:
        wowtoDB = connect()
    mycursor = wowtoDB.cursor()
    mycursor.execute(f"SELECT * FROM User WHERE id = '{id}' LIMIT 1")
    myresult = mycursor.fetchall()
    headers = [x[0] for x in mycursor.description]
    users = dict(zip(headers, myresult))
    json_compatible_item_data = jsonable_encoder(users)
    return JSONResponse(json_compatible_item_data)


@app.get("/users/",dependencies=[Depends(JWTBearer())], tags=["get"])
async def root():
    wowtoDB = connect()
    if wowtoDB.is_connected() == False:
        wowtoDB = connect()
    mycursor = wowtoDB.cursor()
    mycursor.execute(f"SELECT * FROM User")
    myresult = mycursor.fetchall()
    headers = [x[0] for x in mycursor.description]
    users = []
    for i in myresult:
        r = dict(zip(headers, i))
        users.append(r)
    json_compatible_item_data = jsonable_encoder(users)
    return JSONResponse(json_compatible_item_data)


@app.get("/services/",dependencies=[Depends(JWTBearer())], tags=["get"])
async def root():
    wowtoDB = connect()
    if wowtoDB.is_connected() == False:
        wowtoDB = connect()
    mycursor = wowtoDB.cursor()
    mycursor.execute(f"SELECT * FROM Service")
    myresult = mycursor.fetchall()
    headers = [x[0] for x in mycursor.description]
    users = []
    for i in myresult:
        r = dict(zip(headers, i))
        users.append(r)
    json_compatible_item_data = jsonable_encoder(users)
    return JSONResponse(json_compatible_item_data)


@app.post("/car/add/", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def AddCar(info: car.AddCar,request: Request):
    token = request.headers['authorization'].split(' ')[1]
    id = GetIdJWT(token)
    if car.Check_Car_unic(info):
        if car.Push_Car_to_DB(info,id):
            return {200:"success"}
        else:
            return {}
    else:
        return {
            "error": "Car already exists!"
        }


@app.put("/car/change/{id}", dependencies=[Depends(JWTBearer())], tags=["put"])
async def edit_service(id: int, data: car.AddCar):
    try:
        result = car.Update_Car_to_DB(data)
        json_compatible_item_data = jsonable_encoder(result)
        return JSONResponse(json_compatible_item_data)
    except HTTPException:
        HTTPException(status_code=409, detail="Error editing service")


@app.post("/user/login", tags=["login"])
async def login(user: UserLoginSchema = Body(...)):
    if check_user_login(user):
        return signJWT(user.Phone)
    else:
        return {
            "error": "Wrong login details!"
        }

@app.post("/user/signup", tags=["login"])
async def signup(user: UserSignUp):
    if not check_user_Reg(user):
        Push_User_to_DB(user)
        return signJWT(user.Phone)
    return{
            "error": "User already exists!"
        }