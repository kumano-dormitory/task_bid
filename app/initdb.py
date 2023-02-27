from app.models.models import Base
from app.database import engine

def initdb():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
if __name__ == "__main__":
    initdb()