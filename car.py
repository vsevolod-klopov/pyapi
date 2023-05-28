from pydantic import BaseModel
from sql_connector import connect


class AddCar(BaseModel):
    Brand : str
    Model : str
    Number : str
    Features : str
    VIN: str
    Mileage : int

class GetCar(BaseModel):
    Brand : str
    Model : str
    Number : str
    Features : str
    VIN: str
    Mileage : int
    id: str


def Push_Car_to_DB(Car: AddCar,id):
    try:
        wowtoDB = connect()
        mycursor = wowtoDB.cursor()
        mycursor.execute(
            f"INSERT INTO Car (Brand, Model, Number, VIN, Owner, Features, Mileage) VALUES ('{str(Car.Brand)}', '{str(Car.Model)}', '{str(Car.Number)}','{str(Car.VIN)}',{int(id)},'{str(Car.Features)}',{int(Car.Mileage)})")
        wowtoDB.commit()
        return True
    except:
        return False
    

def Update_Car_to_DB(Car: GetCar):
    try:
        wowtoDB = connect()
        mycursor = wowtoDB.cursor()
        mycursor.execute(
            f"UPDATE Service SET Brand = '{Car.Brand}', Model = '{Car.Model}', "
                   f"Number = '{Car.Number}', VIN = '{Car.VIN}', "
                   f"Features = {Car.Features}, Mileage = {Car.Mileage}WHERE id = {Car.id}")
        wowtoDB.commit()
        return True
    except:
        return False


def Check_Car_unic(Car: AddCar):
    wowtoDB = connect()
    mycursor = wowtoDB.cursor()
    mycursor.execute(
        f"SELECT * FROM Car WHERE VIN = {str(Car.VIN)}")
    myresult = mycursor.fetchall()
    if len(myresult)==0:
        return True
    else:
        return False