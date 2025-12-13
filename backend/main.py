from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from sqlmodel import SQLModel, Session, create_engine, select
from models import Sweet, User, UserCreate, UserRead
from passlib.context import CryptContext

# --- Security Setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)
# ----------------------

# Setup Database
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

# --- Auth Endpoints ---
@app.post("/api/auth/register", response_model=UserRead, status_code=201)
def register_user(user: UserCreate):
    with Session(engine) as session:
        # Check if username exists
        existing_user = session.exec(select(User).where(User.username == user.username)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Hash password and save
        hashed_pwd = get_password_hash(user.password)
        db_user = User(username=user.username, hashed_password=hashed_pwd)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

# --- Sweet Endpoints ---
@app.post("/api/sweets", response_model=Sweet)
def create_sweet(sweet: Sweet):
    with Session(engine) as session:
        session.add(sweet)
        session.commit()
        session.refresh(sweet)
        return sweet

@app.get("/api/sweets", response_model=list[Sweet])
def read_sweets():
    with Session(engine) as session:
        sweets = session.exec(select(Sweet)).all()
        return sweets

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