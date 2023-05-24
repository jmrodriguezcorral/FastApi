from fastapi import FastAPI
from routers import productos,usuarios
from fastapi.staticfiles import StaticFiles



app = FastAPI()
# El servidor ser inicia con el comando uvicorn main:app --reload

#Routers
app.include_router(productos.router)
app.include_router(usuarios.router)

#Contenido estatico
# Publica sobre http://localhost:8000/estatico_pub/imagenes/foto.jpg
app.mount("/estatico_pub",StaticFiles(directory="estatico"),name="estatico_nombre") 

#Operaciones
@app.get("/")
async def root():
    return "Hola!"





