from sqlalchemy import Column, ForeignKey, Integer, String,DateTime,Float,PickleType,TEXT
#from sqlalchemy.dialects.mysql import LONGTEXT
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base=declarative_base()

class Admin(Base):
	__tablename__='admin'
	Id=Column(Integer,primary_key=True)
	Name=Column(String(100))
	About=Column(String(100))
	password_hash=Column(TEXT)

	def hash_password(self, password):
		self.password_hash=pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password,self.password_hash)

class Blog_data(Base):
	__tablename__='blog_data'
	Id=Column(Integer,primary_key=True,autoincrement=True)
	head=Column(String(100))
	headtag=Column(String(100))
	quote=Column(TEXT)
	Para1=Column(TEXT)
	Para2=Column(TEXT)
	Para3=Column(TEXT)
	Para4=Column(TEXT)
	Para5=Column(TEXT)
	Para6=Column(TEXT)
	Para7=Column(TEXT)
	Para8=Column(TEXT)
	Sideheads=Column(TEXT)
	links=Column(String(100))
	file=Column(String(100))
	filedescription=Column(String(100))
	Timestamp=Column(DateTime, default=datetime.datetime.utcnow)

class Response(Base):
	__tablename__='response'

	Id=Column(Integer,primary_key=True,autoincrement=True)
	name=Column(String(100))
	email=Column(String(100))
	phone=Column(Integer)
	message=Column(TEXT)
	Timestamp=Column(DateTime,default=datetime.datetime.utcnow)


engine=create_engine('sqlite:///Blog_database.db')

Base.metadata.create_all(engine)

