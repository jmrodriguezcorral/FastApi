from fastapi import APIRouter

router = APIRouter(prefix="/productos", 
                   tags=["Productos"],
                   responses = { 404: {"mensaje":"No encontrado"} })

listaProductos=["Producto1","Producto2","Producto3","Producto4","Producto5"]

#Operaciones
@router.get("/")
async def productos():
    return listaProductos

@router.get("/{id}")
async def productos(id:int):
    return listaProductos[id]





