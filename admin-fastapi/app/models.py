# file ini untuk membuat model dari db, sekaligus untuk buat tabel
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
# import file database.py yg telah kita buat sblmnya, dimana fungsi database.py tsb sbg konektor ke db
from .database import Base
"""
setiap class merepresentasikan tabel
setiap column dlm class merepresentasikan atribut dari tabel(classnya)
"""
# tabel posts, Base as param sehingga terkoneksi ke db, ingat Base ada di database.py
class Product(Base):
    # nama tabel
    __tablename__="product"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    like = Column(Integer, default=0, nullable=True)
    image = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))