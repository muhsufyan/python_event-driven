import time
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from sqlalchemy import false
# import model, konektor db sqlalchemy kita
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .producer import publish
from fastapi.encoders import jsonable_encoder
import random
"""
koneksi ke db dg sql alchemy
"""
# integrasi semua resource akses ke db, yaitu models dan konektor
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dokumentasi untuk api")


class Product(BaseModel):
    title: str
    image: str

# endpoint untuk cek koneksi ke db
@app.get("/konektor", tags=["cek koneksi db"])
# gunakan dependency get_db untuk konek ke db yg bertipe session milik sqlalchemy
async def konekdb(db: Session = Depends(get_db)):
    # get semua data
    data = db.query(models.Product).all()
    # cek atribut database yg dpt diambil apa saja sekaligus cek query dlm bntk sqlnya
    print(db.query(models.Product)) # sama dg SELECT Products.id AS Products_id, Products.nama AS Products_nama, Products.umur AS Products_umur, Products.alamat AS Products_alamat, Products.published AS Products_published, Products.created_at AS Products_created_at FROM Products
    # publish()# simple publisher
    return {
        "message":"sukses terkoneksi ke db",
        "data":data
    }
@app.get("/showProduct", tags=["create new data group"], summary=["tampilkan data dari database"], description="menampilkan data database, hardcode")
async def show(db: Session = Depends(get_db)):
    data = db.query(models.Product).all()
    return{
        "data": data
    }
@app.post("/createProduct",status_code=status.HTTP_201_CREATED, tags=["create new data group"], summary=["buat data baru"], description="buat data baru dlm json lalu tangkap datanya dan tampilkan")
async def createdata2(tangkapdata: Product, db: Session = Depends(get_db)):
    # menangkap dan simpan data dlm memory sementara
    data_baru = models.Product(**tangkapdata.dict())
    """
    jika ingin lbh simpel gunakan kode sprt brkt
    print(**tangkapdata.dict())
    data_baru = models.Product(**tangkapdata.dict())
    """
    # simpan ke db
    db.add(data_baru)
    db.commit()
    db.refresh(data_baru)
    # publisher
    publish('product_created', jsonable_encoder(data_baru))
    return {
        "data": data_baru,
        "dengan **":data_baru
    }

@app.get("/showProduct/{id}", tags=["create new data group"], summary=["tampilkan data id yg ditentukan"], description="menampilkan data dari id yg ditentukan lewat parameter url")
async def showspesific(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Product).filter(models.Product.id == id).first()
    # cetak query sqlnya
    print(db.query(models.Product).filter(models.Product.id == id))
    if not data: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan'
                            )
    return{
        "data with id": data
    }

@app.delete("/Product/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["create new data group"], summary=["hapus data id yg ditentukan"], description="menghapus data dari id yg ditentukan lewat parameter url")
async def delete_Product(id: int, db: Session = Depends(get_db)):
    # get data dg id
    data = db.query(models.Product).filter(models.Product.id == id)
    if data.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan'
                            )
    # simpan ke db
    data.delete(synchronize_session=False)
    db.commit()
    # publisher
    print(data)
    publish('product_deleted', jsonable_encoder(id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/Product/{id}", tags=["create new data group"], summary=["ubah data id yg ditentukan"], description="mengubah data dari id yg ditentukan lewat parameter url")
async def update_Product(id: int, data_update: Product, db: Session = Depends(get_db)):
    cari_id = db.query(models.Product).filter(models.Product.id == id)
    data_cari = cari_id.first()
    if data_cari is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'data dengan id {id} tidak ditemukan')
    cari_id.update(data_update.dict(), synchronize_session=False)
    # simpan ke db
    db.commit()
    # publisher
    consume = {}
    consume['data'] = data_update
    consume["id"] = id
    publish('product_updated', jsonable_encoder(consume))
    print(consume)
    return {"data update": data_update.dict()}
@app.get("/randomproduct/", tags=["random id"])
async def show(db: Session = Depends(get_db)):
    data = db.query(models.Product).all()
    pilih_data = random.choice(data)
    data_id = pilih_data.id
    return{
        "id": data_id
    }
