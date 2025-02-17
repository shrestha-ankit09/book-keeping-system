from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv
load_dotenv()




DATABASE_URL=os.getenv("DATABASE_URL")
print(f"database url is: {DATABASE_URL}")


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



Base = declarative_base()


# Function to test database connection
def test_db_connection():
    try:
        # Attempt to connect to the database
        connection = engine.connect()
        connection.close()
        print("✅ Database connection successful!")
        return True
    except SQLAlchemyError as e:
        print(f"❌ Database connection failed: {e}")
        return False