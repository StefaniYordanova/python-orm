from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE_URL or CONNECTION
DATABASE_URL = "postgresql+psycopg2://postgres:stefi34@localhost:5432/sqlalchemy_db"
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

Session = sessionmaker(bind=engine)
