from datetime import timedelta, datetime
from typing import Optional

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import BaseModel, Field
from starlette import status
import bcrypt
import schemas
from database import get_db


# --- Configuration ---
SECRET_KEY = "608da1e8a2155282f424624a1ad74bc4dba6841c4efe1346b2a023204454fd12"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Setup Auth
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/admin/token")
# REMOVED: bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}}
)


# --- Pydantic Models ---
class AdminCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=8, max_length=72)


def pass_hash_converter(password: str):
    """
    Hashes the password using bcrypt directly.
    Truncates to 72 bytes as required by bcrypt.
    """
    # Convert to bytes and truncate to 72 bytes
    password_bytes = password.encode('utf-8')[:72]
    # Generate salt and hash
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Return as string for database storage
    return hashed.decode('utf-8')


def verify_password(password: str, hash_pass: str):
    """
    Verify password using bcrypt directly.
    Truncates to 72 bytes as required by bcrypt.
    """
    # Convert password to bytes and truncate
    password_bytes = password.encode('utf-8')[:72]
    # Convert stored hash to bytes
    hash_bytes = hash_pass.encode('utf-8')
    # Verify
    return bcrypt.checkpw(password_bytes, hash_bytes)


def authenticate_admin(admin_username: str, password: str, db: Session):
    admin = db.query(schemas.Admin).filter(schemas.Admin.username == admin_username).first()
    if not admin:
        return False
    if not verify_password(password, admin.hashed_pass):
        return False
    return admin


def create_access_token(username: str, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=20)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise get_user_exception()
        return {"username": username}
    except JWTError:
        raise get_user_exception()


# --- Exceptions ---
def token_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_user_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

# --- Routes ---


@router.post("/add")
async def create_newadmin(newadmin: AdminCreate, db: Session = Depends(get_db)):
    try:
        # Check if admin already exists
        existing_admin = db.query(schemas.Admin).filter(schemas.Admin.username == newadmin.username).first()
        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin with this username already exists",
            )

        admin_value = schemas.Admin()
        admin_value.username = newadmin.username
        # Hash password correctly
        admin_value.hashed_pass = pass_hash_converter(newadmin.password)

        db.add(admin_value)
        db.commit()

        return {
            "message": "Admin user created successfully",
            "username": admin_value.username
        }
    except Exception as e:
        print(f"ERROR in create_newadmin: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


@router.post("/token")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(),
                    db: Session = Depends(get_db)):
    admin = authenticate_admin(form_data.username, form_data.password, db)
    if not admin:
        raise token_exception()

    token_expires = timedelta(minutes=20)
    token = create_access_token(admin.username, expires_delta=token_expires)

    return {"access_token": token, "token_type": "bearer"}
