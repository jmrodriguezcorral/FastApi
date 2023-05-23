from fastapi import FastAPI
from routers import productos,usuarios



app = FastAPI()
# El servidor ser inicia con el comando uvicorn main:app --reload

#Routers
app.include_router(productos.router)
app.include_router(usuarios.router)

#Operaciones
@app.get("/")
async def root():
    return "Hola!"





