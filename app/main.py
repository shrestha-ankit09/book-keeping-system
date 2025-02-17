from starlette.applications import Starlette
from starlette.routing import Route
from ariadne.asgi import GraphQL
from app.database.db import SessionLocal, engine, test_db_connection
from app.schema.schema import schema


app = Starlette()



app.mount("/graphql", GraphQL(schema=schema, debug=True))

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


