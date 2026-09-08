from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:stefi34@localhost:5432/sqlalchemy_exercise"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()
