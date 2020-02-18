from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base

class Register(Base):
	__tablename__ = 'register'
	id = Column(Integer, primary_key=True)
	email = Column(Text)
	password = Column(Text)
	def __init__(self, email, pwd):
		self.email = email
		self.password = pwd

class Cart(Base):
	__tablename__ = 'cart'
	id = Column(Integer, primary_key=True)
	name = Column(Text)
	desc = Column(Text)
	price = Column(Text)
	img = Column(Text)
	def __init__(self, name, desc,price,img):
		self.name = name
		self.desc = desc
		self.price = price
		self.img = img
