from fastapi import APIRouter, HTTPException,status
from bd.modelos.usuario import User
from bd.schema.usuario import usuario_schema, usuarios_schema
from bd.cliente import db_cliente
# Usamos esto para poder leer el id de los objetos de mongodb
from bson import ObjectId

router = APIRouter(prefix="/usu_db",
                   tags=["usuario BD"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})


#listas los usuarios
@router.get("/", response_model=list[User])
async def usuarios():
    return usuarios_schema(db_cliente.local.usuarios.find()) 

@router.get("/{id}") #Acceso por path
async def usuario(id: str):
    return buscarUsuario("_id",ObjectId(id))

@router.get("/query/") #Acceso por query
async def usuario(id: str):
    print("hola")
    return buscarUsuario("_id",ObjectId(id))

@router.post("/",response_model=User,status_code=status.HTTP_201_CREATED)
async def usuario(usu:User):
    if type(buscarUsuario_correo(usu.correo)) == User:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="El usuario ya existe")

    usu_dic = dict(usu)
    del usu_dic["id"]
    id = db_cliente.local.usuarios.insert_one(usu_dic).inserted_id
    usu_nuevo = usuario_schema(db_cliente.local.usuarios.find_one({"_id":id}))
    return User(**usu_nuevo)

# Prueba de PUT. Actualizar los valores de un usuario
@router.put("/",response_model=User)
async def usuario(usu:User):
    # Cargamos el usuario en un diccionario y el borramos el ID
    usu_dict = dict(usu)
    del usu_dict["id"]
    try:
        db_cliente.local.usuarios.find_one_and_replace(
            {"_id": ObjectId(usu.id)}, 
            usu_dict)
    except:
        return {"error":"No se ha actualizado"}
    return buscarUsuario("_id", ObjectId(usu.id))


#Prueba de DELETE. Se borra un usuario de la lista
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) #Acceso por path
async def usuario(id: str):
    esta = db_cliente.local.usuarios.find_one_and_delete({"_id": ObjectId(id)})
    
    if not esta:
        return {"error":"No se ha borra. No estaba"}



# Funciones de negocio
def buscarUsuario_correo(correo: int):
    try:
        # Recupero el usuario de la BD por correo electronico
        usu = db_cliente.local.usuarios.find_one({"correo": correo})
        return User(**usuario_schema(usu))
    except:
        return {"error":"elemento no encontrado"}

def buscarUsuario(campo: str, valor):
    try:
        # Recupero el usuario de la BD por correo electronico
        usu = db_cliente.local.usuarios.find_one({campo: valor})
        return User(**usuario_schema(usu))
    except:
        return {"error":"elemento no encontrado"}


