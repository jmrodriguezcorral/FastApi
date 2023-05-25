from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime,timedelta
"""
Para pode trabajar con JWT es necesario instalar:
pip install "python-jose[cryptography]"
pip install "passlib[bcrypt]"

python-jose: nos permite generar y verificar JWT tokes en python
passlib: es una libreria de "JASEO" usaremos el algortimo bcrypt.
        La usaremos para ocultar las password
"""
from jose import jwt,JWTError,ExpiredSignatureError
from passlib.context import CryptContext

# Constantes
ALGORITMO = "HS256"
DURACION_TOKEN = 1 # ! Minuto
# Para generar una semilla segura --> openssl rand -hex 32
SECRETO = "5c73b717724528ecf8a3895fd173b5ec132c5f676067f64e47723b88bad20465"

route = APIRouter(prefix="/usu_auth_jwt",
                   tags=["usu auth jwt"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")
cript = CryptContext(schemes="bcrypt")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: int


class UserDB(User):
    password: str

# Para que las contraseña no esten elaro simulo su encriptacion
# Usar la pagina: https://bcrypt-generator.com/  y pegar a pelo el resultado
users_db = {
    "pepe" : {
        "username": "pepe",
        "full_name": "Pepe Perez",
        "email": "pepe@gmail.com",
        "disable": False,
        "password" : "$2a$12$DN9j.QqMIxd57uq4vFUxxev44qZiwEYSV3l6W3YpP5SddQmiihge6"
    },
        "maria" : {
        "username": "maria",
        "full_name": "Maria Perez",
        "email": "maria@gmail.com",
        "disable": True,
        "password" : "$2a$12$DN9j.QqMIxd57uq4vFUxxev44qZiwEYSV3l6W3YpP5SddQmiihge6"
    }
}

#############################
# Funciones que necesitamos
############################

def buscar_usuario_bd(username: str):
    # Simula la busqeuda en una BD y devulve un objeto user
    if username in users_db:
        return UserDB(**users_db[username])
    
def buscar_usuario(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def usuario_auth(token: str = Depends(oauth2) ):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no validas",
            headers={"WWW-Authenticate": "Bearer"}
    )
            
    try:
        usuario_nombre = jwt.decode(token,SECRETO,algorithms=[ALGORITMO]).get("sub")
        if usuario_nombre is None:
            raise exception
    except JWTError:
        raise exception
    
    return buscar_usuario(usuario_nombre)




async def usuario_actual(usuario: User = Depends(usuario_auth)):
    if usuario.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo"
                            )
    return usuario



##########################
# Redirecciones
#########################

# Basada en el de autenticacion basica pero cifrando el password para no guardarlo en claro
@route.post("/login")
async def login(formulario: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(formulario.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correctp"
        )

    usuario = buscar_usuario_bd(formulario.username)

    # Validar contraseña cifrada. Lo del usuario llega en claro. Hacer JASEO
    if not cript.verify(formulario.password,usuario.password):
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta"
        ) 
    
    # El tiempo de expiracion es el ahora as el tiempo de duracion de token
    expiracion = datetime.utcnow() + timedelta(minutes=DURACION_TOKEN)
    toke_acceso = {"sub":usuario.username,
                   "exp":expiracion}
    return {"access_token": jwt.encode(toke_acceso,SECRETO,algorithm=ALGORITMO),"token_type":"bearer"}

@route.get("/usuario/yo")
async def yo(usuario: User = Depends(usuario_actual)):
    return usuario