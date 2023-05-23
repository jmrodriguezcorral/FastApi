from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["Usuarios"])
# El servidor ser inicia con el comando uvicorn main:app --reload

class User(BaseModel):
    id: int
    nombre: str
    apellido: str
    correo: str
    edad: int

# Lista de usuarios por defecto
lista_usuarios = [User(id=1,nombre="Pedro",apellido="Garcia",correo="pedro_garcia@gmail.com",edad=43),
             User(id=2,nombre="Ana",apellido="Perez",correo="ana_perez@hotmail.com",edad=32),
             User(id=3,nombre="Prueba",apellido="Prueba",correo="prueba@hotmail.com",edad=32)]

#listas los usuarios
@router.get("/usuarios")
async def usuarios():
    return lista_usuarios 

@router.get("/usuario/{id}") #Acceso por path
async def usuario(id: int):
    return buscarUsuario(id)

@router.get("/usuario/") #Acceso por query
async def usuario(id: int):
    return buscarUsuario(id)

#Prueba de POST. Crear nuevo usuario
@router.post("/usuario/",response_model=User,status_code=201)
async def usuario(usu:User):
    if type(buscarUsuario(usu.id)) == User:
        raise HTTPException(status_code=404,detail="El usuario ya existe")
        return {"error":"el usuario ya existe"}
    else:
        lista_usuarios.append(usu)
        return usu

# Prueba de PUT. Actualizar los valores de un usuario
@router.put("/usuario/")
async def usuario(usu:User):
    esta = False
    for i,usuario in enumerate(lista_usuarios):
        if usuario.id == usu.id:
            lista_usuarios[i] = usu
            esta=True
    
    if not esta:
        return {"error":"No se ha actualizado"}
    else:
        return usu

#Prueba de DELETE. Se borra un usuario de la lista
@router.delete("/usuario/{id}") #Acceso por path
async def usuario(id: int):
    esta=False
    for i,usuario in enumerate(lista_usuarios):
        if usuario.id == id:
            del lista_usuarios[i]
            esta=True
    
    if not esta:
        return {"error":"No se ha borra. No estaba"}



# Funciones de negocio
def buscarUsuario(id: int):
    # Se usa una lamdda --> lambda x: x.n [operador] n, lista_x --> devuelve una lista_x
    usuarios = filter(lambda usuario: usuario.id == id, lista_usuarios)
    try:
        return list(usuarios)[0]
    except:
        return {"error":"elemento no encontrado"}



