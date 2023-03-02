from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "mysql://user:password@host"
# engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False})

#create database engine
engine = create_engine("sqlite:///spark-capital.db")

Base = declarative_base() # need to read -> ways to access the actual db

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

