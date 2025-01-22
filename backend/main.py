from fastapi import FastAPI, Depends
from fastapi import HTTPException
from backend.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.connection import get_connection
from sqlalchemy import text
from backend.apis.base import api_router 



app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION
    )

app.include_router(router=api_router, tags=['users'])

@app.get('/')
def hello_api():
    return {"msg":"Hello FastAPI"}

@app.get("/check_connection",)
async def healthchecker(db: AsyncSession = Depends(get_connection)
                        ):
    """
    Check connection database
    
    Depends:
        get_connection - подключение к базе данных
    
    Returns:
        if connection data pase corect, return messages
        else HTTPExeption
    """
    try:
        result = await db.execute(text("SELECT 1"))
        row = result.fetchone()
        if not row:
            raise HTTPException(
                status_code=500, 
                detail="Database is not configured correctly"
                )
        return {
            "message": "Data base normaly work"
            }
    except Exception:    

        raise HTTPException(
            status_code=500, 
            detail="Error connecting to the database"
            )