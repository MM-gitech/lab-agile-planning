# Import required modules
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from threading import Lock

# Initialize FastAPI app, counters dictionary, and thread lock
app = FastAPI()
counters = {}
lock = Lock()

# Root endpoint: Welcome message
@app.get("/")
def root():
    return {"message": "Welcome to the Counter API! Use /counter endpoints to interact."}

# Endpoint to create a new named counter with an initial value
@app.post("/counter/create")
def create_counter(name: str = Query(..., description="Name of the counter"), initial: int = Query(0, description="Initial value")):
    with lock:
        if name in counters:
            return JSONResponse({"error": "Counter already exists", "name": name, "value": counters[name]}, status_code=400)
        counters[name] = initial
        return JSONResponse({"name": name, "value": initial})

# Endpoint to delete a named counter
@app.delete("/counter/delete")
def delete_counter(name: str = Query(..., description="Name of the counter")):
    with lock:
        if name in counters:
            del counters[name]
            return JSONResponse({"message": f"Counter '{name}' deleted."})
        else:
            return JSONResponse({"error": "Counter not found", "name": name}, status_code=404)

# Endpoint to get the value of a named counter (returns 404 if not found)
@app.get("/counter")
def get_counter(name: str = Query(..., description="Name of the counter")):
    with lock:
        if name in counters:
            value = counters[name]
            return JSONResponse({"name": name, "value": value})
        else:
            return JSONResponse({"error": "Counter not found", "name": name}, status_code=404)

# Endpoint to increment a named counter
@app.post("/counter/increment")
def increment_counter(name: str = Query(..., description="Name of the counter")):
    with lock:
        counters[name] = counters.get(name, 0) + 1
        return JSONResponse({"name": name, "value": counters[name]})
