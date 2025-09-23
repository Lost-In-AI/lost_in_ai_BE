from sqlalchemy import text 
from sqlmodel import create_engine

from core.configs import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.DATABASE_ECHO)
  

def test_connection():
  try:
    with engine.connect() as conn:
      conn.execute(text("SELECT 1"))
      return True
  except Exception as e:
    print(f"Errore nella connessione al database: {e}")
    return False
  
  