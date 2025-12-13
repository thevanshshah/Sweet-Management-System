from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import FastAPI, HTTPException, status, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, create_engine, select
from passlib.context import CryptContext
from jose import JWTError, jwt

# Import your models
from models import Sweet, User, UserCreate, UserRead

# --- Configuration ---
SECRET_KEY = "mysecretkey" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Security Setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Database Setup ---
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# --- Dependencies ---

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user

# NEW: Admin Only Dependency
async def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, 
            detail="Not authorized. Admin privileges required."
        )
    return current_user

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sweet Shop API!"}

# --- Auth Endpoints ---

@app.post("/api/auth/register", response_model=UserRead, status_code=201)
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    # --- SECURITY CHECK: VALIDATE ROLE ---
    if user.role not in ["admin", "customer"]:
        raise HTTPException(status_code=400, detail="Role must be 'admin' or 'customer'")
    # -------------------------------------

    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pwd = get_password_hash(user.password)
    # Default is customer, but we allow 'admin' for this assessment demo
    db_user = User(username=user.username, hashed_password=hashed_pwd, role=user.role)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.post("/api/auth/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, # Include role in token
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

# --- Sweet Endpoints ---

# 1. List Sweets (Public)
@app.get("/api/sweets", response_model=List[Sweet])
def read_sweets(session: Session = Depends(get_session)):
    sweets = session.exec(select(Sweet)).all()
    return sweets

# 2. Search Sweets (Public) - NEW
@app.get("/api/sweets/search", response_model=List[Sweet])
def search_sweets(
    q: Optional[str] = Query(None, min_length=1),
    session: Session = Depends(get_session)
):
    if not q:
        return []
    statement = select(Sweet).where(
        (Sweet.name.contains(q)) | (Sweet.category.contains(q))
    )
    results = session.exec(statement).all()
    return results

# 3. Create Sweet (Admin Only) - UPDATED
@app.post("/api/sweets", response_model=Sweet)
def create_sweet(
    sweet: Sweet, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin) # <--- Locked
):
    session.add(sweet)
    session.commit()
    session.refresh(sweet)
    return sweet

# 4. Update Sweet (Admin Only) - NEW
@app.put("/api/sweets/{sweet_id}", response_model=Sweet)
def update_sweet(
    sweet_id: int,
    sweet_data: Sweet,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin) # <--- Locked
):
    db_sweet = session.get(Sweet, sweet_id)
    if not db_sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    
    db_sweet.name = sweet_data.name
    db_sweet.category = sweet_data.category
    db_sweet.price = sweet_data.price
    db_sweet.quantity = sweet_data.quantity
    
    session.add(db_sweet)
    session.commit()
    session.refresh(db_sweet)
    return db_sweet

# 5. Delete Sweet (Admin Only) - NEW
@app.delete("/api/sweets/{sweet_id}")
def delete_sweet(
    sweet_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin) # <--- Locked
):
    sweet = session.get(Sweet, sweet_id)
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    session.delete(sweet)
    session.commit()
    return {"ok": True}

# 6. Purchase (Logged in Users) - RENAMED from "Buy" logic
@app.post("/api/sweets/{sweet_id}/purchase", response_model=Sweet)
def purchase_sweet(
    sweet_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user) # Any logged in user
):
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

# 7. Restock (Admin Only) - NEW
@app.post("/api/sweets/{sweet_id}/restock")
def restock_sweet(
    sweet_id: int,
    amount: int = 10, # Default restock amount
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin) # <--- Locked
):
    sweet = session.get(Sweet, sweet_id)
    if not sweet:
        raise HTTPException(status_code=404, detail="Sweet not found")
    
    sweet.quantity += amount
    session.add(sweet)
    session.commit()
    session.refresh(sweet)
    return sweet