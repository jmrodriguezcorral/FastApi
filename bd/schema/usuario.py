#Aqui se hacen tranformacion de un objeto a otro con lo mapeos que sean

# Esta funcion coge objeto de usuario tipo de BD y lo pasa a normal
# Los objetos son JSON
def usuario_schema(usu) -> dict:
    return {"id": str(usu["_id"]),
            "nombre_usuario": usu["nombre_usuario"],
            "correo": usu["correo"],
            }

def usuarios_schema(usu) -> list:
    return [usuario_schema(u) for u in usu]
