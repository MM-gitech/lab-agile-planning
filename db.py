# db.py: Database setup and Counter model for FastAPI
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL and engine setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./counters.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Counter model definition
class Counter(Base):
	__tablename__ = "counters"
	name = Column(String, primary_key=True, index=True)
	value = Column(Integer, default=0)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Utility functions for counter operations
def get_counter(db, name):
	"""Retrieve a counter by name."""
	return db.query(Counter).filter(Counter.name == name).first()

def create_counter(db, name, initial=0):
	"""Create a new counter with a given name and initial value."""
	db_counter = get_counter(db, name)
	if db_counter:
		return None
	counter = Counter(name=name, value=initial)
	db.add(counter)
	db.commit()
	db.refresh(counter)
	return counter

def increment_counter(db, name):
	"""Increment the value of a counter by name. Creates the counter if it does not exist."""
	counter = get_counter(db, name)
	if not counter:
		counter = Counter(name=name, value=1)
		db.add(counter)
	else:
		counter.value += 1
	db.commit()
	db.refresh(counter)
	return counter

def delete_counter(db, name):
	"""Delete a counter by name."""
	counter = get_counter(db, name)
	if counter:
		db.delete(counter)
		db.commit()
		return True
	return False
