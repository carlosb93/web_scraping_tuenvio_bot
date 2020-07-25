import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    arroba = Column(String(255))
    lang = Column(String(255))
    tgid = Column(Integer, nullable=True)
    phone = Column(Integer, nullable=True)
    pay = Column(Integer, nullable=True)
    pay_date = Column(Integer, nullable=True)
    # payment = Column(Integer, nullable=True)

class Productos(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    code = Column(String(255))#codigo que machea con el code de setting
    
class Modulos(Base):
    __tablename__ = 'modulos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    url = Column(String(255))
    
class ProdModules(Base):
    __tablename__ = 'prodmodules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, nullable=True) 
    product_id = Column(Integer, nullable=True) 
    

class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    code = Column(String(255))
    setting_type = Column(String(255))
    # ---setting_type---
    # alert
    # basic
    # conf
    
class Settings4User(Base):
    __tablename__ = 'settings4user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    setting_id = Column(Integer, nullable=True) 
    user_id = Column(Integer, nullable=True) 
    