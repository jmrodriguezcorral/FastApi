from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

router = APIRouter(prefix="/usu_auth_basico",
                   tags=["usu auth basico"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

# La clase se encarga de controlar la seguridad. La instaciamos y le decimos
# que URL tendra el control de solicitar usuario y cotraseña
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Definimos un clase para el usuario autenticado
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: int

# Simulamos una Base de datos de usarios, donde tenemos usuarios y contraseña
# Creamos el objeto que recupera el usario de la BD. El mismo de usario pero con password (herencia)
class UserDB(User):
    password: str
# Simulamos los datos de la BD en JSON
users_db = {
    "pepe" : {
        "username": "pepe",
        "full_name": "Pepe Perez",
        "email": "pepe@gmail.com",
        "disable": False,
        "password" : 123456
    },
        "maria" : {
        "username": "maria",
        "full_name": "Maria Perez",
        "email": "maria@gmail.com",
        "disable": True,
        "password" : 123456
    }
}

def buscar_usuario_bd(username: str):
    # Miramos si el nombre usuario pasado es miembro de algun key de JSON de datos
    # Si esta, devovlemos un objeto UserDB con todos los datos.
    if username in users_db:
        return UserDB(**users_db[username])
    
def buscar_usuario(username: str):
    # Miramos si el nombre usuario pasado es miembro de algun key de JSON de datos
    # Si esta, devovlemos un objeto UserDB con todos los datos.
    if username in users_db:
        return User(**users_db[username])
    
async def usuario_actual(token: str = Depends(oauth2)):
    # Esta funcion depende de OAuth2PasswordBearer, cargado al inicio sobre oauth2. 
    # OAuth2PasswordBearer hace la magia. Se encarga de gesionar el token que se obtiene por login
    # Nota: en este caso hemos hecho que el token sea el nombre de usuario
    usuario = buscar_usuario(token)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="No tienes permiso",
                            headers={"WWW-Authenticate","Bearer"} # Se puede poner lo que quira, pero hay estandar
                            )
    
    if usuario.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo"
                            )
    return usuario
    
@router.post("/login")
async def login(formulario: OAuth2PasswordRequestForm = Depends()):
    # La clase OAuth2PasswordRequestForm nos proporciona un formulario por defecto para recoger datos de usuario

    # Buscamos si existe el username en nuestra BD simulada en JSON. Ojo lo hacemos con el key.  
    user_db = users_db.get(formulario.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correctp"
        )
    # Recuperamos todos los valores del usuario de la BD JSON
    usuario = buscar_usuario_bd(formulario.username)

    # Comprobamos la contraseña
    if not formulario.password == usuario.password:
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta"
        ) 
    
    # En caso de tener exito (no ha saltado ninguna excepcion) se devulve un token. JSON predefinido
    return {"access_token": usuario.username,"token_type":"bearer"}

@router.get("/usuario/yo")
async def yo(usuario: User = Depends(usuario_actual)):
    return usuario



