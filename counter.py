# Import required modules and database functions
from fastapi import FastAPI, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db import SessionLocal, get_counter, create_counter as db_create_counter, increment_counter as db_increment_counter, reset_counter as db_reset_counter, delete_counter as db_delete_counter

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize FastAPI app
app = FastAPI()

# Root endpoint: Welcome message
@app.get("/")
def root():
    return {"message": "Welcome to the Counter API! Use /counter endpoints to interact."}

# Endpoint to create a new named counter with an initial value
@app.post("/counter/create")
def create_counter_endpoint(name: str = Query(..., description="Name of the counter"), initial: int = Query(0, description="Initial value"), db: Session = Depends(get_db)):
    counter = db_create_counter(db, name, initial)
    if not counter:
        existing = get_counter(db, name)
        return JSONResponse({"error": "Counter already exists", "name": name, "value": existing.value}, status_code=400)
    return JSONResponse({"name": counter.name, "value": counter.value})

# Endpoint to delete a named counter
@app.delete("/counter/delete")
def delete_counter_endpoint(name: str = Query(..., description="Name of the counter"), db: Session = Depends(get_db)):
    success = db_delete_counter(db, name)
    if success:
        return JSONResponse({"message": f"Counter '{name}' deleted."})
    else:
        return JSONResponse({"error": "Counter not found", "name": name}, status_code=404)

# Endpoint to get the value of a named counter (returns 404 if not found)
@app.get("/counter")
def get_counter_endpoint(name: str = Query(..., description="Name of the counter"), db: Session = Depends(get_db)):
    counter = get_counter(db, name)
    if counter:
        return JSONResponse({"name": counter.name, "value": counter.value})
    else:
        return JSONResponse({"error": "Counter not found", "name": name}, status_code=404)

# Endpoint to increment a named counter
@app.post("/counter/increment")
def increment_counter_endpoint(name: str = Query(..., description="Name of the counter"), db: Session = Depends(get_db)):
    counter = db_increment_counter(db, name)
    return JSONResponse({"name": counter.name, "value": counter.value})
    
