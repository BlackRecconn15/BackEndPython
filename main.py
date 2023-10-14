

from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles

#? Run server: --> python -m uvicorn main:app --reload


app = FastAPI()

#* Routers
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static") #Asi se "exponen" las imagenes



@app.get("/")
async def root():
    return {"message" : "Hola Mundo!!"}

@app.get("/url")
async def url():
    return {"url" : "http://josuemorales.dev"}


#? Documentacion con Swagger: http://127.0.0.1:8000/docs
#? Documentacion con Redocly: http://127.0.0.1:8000/redoc