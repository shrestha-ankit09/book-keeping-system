from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.database.db import SessionLocal, engine, test_db_connection



async def home_page(_: Request):
    return JSONResponse({"success": True, "message": "homepage"})



app = Starlette(debug=True, routes=[Route("/", home_page)])


# Test database connection on startup
@app.on_event("startup")
async def startup():
    if test_db_connection():
        print("🚀 Application started successfully!")
    else:
        print("🔴 Application failed to start due to database connection issues.")

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# app.mount("/graphql", home_page)