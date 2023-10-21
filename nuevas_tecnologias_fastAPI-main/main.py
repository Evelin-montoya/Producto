from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from database import SessionLocal
import models

app = FastAPI()


class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: int
    en_oferta: bool


db = SessionLocal()


@app.get('/productos', response_model=List[Producto], status_code=200)
def productos():
    productos = db.query(models.Producto).all()
    return productos


@app.post('/producto', response_model=Producto, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: Producto):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto.id).first()

    if db_producto is not None:
        raise HTTPException(status_code=400, detail='El producto ya existe')

    nuevo_producto = models.Producto(
        nombre=producto.nombre,
        precio=producto.precio,
        descripcion=producto.descripcion,
        en_oferta=producto.en_oferta
    )

    db.add(nuevo_producto)
    db.commit()

    return nuevo_producto

@app.put('/producto/{producto_id}', response_model=Producto, status_code=status.HTTP_200_OK)
def actualiza_un_producto(producto_id: int, producto: Producto):
    actualiza_un_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    actualiza_un_producto.nombre = producto.nombre
    actualiza_un_producto.precio = producto.precio
    actualiza_un_producto.descripcion = producto.descripcion
    actualiza_un_producto.en_oferta = producto.en_oferta

    db.commit()

    return actualiza_un_producto



@app.get('/producto/{producto_id}', response_model=Producto, status_code=status.HTTP_200_OK)
def traer_un_producto(producto_id: int):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    return producto


@app.delete('/producto/{producto_id}')
def borrar_un_producto(producto_id: int):
    borrar_un_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()

    if borrar_un_producto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")

    db.delete(borrar_un_producto)
    db.commit()

    return borrar_un_producto