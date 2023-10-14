from fastapi import HTTPException, APIRouter
from pydantic import BaseModel


router = APIRouter(tags=["users"], 
                   responses={404: {"message": "No encontrado"}})

#? Recuerda estar dentro de la carpeta
#? run server: --> python -m uvicorn users:app --reload

#*Entidad User

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1, name="Josue", surname="Morales", url="https://moracam.dev", age=24),
                User(id=2, name="Jose", surname="Moral", url="https://moracam2.dev", age=22),
                User(id=3, name="Alan", surname="Morales", url="https://moralong.dev", age=25)]

@router.get("/usersjson")
async def usersjson(): #Creamos un JSON a mano
    return [{"name" : "Josue", "surname": "Morales", "url": "https://moracam.dev", "age": 24},
            {"name" : "Jose", "surname": "Moral", "url": "https://moracam2.dev", "age": 22},
            {"name" : "Alan", "surname": "Morales", "url": "https://moralong.dev", "age": 25}]

@router.get("/users")
async def users():
    return users_list

#Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    
#query
@router.get("/user/")
async def user(id: int):
    return search_user(id)

@router.post("/user/",response_model= User ,status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code= 204, detail= "El usuario ya existe")
    
    users_list.append(user)
    return {"message": "El usuario se agrego"}  

@router.put("/user/")
async def user(user : User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            return {"message": "El Usuario se ah actualizado"}

    if not found:
        return {"error": "No se ah encontrado el usuario"}
    
@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return {"message": "El Usuario se a Eliminado correctamente"}

    if not found:
        return {"error": "No se ah eliminado el usuario"}


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try :
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
    
