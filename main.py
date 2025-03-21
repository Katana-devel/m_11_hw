from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.fu_db import get_db
from src.routes import contacts, user, auth



app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(contacts.router, prefix="/api")


@app.get("/")
def index():
    """
    Root endpoint that returns a basic welcome message.

    Returns:
        dict: A JSON response containing a welcome message.
    """
    return {"message": "Contacts Aplication"}


@app.get("/api/healthchecker")

async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    Healthcheck endpoint used to verify database connectivity.

    This function attempts to run a simple SQL query (SELECT 1) against the database.
    If successful, it confirms the application can connect to the database.
    If the connection or query fails, it raises an HTTP 500 error indicating a problem.

    Args:
        db (AsyncSession): Asynchronous database session injected via dependency.

    Returns:
        dict: A JSON response with a success message if the database is reachable.

    Raises:
        HTTPException: If the database connection or query fails.
    """
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")