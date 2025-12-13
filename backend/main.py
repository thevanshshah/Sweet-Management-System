from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException # Imported HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from models import Sweet

# Setup Database (SQLite)
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Endpoint to Create a Sweet
@app.post("/api/sweets", response_model=Sweet)
def create_sweet(sweet: Sweet):
    with Session(engine) as session:
        session.add(sweet)
        session.commit()
        session.refresh(sweet)
        return sweet

# Endpoint to Get All Sweets
@app.get("/api/sweets", response_model=list[Sweet])
def read_sweets():
    with Session(engine) as session:
        sweets = session.exec(select(Sweet)).all()
        return sweets

# Endpoint to Purchase a Sweet (New Feature)
@app.post("/api/sweets/{sweet_id}/purchase", response_model=Sweet)
def purchase_sweet(sweet_id: int):
    with Session(engine) as session:
        sweet = session.get(Sweet, sweet_id)
        if not sweet:
            raise HTTPException(status_code=404, detail="Sweet not found")
        
        if sweet.quantity <= 0:
            raise HTTPException(status_code=400, detail="Sweet out of stock")
        
        sweet.quantity -= 1
        session.add(sweet)
        session.commit()
        session.refresh(sweet)
        return sweet