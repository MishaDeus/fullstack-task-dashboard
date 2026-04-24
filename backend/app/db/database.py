from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
#postgres:postgres - first login, second password
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/tasks_db" 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()