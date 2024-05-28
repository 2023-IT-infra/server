from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from database import SessionLocal

class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = None
        db = SessionLocal()
        try:
            request.state.db = db
            response = await call_next(request)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
        return response

